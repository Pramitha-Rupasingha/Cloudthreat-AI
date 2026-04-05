import boto3
import json
from datetime import datetime, timedelta

def fetch_cloudtrail_events(hours=24):
    client = boto3.client('cloudtrail', region_name='ap-southeast-1')
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    response = client.lookup_events(
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=100
    )
    
    events = []
    for event in response['Events']:
        cloud_event = json.loads(event['CloudTrailEvent'])
        events.append({
            'eventTime': event['EventTime'].isoformat(),
            'eventName': event['EventName'],
            'sourceIP': cloud_event.get('sourceIPAddress', 'unknown'),
            'userAgent': cloud_event.get('userAgent', 'unknown'),
            'userName': cloud_event.get('userIdentity', {}).get('userName', 'unknown'),
            'errorCode': cloud_event.get('errorCode', None),
            'region': cloud_event.get('awsRegion', 'unknown')
        })
    
    return events

if __name__ == "__main__":
    events = fetch_cloudtrail_events()
    print(f"Fetched {len(events)} events")
    with open('logs/raw_logs.json', 'w') as f:
        json.dump(events, f, indent=2)
    print("Saved to logs/raw_logs.json")
