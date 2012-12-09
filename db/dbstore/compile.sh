#!/bin/bash
g++ lib/main.cc lib/dbdriver.cc -I include/ -pthread -lmongoclient -lboost_thread-mt -lboost_filesystem -lboost_program_options -lboost_system -o dbstore
