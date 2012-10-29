import logging, logging.handlers
import time

levelDict = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}

logDir = "/var/log/log_analytics_api/"

ApiLogger = None
WorkerLogger = None

# returns a logger object at a specified location

def getApiLogger(logLevel = 'DEBUG', maxBytes = 102400, backupCount = 15):
    global ApiLogger

    if ApiLogger is not None:
        return ApiLogger
    else:
        ApiLogger = createLogger(logFileName="api_trace.log", logLevel = 'DEBUG', maxBytes = 102400, backupCount = 15)
        return ApiLogger

def getWorkerLogger(logLevel = 'DEBUG', maxBytes = 102400, backupCount = 15):
    global WorkerLogger

    if WorkerLogger is not None:
        return WorkerLogger
    else:
        WorkerLogger = createLogger(logFileName="worker_trace.log", logLevel = 'DEBUG', maxBytes = 102400, backupCount = 15)
        return WorkerLogger

def createLogger(logFileName = None, logLevel = 'DEBUG', maxBytes = 102400, backupCount = 15):
    if logFileName:
        logFileAbsPath = logDir + logFileName
        logger = logging.getLogger(logFileAbsPath) #this might need some change
        logger.setLevel(levelDict[logLevel])
        logging.Formatter.converter = time.gmtime
        formatter = logging.Formatter("%(asctime)s: %(filename)s: %(funcName)s: %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler(logFileAbsPath,
                                                       maxBytes=maxBytes,
                                                       backupCount=backupCount)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        appLogger = logger
        return appLogger
    return None 

