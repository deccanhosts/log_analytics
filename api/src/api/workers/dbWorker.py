from src.utils import customLogger
from src.api.workers import mongoDriver
from dateutil.relativedelta import relativedelta
import datetime
from datetime import datetime
import calendar

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
  
  if scale != 5:
    dbResDictAll = None
    dbResDictAll, errmsg = mongoDriver.getVisitArrAll(vhost = hostname, modulo = modulo,\
                             startDate = time_from, endDate = time_to)
    if errmsg is None:
      workerLogger.error("Error fetching response from backend")
      return None, False, "Error fetching response from backend"

    dbResDictHtml = None
    dbResDictHtml, errmsg = mongoDriver.getVisitArrHtml(vhost = hostname, modulo = modulo,\
                             startDate = time_from, endDate = time_to)
    if errmsg is None:
      workerLogger.error("Error fetching response from backend")
      return None, False, "Error fetching response from backend"

    visitDict = populateDict(dbResDictAll, dbResDictHtml, time_from, time_to, modulo)

  else:
    i = 0
    dbResDictAll  = []
    dbResDictHtml = []
    time_from_datetime = datetime.utcfromtimestamp(time_from)
    startDate = calendar.timegm((time_from_datetime + relativedelta(day=1)).timetuple()) -1
    endDate = calendar.timegm((time_from_datetime + relativedelta(day=1, months=+1, days=-1)).timetuple()) 
    modulo = endDate - startDate
    visitDict = []
    while i < 12:
      print "startDate:: ", startDate
      print "endDate:: ", endDate
      tmpResDictAll = None
      modulo = endDate - startDate
      tmpResDictAll, errmsg = mongoDriver.getVisitArrAll(vhost = hostname, modulo = modulo,\
                             startDate = startDate, endDate = endDate)

      dbResDictAll.append({})
      visitDict.append({})
      if len(tmpResDictAll) > 0:
        dbResDictAll[i]['count'] = tmpResDictAll[0]['count']
      else:
        dbResDictAll[i]['count'] = 0
      

      if errmsg is None:
        workerLogger.error("Error fetching response from backend")
        return None, False, "Error fetching response from backend"

      tmpResDictHtml = None
      tmpResDictHtml, errmsg = mongoDriver.getVisitArrHtml(vhost = hostname, modulo = modulo,\
                             startDate = startDate, endDate = endDate)
      if errmsg is None:
        workerLogger.error("Error fetching response from backend")
        return None, False, "Error fetching response from backend"
      
      dbResDictHtml.append({})
      if len(tmpResDictHtml) > 0:
        dbResDictHtml[i]['count'] = tmpResDictHtml[0]['count']
      else:
        dbResDictHtml[i]['count'] = 0

      visitDict[i]['visit_time'] = startDate
      visitDict[i]['num_visits_all'] = dbResDictAll[i]['count']
      visitDict[i]['num_visits_html'] = dbResDictHtml[i]['count']

      startDate = calendar.timegm((time_from_datetime + relativedelta(day=1, months=+i)).timetuple()) - 1
      endDate = calendar.timegm((time_from_datetime + relativedelta(day=1, months=+i, days=-1)).timetuple())
      i = i + 1   

  #print "visit dict is : ", visitAllDict
  resp_dict = {}
  resp_dict['resp_struct'] = {}
  resp_dict['resp_struct']['visit_struct'] = visitDict
  print "resp dict:: ", resp_dict
  cnt = len(resp_dict["resp_struct"]["visit_struct"])
  print "count is : ", cnt, "***********\n"
  return resp_dict, True, ""


def populateDict(dbResDictAll, dbResDictHtml, time_from, time_to, modulo):
  idx = time_from
  i = 0
  tmp_dict = {}
  tmp_count = len(dbResDictAll)
  while True:
    if tmp_count == 0:
      break
    tmp_dict[str(dbResDictAll[i]['_id'])] = dbResDictAll[i]['count']
    i = i + 1
    if i == tmp_count:
      break
  print "tmp dict:: ", tmp_dict

  i = 0
  tmp_dict2 = {}
  tmp_count2 = len(dbResDictHtml)
  while True:
    if tmp_count2 == 0:
      break
    tmp_dict2[str(dbResDictHtml[i]['_id'])] = dbResDictHtml[i]['count']
    i = i + 1
    if i == tmp_count2:
      break
  print "tmp dict html:: ", tmp_dict2
 

  i = 0
  visitDict = []
  while True:
    visitDict.append({})
    visitDict[i]['visit_time'] = idx
    tmpDictIdx = str(idx) + ".0"
    if tmpDictIdx in tmp_dict:
      visitDict[i]['num_visits_all'] = tmp_dict[tmpDictIdx]
    else:
      visitDict[i]['num_visits_all'] = 0
    
    if tmpDictIdx in tmp_dict2:
      visitDict[i]['num_visits_html'] = tmp_dict2[tmpDictIdx]
    else:
      visitDict[i]['num_visits_html'] = 0

    idx = idx + modulo
    i = i + 1
    if idx > time_to:
      break
  return visitDict
   
  
  
  
