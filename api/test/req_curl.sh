#!/bin/bash
curl -i -H "Accept: application/json" -H "Content-type: application/octet-stream" -X GET --data-binary @tmp_get_test.txt localhost:8086/api/v1/stats/ -vvv

