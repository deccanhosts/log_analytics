#include "dbdriver/dbdriver.h"
#include "dbdriver/constants.h"
#include "mongo/client/dbclient.h"
#include <vector>
#include <string>
#include <cstdlib>
#include <sstream>
#include "mongo/db/jsobj.h"

#include <iostream>

namespace dbdriver {

status_t str2uint(const std::string & str, uint64_t & uintval);

const size_t LOG_FIELDS_COUNT = 8;

class DbDriverImpl {

  private:
    
    std::string _vhost;
    std::string _remote_host;
    uint64_t _timestamp;
    std::string _req_str;
    uint64_t _ret_code;
    uint64_t _resp_size;
    std::string _referrer;
    std::string _user_agent;
    
    mongo::DBClientConnection _conn;
    
    DbDriverImpl(const DbDriverImpl & dbdriver_impl); // prevent copy construction
    status_t _tokenize(const std::string & input_line, std::vector<std::string> & tokens);
    status_t _populate_fields(const std::vector<std::string> & tokens);
    status_t _insert_record_db();
     
    
    
  public:
    DbDriverImpl();
    ~DbDriverImpl();
    status_t insert(const std::string & input_line);
    
};


DbDriver::DbDriver():
                   _impl(new DbDriverImpl()) 
{

}


status_t DbDriver::insert(const std::string & input_line)
{
  return _impl->insert(input_line);
}


DbDriver::~DbDriver()
{
  if (_impl){
    delete _impl;
    _impl = NULL;
  }
}


DbDriverImpl::DbDriverImpl()
{
  _conn.connect(DB_HOST);
}


status_t DbDriverImpl::insert(const std::string & input_line)
{
  std::vector<std::string> tokens;
  std::vector<std::string>::iterator token_it;
  int i = 0;
  if (DB_SUCCESS != _tokenize(input_line, tokens)){
    std::cerr << "Error tokenizing input line" << std::endl;
    return DB_FAILURE;
  }
  for(token_it = tokens.begin(); token_it < tokens.end(); token_it++, i++){
  }
  if (DB_SUCCESS != _populate_fields(tokens)){
    std::cerr << "Error populating fields" << std::endl;
    return DB_FAILURE;
  }
  if (DB_SUCCESS != _insert_record_db()){
    std::cerr << "Error inserting record into database" << std::endl;
    return DB_FAILURE;
  }
  return DB_SUCCESS;
}


status_t DbDriverImpl::_tokenize(const std::string & input_line, std::vector<std::string> & tokens)
{  
  const char * separator = " ";
  char *tok = strtok((char *)input_line.c_str(), separator);
  bool begin = false;
  bool tok_complete = true;
  std::string tmp_tok;
  while(tok) {
    if(tok[0] == '"' && begin == false && tok[strlen(tok) - 1] != '"'){
      begin = true;
      //tmp_tok = tok;
      tmp_tok = tok + 1;
      tok_complete = false;
    }
    else if(begin == true){
      tmp_tok = tmp_tok + " " + tok;
      if(tok[strlen(tok) - 1] == '"'){
        tok_complete = true;
        begin = false;
      }
    }
    else {
      if (tok[0] == '"') {
        tmp_tok = tok + 1;
      }
      else {
        tmp_tok = tok;
      }
    }
    if(tok_complete){
      // to remove the trailing "
      if(tmp_tok[tmp_tok.size() - 1] == '"'){
        tmp_tok = tmp_tok.substr(0, tmp_tok.length() - 1);
      }
      tokens.push_back(tmp_tok); 
    }
    tok = strtok(NULL, " ");
  }
  return DB_SUCCESS;
}


status_t DbDriverImpl::_populate_fields(const std::vector<std::string> & tokens)
{

  if(tokens.size() != LOG_FIELDS_COUNT){
    std::cerr << "Invalid number of fields, expected " << LOG_FIELDS_COUNT << ", got " << tokens.size() << std::endl;
    return DB_FAILURE;
  }

  _vhost       = tokens[0];
  _remote_host = tokens[1];
  _req_str     = tokens[3];
  _referrer    = tokens[6];
  _user_agent  = tokens[7];
  if(str2uint(tokens[2], _timestamp) != DB_SUCCESS) {
    std::cerr << "Unable to parse timestamp from " << tokens[2] << std::endl;
  }
  if(str2uint(tokens[4], _ret_code) != DB_SUCCESS) {
    std::cerr << "Unable to parse return code from " << tokens[4] << std::endl;
  }
  if(str2uint(tokens[5], _resp_size) != DB_SUCCESS) {
    std::cerr << "Unable to parse response size from " << tokens[5] << std::endl;
  }
  
  return DB_SUCCESS;
}


status_t DbDriverImpl::_insert_record_db()
{
  mongo::BSONObjBuilder b;
  b.append("vhost", _vhost);
  b.append("remote_host", _remote_host);
  b.appendTimeT("timestamp", (time_t)_timestamp);
  b.append("req_str", _req_str);
  b.append("ret_code", (double)_ret_code);
  b.append("resp_size", (double)_resp_size);
  b.append("referrer", _referrer);
  b.append("user_agent", _user_agent);
  mongo::BSONObj p = b.obj();

  _conn.insert(DB_COLLECTION_NAME.c_str(), p);

  return DB_SUCCESS;
}

DbDriverImpl::~DbDriverImpl()
{

}

status_t str2uint(const std::string & str, uint64_t & uintval)
{
  uint64_t tmpval;
  char c;
  std::stringstream ss(str);
  ss >> tmpval;
  if(ss.fail() || ss.get(c)){
    return DB_FAILURE;
  }
  uintval = tmpval;
  return DB_SUCCESS;
}

};
