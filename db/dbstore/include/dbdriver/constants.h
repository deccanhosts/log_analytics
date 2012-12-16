#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <inttypes.h>
#include <string>
namespace dbdriver {

typedef const uint64_t status_t;
const int EXIT_SUCCESS     = 0;
const int EXIT_FAILURE     = 1;

status_t DB_SUCCESS        = 0;
status_t DB_FAILURE        = 1;
const std::string DB_HOST  = "localhost";
const std::string DB_COLLECTION_NAME = "local.aplogs";
const std::string DB_UA_COLLECTION_NAME = "local.useragents";



};

#endif // CONSTANTS_H

