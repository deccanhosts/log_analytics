from src.utils import threadCache
from src.utils import customLogger
import json
import time
import log_analytics_proto
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
        
    if tcacheObj is not None:
      if tcacheObj.logger is not None or len(tcacheObj.logger) > 0:
        tcacheObj.error("Error Code: " + str(code) + " " + detail)
      else:
        apiLogger.error("Error Code: " + str(code) + " " + detail)
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


def getCurrentTime():
  return int(time.mktime(time.gmtime())) - int(time.mktime(time.gmtime(0)))


def gettcacheObj():
    global tcacheObj

    if tcacheObj is not None:
        return tcacheObj

    tcacheObj = threadCache.threadCache()
    return tcacheObj


def getTestRespDict(req_id = None):
  resp_dict = {}
  resp_dict["req_id"] = req_id
  resp_dict["debug_msg"] = {}
  
  resp_dict["debug_msg"]["query_time"] = 98.65
  resp_dict["debug_msg"]["ctrl_msg"]   = "Test debug message"
  resp_dict["resp_struct"] = {}
  
  resp_dict["resp_struct"]["page_views"]         = 777
  resp_dict["resp_struct"]["total_visits"]       = 143
  resp_dict["resp_struct"]["unique_visits"]      = 115
  resp_dict["resp_struct"]["pages_per_visit"]    = 5.43
  resp_dict["resp_struct"]["avg_visit_duration"] = 289
  resp_dict["resp_struct"]["visit_struct"] = []

  resp_dict["resp_struct"]["visit_struct"].append({})
  resp_dict["resp_struct"]["visit_struct"][0]["visit_time"] = 1349340137
  resp_dict["resp_struct"]["visit_struct"][0]["num_visits"] = 20

  
  #resp_dict["resp_struct"]["visit_struct"][1] = {}
  resp_dict["resp_struct"]["visit_struct"].append({})
  resp_dict["resp_struct"]["visit_struct"][1]["visit_time"] = 1349341137
  resp_dict["resp_struct"]["visit_struct"][1]["num_visits"] = 12

  #resp_dict["resp_struct"]["visit_struct"][2] = {}
  resp_dict["resp_struct"]["visit_struct"].append({})
  resp_dict["resp_struct"]["visit_struct"][2]["visit_time"] = 1349342137
  resp_dict["resp_struct"]["visit_struct"][2]["num_visits"] = 38

  #resp_dict["resp_struct"]["visit_struct"][3] = {}
  resp_dict["resp_struct"]["visit_struct"].append({})
  resp_dict["resp_struct"]["visit_struct"][3]["visit_time"] = 1349343137
  resp_dict["resp_struct"]["visit_struct"][3]["num_visits"] = 27

  #resp_dict["resp_struct"]["visit_struct"][4] = {}
  resp_dict["resp_struct"]["visit_struct"].append({})
  resp_dict["resp_struct"]["visit_struct"][4]["visit_time"] = 1349344137
  resp_dict["resp_struct"]["visit_struct"][4]["num_visits"] = 44

  return resp_dict


def constructRespObj(resp_dict = None, req_id = None):

  if resp_dict is None:
    return None, False, "Invalid response returned by DB"

  if req_id is None:
    return None, False, "Request id in response cannot be NULL"
  
  resp_obj = log_analytics_proto.resp_msg()
  resp_obj.req_id = req_id
  
  if "debug_msg" in resp_dict:
    debug_msg_obj = log_analytics_proto.debug_msg()
    if resp_dict["debug_msg"]["query_time"] is not None:
      debug_msg_obj.query_time = resp_dict["debug_msg"]["query_time"]
    if resp_dict["debug_msg"]["ctrl_msg"] is not None:
      debug_msg_obj.ctrl_msg = resp_dict["debug_msg"]["ctrl_msg"]
    resp_obj.dbg = debug_msg_obj
  if "resp_struct" in resp_dict:
    resp_struct_obj = log_analytics_proto.resp_struct()      
    if "page_views" in resp_dict["resp_struct"]:
      resp_struct_obj.page_views = resp_dict["resp_struct"]["page_views"]
    if "total_visits" in resp_dict["resp_struct"]:
      resp_struct_obj.total_visits = resp_dict["resp_struct"]["total_visits"]
    if "unique_visits" in resp_dict["resp_struct"]:
      resp_struct_obj.unique_visits = resp_dict["resp_struct"]["unique_visits"]
    if "pages_per_visit" in resp_dict["resp_struct"]:
      resp_struct_obj.pages_per_visit = resp_dict["resp_struct"]["pages_per_visit"]
    if "avg_visit_duration" in resp_dict["resp_struct"]:
      resp_struct_obj.avg_visit_duration = resp_dict["resp_struct"]["avg_visit_duration"]
        
    if "visit_struct" in resp_dict["resp_struct"]:
      cnt = len(resp_dict["resp_struct"]["visit_struct"])
      print "count is : ", cnt
      i = 0
      visit_struct_obj = []
      while i < cnt:
        print "**********", i , "***********\n"
        tmp_visit_struct_obj = log_analytics_proto.visit_struct()
        visit_struct_obj.append(tmp_visit_struct_obj)
        if resp_dict["resp_struct"]["visit_struct"][i]["visit_time"] is not None:
          visit_struct_obj[i].visit_time = resp_dict["resp_struct"]["visit_struct"][i]["visit_time"]
        if resp_dict["resp_struct"]["visit_struct"][i]["num_visits_all"] is not None:
          visit_struct_obj[i].num_visits_all = resp_dict["resp_struct"]["visit_struct"][i]["num_visits_all"]
        if resp_dict["resp_struct"]["visit_struct"][i]["num_visits_html"] is not None:
          visit_struct_obj[i].num_visits_html = resp_dict["resp_struct"]["visit_struct"][i]["num_visits_html"]
        #resp_struct_obj.visit_arr[i] = visit_struct_obj
        i = i + 1
      resp_struct_obj.visit_arr = visit_struct_obj  
    resp_obj.resp = resp_struct_obj
  return resp_obj, True, ""
  
