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
        myprint("data: " + request.data)

        if request.content_type == "application/octet-stream":
            pass
        else:
            return apiHelper.badRequest(code = 101, detail = "Invalid content-type " + str(request.content_type))
        
        resp = rc.ALL_OK
        resp['Content-Type'] = 'application/octet-stream'
        resp.content = "SAMPLE_RESPONSE"
        tcObj.debug("Stats handler success, response: " + str(resp))
        return resp

