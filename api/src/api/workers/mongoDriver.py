import pymongo
from pymongo import Connection
from datetime import datetime
from src.utils import customLogger
from conf import config
workerLogger = customLogger.getWorkerLogger()
connection = Connection()
db = connection.local

def getVhostId(vhost):
  vhost_id = ""
  if vhost is None:
    return None
  for find in db[config.vhostCollection].find({'vhost': vhost}):
    vhost_id = str(find["_id"])
    break
  return vhost_id


def getVisitArrAll(vhost = None, modulo = None, startDate = None, endDate = None):
  if vhost is None or startDate is None or endDate is None\
     or modulo is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  vhost_id = getVhostId(vhost)
  if vhost_id is None:
    return None, "vhost " + vhost + " not found"
  pipeline = [
    {'$match': \
      { "$and": \
        [{'vhost': vhost_id}, \
         {'timestamp': {"$gte" : startDate,\
                        "$lte" : endDate}}]\
      }\
    },
    {'$project': \
      {'dateLowerBound': \
        { "$subtract": \
          ['$timestamp', 
            {"$mod": ['$timestamp', modulo]\
         }]\
        }\
      }\
    },
    {'$group': 
      {'_id':"$dateLowerBound",\
       'count': {"$sum": 1}\
      }\
    }\
  ]
  q = db.command('aggregate', config.aplogCollection, pipeline=pipeline)
    
  #q = db.command('aggregate', 'aplogs', pipeline=pipeline, explain = True)
  return q["result"], ""

def getVisitArrAllHtml(vhost = None, modulo = None, startDate = None, endDate = None):
  if vhost is None or startDate is None or endDate is None\
     or modulo is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  pipeline = [
    {'$match': \
      { "$and": \
        [{'vhost': vhost}, \
         {'timestamp': {"$gte" : startDate,\
                        "$lte" : endDate}}]\
      }\
    },
    {'$project': \
      {'dateLowerBound': \
        { "$subtract": \
          ['$timestamp', 
            {"$mod": ['$timestamp', modulo]\
         }]\
        }\
      }\
    },
    {'$group': 
      {'_id':"$dateLowerBound",\
       'count': {"$sum": 1}\
      }\
    }\
  ]
  q = db.command('aggregate', config.aplogCollection, pipeline=pipeline)
    
  #q = db.command('aggregate', 'aplogs', pipeline=pipeline, explain = True)
  return q["result"], ""
