from piston.handler import BaseHandler
import json
from piston.utils import rc
from google.protobuf.message import DecodeError
import log_analytics_proto
from src.api.v1.settings import apiLogger
import apiHelper
import traceback
# import worker classes/functions
from src.utils import utils
from src.utils import threadCache

class StatsHandler( BaseHandler ):
        
    def read(self, request):
        apiLogger.debug("Begin stats get handler")
        tcObj = apiHelper.init(webSessionId = "NA", userName = "NA")
        print "data: ", request.data

        if request.content_type == "application/octet-stream":
            pass
        else:
            return apiHelper.badRequest(code = 101, detail = "Invalid content-type " + str(request.content_type))
        
        resp = rc.ALL_OK
        resp['Content-Type'] = 'application/octet-stream'
        resp.content = "SAMPLE_RESPONSE"
        tcObj.debug("Stats handler success, response: " + str(resp))
        return resp
    
    def create(self, request):
      return apiHelper.badRequest(code = 201, detail = "POST method not allowed")

    def update(self, request):
      return apiHelper.badREquest(code = 301, detail = "PUT method not allowed")

    def delete(self, request):
      return apiHelper.badREquest(code = 401, detail = "DELETE method not allowed")

