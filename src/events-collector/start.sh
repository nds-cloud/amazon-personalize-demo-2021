#!/bin/bash
echo "starting_collecting..."
tail -f -n1 /var/log/nginx/access_collect.log | python3 events_collector.py
