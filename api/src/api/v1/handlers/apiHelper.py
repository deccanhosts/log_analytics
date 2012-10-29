from src.utils import threadCache
from src.utils import customLogger
import json
from piston.utils import rc
from src.utils import customLogger
apiLogger = customLogger.getApiLogger()

tcacheObj = None


def badRequest(code = None, detail = None, description = None):

    global tcacheObj
    
    if not detail:
        detail = "Invalid request"
    if not description:
        description = detail
        
    if tcacheObj.logger is not None or len(tcacheObj.logger) > 0:
        tcacheObj.error("Error Code: " + str(code) + " " + detail)
    else:
        apiLogger.error("Error Code: " + str(code) + " " + detail)

    resp = rc.BAD_REQUEST
    resp['Content-Type'] = 'application/json; charset=utf-8'
    resp.content = json.dumps({"error": {"code": code, "detail": detail, "description": description }})
    return resp


def init(reqId = "NA"):

    if reqId is None:
        reqId = "NA"

    userName = "NA"

    global tcacheObj

    if tcacheObj is None:
        tcacheObj = threadCache.threadCache()

    tcacheObj.setSessionId(reqId)
    tcacheObj.setUserId(userName)
    tcacheObj.setLogger(customLogger.getApiLogger())
    return tcacheObj


def gettcacheObj():
    global tcacheObj

    if tcacheObj is not None:
        return tcacheObj

    tcacheObj = threadCache.threadCache()
    return tcacheObj

