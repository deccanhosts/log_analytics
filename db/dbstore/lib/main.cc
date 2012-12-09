#include <iostream>
#include <string>
#include "dbdriver/constants.h"
#include "dbdriver/dbdriver.h"

using namespace dbdriver;
int main()
{
  std::string input_line;
  DbDriver *db_driver = new DbDriver(); 
  while(std::cin) {
    getline(std::cin, input_line);
    if (input_line.size() == 0) continue;
    if (DB_FAILURE == db_driver->insert((const std::string &)input_line) ){
      std::cerr << "Failed to insert record: " << input_line << std::endl;
    }
  };
  delete db_driver;
  return EXIT_SUCCESS;
}

