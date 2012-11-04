#!/bin/bash
curl -i -H "Accept: application/json" -H "Content-type: application/octet-stream" -X POST --data-binary @sample_data.txt localhost:8086/api/v1/stats/ -vvv

