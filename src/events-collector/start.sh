#!/bin/bash
echo "collecting interaction data"
tail -f -n1 /var/log/nginx/access_collect.log | python3 events_collector.py
