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
import base64

class StatsHandler( BaseHandler ):
        
    def read(self, request):
        apiLogger.debug("Begin stats get handler")

        if request.content_type == "application/octet-stream":
            pass
        else:
            return apiHelper.badRequest(code = 101, detail = "Invalid content-type " + str(request.content_type))

        req_enc_str = request.GET.get('req', '')
        request_data = base64.b64decode(req_enc_str)
        req_obj = log_analytics_proto.req_msg() 
        try:
          req_obj.ParseFromString(request_data)
        except DecodeError, e:
            return apiHelper.badRequest(code = 102, detail = "Failed to decode protobuf. " + e)
        
        if req_obj.req_id is None or \
           req_obj.req_type is None:
            return apiHelper.badRequest(code = 103, detail = "Null value specified for REQUIRED fields")

        tcObj = apiHelper.init(reqId = req_obj.req_id)
        req_id = req_obj.req_id
  
        if req_obj.req_type == 1:
        
          # default scale is 2 - daily
          req_payload = log_analytics_proto.req_payload_struct()
          try:
            req_payload = req_obj.req_payload
          except DecodeError, e:
            return apiHelper.badRequest(code = 104, detail = "Failed to decode protobuf. " + e)
            
          scale = req_payload.scale if req_payload.scale is not None else 2
          hostname = req_payload.hostname
          time_from = req_payload.time_from
         
        # default time_to is current time 
          time_to = req_payload.time_to if req_payload.time_to is not None else apiHelper.getCurrentTime()
          retval, err_msg = utils.validateInput(hostname  = hostname, \
                                              scale     = scale, \
                                              time_from = time_from, \
                                              time_to   = time_to)

          if retval is False:
            return apiHelper.badRequest(code = 105, detail = err_msg)
        
        #resp_dict, retval, err_msg = getResponse(hostname = hostname, scale = scale, time_from = time_from, time_to = time_to)
        #if retval is False:
        #  return apiHelper.badRequest(code = 105, detail = err_msg)
          resp_dict = {}
          resp_dict = apiHelper.getTestRespDict()
          resp_obj, retval, err_msg = apiHelper.constructRespObj(resp_dict = resp_dict,
                                                             req_id = req_id)
          if retval is False:
            return apiHelper.badRequest(code = 106, detail = err_msg)

        else if req_obj.req_type == 2:
          return apiHelper.badRequest(code = 107, detail = "Not yet implemented!!")
        else:
          return apiHelper.badRequest(code = 108, detail = "Invalid request type!!")

        resp = rc.ALL_OK
        resp['Content-Type'] = 'application/octet-stream'
        resp.content = resp_obj.SerializeToString()
        return resp
    
    def create(self, request):
      return apiHelper.badRequest(code = 201, detail = "POST method not allowed")

    def update(self, request):
      return apiHelper.badRequest(code = 301, detail = "PUT method not allowed")

    def delete(self, request):
      return apiHelper.badRequest(code = 401, detail = "DELETE method not allowed")

