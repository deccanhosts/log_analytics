db
==

db and its driver for fetching/storing log data

Installing Mongodb, mongo C++ driver and dbstore binary
1. Install mongodb: sudo apt-get install mongodb
2. Install scons: sudo apt-get install scons
3. Download the driver from  http://downloads.mongodb.org/cxx-driver/mongodb-linux-x86_64-2.3.0.tgz  and extract. Install using command scons
4. Install boost libraries: sudo apt-get install libboost-thread-dev g++ libboost-filesystem-dev libboost-program-options-dev
5. Build the dbstore library: cd log_analytics/db/dbstore/ ; ./compile.sh

