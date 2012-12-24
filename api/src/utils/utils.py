# this file provides generic api's for validation of various user inputs
import re
#domain '-' allowed but not double or more continuosly, '.' also allowed , both
# (-, .) not in the begining or end
domain_re = "^[0-9a-zA-Z]+((-[0-9a-zA-Z]+)*(\.[0-9a-zA-Z]+)*)*(\.[0-9a-zA-Z]+)+$"
domain_regex = None

MAX_EPOCH_TIME = 32535215999 # epoch time for 12/31/3000
MAX_DOMAIN_LEN = 512 

def validateDomain(domain, field_name = None):
    global domain_regex
    global domain_re

    retval = True
    msg = ""

    if field_name is None or len(field_name) == 0:
        field_name = "hostname"

    if domain is None or len(domain) == 0:
        return True, str(field_name) + " is empty"

    if domain_regex is None:
        domain_regex = re.compile(domain_re)
        
    if domain_regex.match(domain) is None:
        retval = False
        msg = msg + str(field_name) + ": " + str(domain) + " is not valid !!. "
    if len(domain) > MAX_DOMAIN_LEN:
        retval = False
        msg = msg + str(field_name) + ": " + str(domain) + " length exceeds limit of " + str(MAX_DOMAIN_LEN) + ". "
    return retval, msg


def validateScale(scale = 2):
  if scale < 0 or scale > 6:
    return False, "Invalid value supplied for scale"
  return True, ""


def validateTime(time_val):
  if time_val < 0 or time_val > MAX_EPOCH_TIME:
    return False, "Invalid value supplied for time"
  return True, ""


def validateInput(hostname = "", scale = 2, time_from = 0, time_to = 0):
  
  msg = ""
  retval = True
  tmp_val, tmp_msg = validateDomain(hostname) 
  if tmp_val is False:
    retval = False
    msg = msg + tmp_msg
  
  tmp_val, tmp_msg = validateScale(scale) 
  if tmp_val is False:
    retval = False
    msg = msg + tmp_msg
    
  tmp_val, tmp_msg = validateTime(time_from) 
  if tmp_val is False:
    retval = False
    msg = msg + tmp_msg

  tmp_val, tmp_msg = validateTime(time_to) 
  if tmp_val is False or time_to < time_from:
    retval = False
    msg = msg + tmp_msg
  
  if time_from > time_to:
    retval = False
    msg = msg + "\ntime_from cannot be greater than time_to \n"

  return retval, msg


