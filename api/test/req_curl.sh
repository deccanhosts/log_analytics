#!/bin/bash
curl -i -H "Accept: application/json" -H "Content-type: application/octet-stream" -X GET localhost:8086/api/v1/stats/?req=`cat tmp_get_test.txt` -vvv

