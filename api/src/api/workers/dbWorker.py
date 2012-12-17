from src.utils import customLogger
from src.api.workers import mongoDriver
workerLogger = customLogger.getWorkerLogger()
def getResponse(hostname = None, scale = None, time_from = None, time_to = None):
  if hostname is None or scale is None or time_from is None or time_to is None:
    workerLogger.error("Invalid input parameters")
    return None, False, "Invalid input parameters"
 
  if scale == 1:
    modulo = 60
  elif scale == 2:
    modulo = 3600
  elif scale == 3:
    modulo = 86400
  elif scale == 4:
    modulo = 604800
  elif scale == 5:
    modulo = 2592000
  elif scale == 6:
    modulo = 31536000
  else:
    workerLogger.error("Invalid scale")
    return None, False, "Invalid scale"
  
  dbResDict = None
  dbResDict, errmsg = mongoDriver.getVisitArrAll(vhost = hostname, modulo = modulo,\
                             startDate = time_from, endDate = time_to)
  if errmsg is None:
    workerLogger.error("Error fetching response from backend")
    return None, False, "Error fetching response from backend"

  visitAllDict = populateDict(dbResDict, time_from, time_to, modulo)
  #print "visit dict is : ", visitAllDict
  resp_dict = {}
  resp_dict['resp_struct'] = {}
  resp_dict['resp_struct']['visit_struct'] = visitAllDict
  print "resp dict:: ", resp_dict
  cnt = len(resp_dict["resp_struct"]["visit_struct"])
  print "count is : ", cnt, "***********\n"
  return resp_dict, True, ""

def populateDict(dbResDict, time_from, time_to, modulo):
  idx = time_from
  i = 0
  tmp_dict = {}
  tmp_count = len(dbResDict)
  while True:
    tmp_dict[str(dbResDict[i]['_id'])] = dbResDict[i]['count']
    i = i + 1
    if i == tmp_count:
      break
  print "tmp dict:: ", tmp_dict
  i = 0
  visitAllDict = []
  while True:
    visitAllDict.append({})
    visitAllDict[i]['visit_time'] = idx
    tmpDictIdx = str(idx) + ".0"
    if tmpDictIdx in tmp_dict:
      visitAllDict[i]['num_visits_all'] = tmp_dict[tmpDictIdx]
    else:
      visitAllDict[i]['num_visits_all'] = 0
    
    # add code for num_visits_html
    visitAllDict[i]['num_visits_html'] = 0
    idx = idx + modulo
    i = i + 1
    if idx > time_to:
      break
  return visitAllDict
   
  
  
  
