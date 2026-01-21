import requests
import pandas as pd
import json

API_BASE = "https://builder-api-875175326233.us-central1.run.app/builder-api"
API_KEY = "bapi_sk_c8f9a2b7e4d1c5a3f6b9d2e7a1c4b8f5"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("=== API TEST ===\n")

# Test CRM API - Builder A
print("Testing CRM API - Builder A...")
try:
    response = requests.get(f"{API_BASE}/crm?builder=a", headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response type: {type(data)}")
        print(f"Sample (first 500 chars):\n{json.dumps(data, indent=2)[:500]}\n")
        
        # Try to make dataframe
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.DataFrame([data])
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 3 rows:\n{df.head(3)}\n")
        df.to_csv('01_Data_Analytics/02A_api_crm_builder.csv', index=False)
        print("✓ Saved to 01_Data_Analytics/02A_api_crm_builder.csv\n")
    else:
        print(f"Error: {response.text}\n")
except Exception as e:
    print(f"Exception: {e}\n")

# Test CRM API - Builder B
print("Testing CRM API - Builder B...")
try:
    response = requests.get(f"{API_BASE}/crm?builder=b", headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.DataFrame([data])
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        df.to_csv('01_Data_Analytics/02B_api_crm_builder.csv', index=False)
        print("✓ Saved to 01_Data_Analytics/02B_api_crm_builder.csv\n")
    else:
        print(f"Error: {response.text}\n")
except Exception as e:
    print(f"Exception: {e}\n")

# Test Web Traffic API - Builder A
print("Testing Web Traffic API - Builder A...")
try:
    response = requests.get(f"{API_BASE}/web-traffic?builder=a", headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.DataFrame([data])
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 3 rows:\n{df.head(3)}\n")
        df.to_csv('01_Data_Analytics/02A_api_traffic_builder.csv', index=False)
        print("✓ Saved to 02A_api_traffic_builder.csv\n")
    else:
        print(f"Error: {response.text}\n")
except Exception as e:
    print(f"Exception: {e}\n")

# Test Web Traffic API - Builder B
print("Testing Web Traffic API - Builder B...")
try:
    response = requests.get(f"{API_BASE}/web-traffic?builder=b", headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        else:
            df = pd.DataFrame([data])
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        df.to_csv('01_Data_Analytics/02B_api_traffic_builder.csv', index=False)
        print("✓ Saved to 01_Data_Analytics/02B_api_traffic_builder.csv\n")
    else:
        print(f"Error: {response.text}\n")
except Exception as e:
    print(f"Exception: {e}\n")

print("=== API TEST COMPLETE ===")