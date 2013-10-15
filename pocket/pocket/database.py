from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


def add_models(Base):
    
    class LogMessage(Base):
        
        __tablename__ = 'logMessage'
        
        id = Column(Integer, primary_key=True)
        case_execution_id = Column(Integer, ForeignKey('testCaseExecution.id'))
        case_execution = relationship('CaseExecution', backref='log_messages')
        message = Column(String(5000))
        level = Column(String(20))
        source = Column(String(200))
        time_logged = Column(DateTime)
        
        def __init__(self, message, level, source, case_execution=None, time=None):
            
            try:
                self.case_execution_id = int(case_execution)
            except:
                self.case_execution = case_execution
            self.message = message
            self.level = level
            self.source = source
            self.time_logged = time if time is not None else datetime.now()
    
    return {'LogMessage' : LogMessage}