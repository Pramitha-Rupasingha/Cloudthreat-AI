import json
from log_fetcher import fetch_cloudtrail_events
from threat_detector import load_and_engineer, detect_anomalies

print("🔍 Fetching AWS CloudTrail logs...")
events = fetch_cloudtrail_events(hours=24)
with open('logs/raw_logs.json', 'w') as f:
    json.dump(events, f, indent=2)
print(f"✅ Fetched {len(events)} events")

print("\n🤖 Running ML anomaly detection...")
df = load_and_engineer()
threats, full_df = detect_anomalies(df)
threats.to_json('alerts/threats.json', orient='records', indent=2)

print(f"\n🚨 Threats detected: {len(threats)}")
if len(threats) > 0:
    print(threats[['eventTime', 'eventName', 'sourceIP', 'userName']].to_string())
else:
    print("✅ No threats found!")

print("\n✅ CloudThreat AI scan complete!")
