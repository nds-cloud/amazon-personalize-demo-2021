#!/bin/python3
import re
import boto3
import datetime
import time

def main():
    trackingId = None
    pattern = re.compile('"GET /product/([^\.].+)\.html HTTP/1\.1" "([^"].+)"')
    while True:
        try:
            log = input()
            search = pattern.search(log)
            if search is not None:
                found = search.groups()
                if found is not None:
                    now = datetime.datetime.now()
                    print(f'%s,%s,%d' % (found[1], found[0], int(time.mktime(now.timetuple()))))
                    if trackingId:
                        client=boto3.client('personalize-events', 'ap-northeast-2')
                        response = client.put_events(
                            trackingId=trackingId,
                            userId=found[1],
                            sessionId=found[1],
                            eventList=[
                                {
                                    'eventType': 'click',
                                    'itemId': found[0],
                                    'sentAt': now
                                }
                            ]
                        )
        except EOFError:
            pass
        except KeyboardInterrupt:
            exit()
if __name__ == "__main__":
    main()
