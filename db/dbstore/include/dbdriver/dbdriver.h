#ifndef DBDRIVER_H
#define DBDRIVER_H
#include <string>
#include "constants.h"

namespace dbdriver {

class DbDriverImpl;
class DbDriver {

  private:
    DbDriver(const DbDriver & dbdriver); //prevent copy constructor
  public:
    DbDriver();
    ~DbDriver();
    DbDriverImpl *_impl;
    status_t insert(const std::string & input_line);
  
};

};

#endif // DBDRIVER_H

