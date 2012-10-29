import sys, os
from src.utils import customLogger

class threadCache():
    
    def __init__(self):
        self.sid = ""
        self.userid = ""

    def getSessionId(self):
        return self.sid

    def setSessionId(self, id):
        self.sid = id

    def setUserId(self, id):
        self.userid = id

    def setLogger(self, loggerObj):
        self.logger = loggerObj
        
    def error(self, msg):
        filename, linenum, funcname = self.findCaller()
        a, b, c = filename.rpartition('/')
        self.logger.error(c + ":" + funcname + "(): - [" + self.sid + "] [" + self.userid + "] "+ msg)

    def debug(self, msg):
        filename, linenum, funcname = self.findCaller()
        a, b, c = filename.rpartition('/')
        self.logger.debug(c + ":" + funcname + "(): - [" + self.sid + "] [" + self.userid + "] "+ msg)

    def critical(self, msg):
        filename, linenum, funcname = self.findCaller()
        a, b, c = filename.rpartition('/')
        self.logger.critical(c + ":" + funcname + "(): - [" + self.sid + "] [" + self.userid + "] "+ msg)

    # next bit filched from 1.5.2's inspect.py
    def currentFrame(self):
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except:
            return sys.exc_info()[2].tb_frame.f_back
        

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = self.currentFrame()
        if f is not None:
            f = f.f_back
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        rv = (co.co_filename, f.f_lineno, co.co_name)
        return rv

