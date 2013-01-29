import pymongo
from pymongo import Connection
from datetime import datetime
from src.utils import customLogger
from conf import config
from bson.objectid import ObjectId

import re
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


def getUserAgent(ua_id):

  user_agent = ""
  #print "ua_id :::", ua_id
  if ua_id is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"
  for find in db[config.useragentCollection].find({'_id': ObjectId(ua_id)}):
    user_agent = str(find["user_agent"])
    break
  return user_agent   


def getVisitArrAll(vhost = None, modulo = None, startDate = None, endDate = None):
  if vhost is None or startDate is None or endDate is None\
     or modulo is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"
  
  endTimestamp = endDate + modulo
  vhost_id = getVhostId(vhost)
  if vhost_id is None:
    return None, "vhost " + vhost + " not found"
  pipeline = [
    {'$match': \
      { "$and": \
        [{'vhost': vhost_id}, \
         {'timestamp': {"$gte" : startDate,\
                        "$lte" : endTimestamp}}]\
      }\
    },
    {'$project': \
      {'dateLowerBound': \
        { "$subtract": \
          ['$timestamp',\
            {"$mod": [\
              {"$subtract": ['$timestamp', startDate]},\
            modulo]\
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
  #print "pipeline is ::", pipeline, "********\n"
    
  #q = db.command('aggregate', 'aplogs', pipeline=pipeline, explain = True)
  #print "result... " , q, "********\n"
  return q["result"], ""

def getVisitArrHtml(vhost = None, modulo = None, startDate = None, endDate = None):
  if vhost is None or startDate is None or endDate is None\
     or modulo is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  endTimestamp = endDate + modulo
  vhost_id = getVhostId(vhost)
  if vhost_id is None:
    return None, "vhost " + vhost + " not found"
  pipeline = [
    {'$match': \
      { "$and": \
        [{'vhost': vhost_id}, \
         {'timestamp': {"$gte" : startDate,\
                        "$lte" : endTimestamp}},\
         {'req_str': {"$not": re.compile("((\.jpg|\.jpeg|\.png|\.js|\.css|\.gif|\.ico)$)|((\.jpg|\.jpeg|\.png|\.js|\.css|\.gif|\.ico)\?.*$)", re.IGNORECASE)}}\
]\
      }\
    },
    {'$project': \
      {'dateLowerBound': \
        { "$subtract": \
          ['$timestamp',\
            {"$mod": [\
              {"$subtract": ['$timestamp', startDate]},\
            modulo]\
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

def getLastVisitorsList(vhost_id = None, count = None):

  if vhost_id is None or count is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  pipeline = [
    {'$match': {'vhost': vhost_id}},
    {'$project': {'_id':0, 'remote_host': 1, 'maxVal': {'val': "$timestamp"}, 'lastUa': {'ua': "$user_agent"}}},
    {'$group':
      {'_id':{"remote_host": "$remote_host"},\
       'count': {"$sum": 1},\
        'maxTs': {"$max":"$maxVal"},
        'lastUa': {"$last": "$lastUa"}
      }\
    },\
    {'$project': {'_id':0,"remote_host":"$_id.remote_host", \
                  "count": "$count", \
                  "timestamp": "$maxTs.val", \
                  "user_agent": "$lastUa.ua"}},
    {'$sort': {'timestamp': -1}},\
    {'$limit': count}
  ]


  q = db.command('aggregate', config.aplogCollection, pipeline=pipeline)
  #print "pipeline is ::::", pipeline, "\n^^^^^^^^^^^^^^^\n"
  #workerLogger.debug("mongoDriver resp::" + str(q))
  #print "result is ::::", q, "\n^^^^^^^^^^^^^^^\n"
  
  return q["result"], ""


def getLastVisitorInfo(vhost_id = None, remote_host = None):

  if vhost_id is None or remote_host is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  pipeline = [
    {'$match':
      { '$and':[
        {'vhost': vhost_id},
        {'remote_host': remote_host}
      ]} 
    },
    {'$sort': {'timestamp': -1}},\
    {'$limit': 1},\
    {'$project': {'user_agent': 1, 'timestamp': 1}}
  ]

  q = db.command('aggregate', config.aplogCollection, pipeline=pipeline)
  #print "pipeline is ::::", pipeline, "\n^^^^^^^^^^^^^^^\n"
  #print "result is ::::", q, "\n^^^^^^^^^^^^^^^\n"
  #workerLogger.debug("mongoDriver resp::" + str(q))
  return q["result"], ""

def getLastVisitorsRawList(vhost_id = None, count = None):

  if vhost_id is None or count is None:
    workerLogger.error("Invalid input parameters")
    return None, "Invalid input params"

  pipeline = [
    {'$match':
      { '$and':[
        {'vhost': vhost_id},
        {'resp_code': {'$ne': 404}}
      ]} 
    },
    {'$sort': {'timestamp': -1}},\
    {'$project': 
      {'remote_host': 1, \
       'timestamp'  : 1, \
       'req_str'    : 1, \
       'referrer'   : 1, \
       'user_agent' : 1 \
      }
    },
    {'$limit': count}
  ]

  q = db.command('aggregate', config.aplogCollection, pipeline=pipeline)
  #workerLogger.debug("mongoDriver resp::" + str(q))
  #print "pipeline is ::::", pipeline, "\n^^^^^^^^^^^^^^^\n"
  #print "result is ::::", q, "\n^^^^^^^^^^^^^^^\n"
  
  return q["result"], ""


