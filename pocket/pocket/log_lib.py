from logging import Handler, getLogger


def add_options(parser, env):
    
    parser.add_option('--close-pocket',
                      action='store_true',
                      dest='close_pocket')
    parser.add_option('--pocket-batch-size',
                      action='store',
                      dest='pocket_batch_size',
                      type=int,
                      default=10)

class TissueHandler(Handler):
    
    def __init__(self, tissue, options, noseconfig):
        
        Handler.__init__(self)
        self.tissue = tissue
        self.message_buffer_size = options.pocket_batch_size
        self.buffered_messsage_count = 0
        self.session = None
        self.session_objects = {}
        self.last_error = None
        getLogger().addHandler(self)
    
    @classmethod
    def enabled(cls, tissue, options, noseconfig):
        
        return not options.close_pocket
    
    def after_enter_case(self, case, description):
        
        last_session = self.session
        self.session, self.session_objects = self.tissue.make_session(False)
        if last_session:
            last_session.close()
    
    def emit(self, record):
        
        if self.session_objects:
            try:
                message = record.message
            except AttributeError:
                message = record.msg
            self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage'](message,
                                                                                                           record.levelname, 
                                                                                                           record.name))
            self.buffered_messsage_count += 1
            if self.buffered_messsage_count >= self.message_buffer_size:
                self.flush()
    
    def flush(self):
        
        self.tissue.access_lock.acquire()
        self.session.commit()
        self.buffered_messsage_count = 0
        self.tissue.access_lock.release()
    
    def peek_error(self, test, err):
        
        self.last_error = err
    
    def handle_skip(self, message):
        
        self.acquire()
        if self.session_objects:
            sep = self.last_error[1].message if hasattr(self.last_error[1], 'message') else self.last_error[1].msg
            if sep:
                _, error, capture = message.partition(sep)
            else:
                _, error, capture = message.partition('\n')
            error = message
            capture = capture.strip('\n')
            message = 'Test Skipped' + ((': %s' % error) if error else '')
            self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage'](message,
                                                                                                           'WARN', 
                                                                                                           'test.result'))
            self.buffered_messsage_count += 1
            if capture:
                self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage'](capture,
                                                                                                               'DEBUG', 
                                                                                                               'test.capture'))
                self.buffered_messsage_count += 1
        self.release()
    
    def handle_fail(self, message):
        
        self.acquire()
        if self.session_objects:
            sep = self.last_error[1].message if hasattr(self.last_error[1], 'message') else self.last_error[1].msg
            if sep:
                _, error, capture = message.partition(sep)
            else:
                _, error, capture = message.partition('\n')
            capture = capture.strip('\n')
            message = 'Test Failed' + ((': %s' % error) if error else '')
            self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage'](message,
                                                                                                           'CRITICAL', 
                                                                                                           'test.result'))
            self.buffered_messsage_count += 1
            if capture:
                self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage'](capture,
                                                                                                               'DEBUG', 
                                                                                                               'test.capture'))
                self.buffered_messsage_count += 1
        self.release()
    
    def handle_pass(self):
        
        self.acquire()
        if self.session_objects:
            self.session_objects['case_execution'].log_messages.append(self.tissue.db_models['LogMessage']('Test Passed',
                                                                                                           'INFO', 
                                                                                                           'test.result'))
            self.buffered_messsage_count += 1
        self.release()
    
    def after_exit_case(self, result):
        
        self.flush()
    
    def exit_cycle(self):
        
        self.flush()