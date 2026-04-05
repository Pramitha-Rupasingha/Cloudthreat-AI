import pandas as pd
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import numpy as np

def load_and_engineer(filepath='logs/raw_logs.json'):
    with open(filepath) as f:
        events = json.load(f)
    
    df = pd.DataFrame(events)
    
    le = LabelEncoder()
    df['eventName_enc'] = le.fit_transform(df['eventName'])
    df['sourceIP_enc'] = le.fit_transform(df['sourceIP'])
    df['has_error'] = df['errorCode'].notna().astype(int)
    df['hour'] = pd.to_datetime(df['eventTime']).dt.hour
    df['unusual_hour'] = ((df['hour'] < 8) | (df['hour'] > 18)).astype(int)
    
    return df

def detect_anomalies(df):
    features = ['eventName_enc', 'sourceIP_enc', 'has_error', 'unusual_hour']
    X = df[features]
    
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    
    df['anomaly_score'] = model.fit_predict(X)
    df['score_raw'] = model.score_samples(X)
    
    threats = df[df['anomaly_score'] == -1].copy()
    return threats, df

if __name__ == "__main__":
    df = load_and_engineer()
    threats, full_df = detect_anomalies(df)
    
    print(f"\n🚨 Threats detected: {len(threats)}")
    if len(threats) > 0:
        print(threats[['eventTime', 'eventName', 'sourceIP', 'userName', 'score_raw']].to_string())
    
    threats.to_json('alerts/threats.json', orient='records', indent=2)
    print("\n✅ Saved to alerts/threats.json")
