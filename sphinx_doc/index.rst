.. pocket documentation master file, created by
   sphinx-quickstart on Tue Dec 17 11:15:22 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

Pocket is a plugin for the Sneeze nose plugin.  It adds all messages passed
through normal usage of Python's ``logging`` module to the data recorded in the
database.

Installation and Quickstart
===========================

Installing pocket (``pip install sneeze-pocket``) will enable it for all 
``nosetests`` runs where Sneeze is enabled.

Overview
========

Pocket works by attaching a handler to the root logger.  This handler writes
all handled messages to the database.  You can control the volume of messages
with standard logging module mechanisms like log levels and other filters.
Note that you may run in to some problems dispatching log messages from within
Sneeze plugins.

Pocket attaches messages to the Case Execution record.  It batches writes to
increase performance.  Messages are written to the DB when there are
``--pocket-batch-size`` messages queued, when it has been
``--pocket-batch-frequency`` seconds since messages were written to the DB,
or when a case is exited, whichever happens first.  While writes are batched,
the time a message was created is recorded when the message is handled, so
will still be an accurate reference to when the activity that triggered the
message occurred.

Repo
====
https://github.com/NYTimes/pocket

Details
=======

.. toctree::
   :maxdepth: 2
   
   command_line_options

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

