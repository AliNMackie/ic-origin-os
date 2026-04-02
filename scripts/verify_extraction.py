import os
import requests
from google.cloud import bigquery
from google.auth import default
from dotenv import load_dotenv

# Load .env file and override existing env vars
load_dotenv(override=True)

def verify():
    print("--- IC Origin Extraction Verification ---")
    
    # 1. Check Companies House API Key
    ch_api_key = os.environ.get("CH_API_KEY")
    if not ch_api_key:
        print("❌ CH_API_KEY is NOT set in environment.")
    else:
        print("✅ CH_API_KEY is set.")
        # Dry-run Companies House (Seasalt)
        crn = "02259954"
        url = f"https://api.company-information.service.gov.uk/company/{crn}"
        try:
            resp = requests.get(url, auth=(ch_api_key, ''), timeout=10)
            if resp.status_code == 200:
                print(f"✅ Companies House connection successful (Retrieved {resp.json().get('company_name')})")
            else:
                print(f"❌ Companies House connection failed with status {resp.status_code}")
        except Exception as e:
            print(f"❌ Companies House connection error: {e}")

    # 2. Check BigQuery Identity and Connection
    try:
        credentials, project = default()
        client = bigquery.Client()
        
        # Check Identity
        service_account_email = getattr(credentials, 'service_account_email', 'User Account')
        print(f"📡 Current Google Identity: {service_account_email}")
        
        expected_email = "sentinel-growth-sa@cofound-agents-os-788e.iam.gserviceaccount.com"
        if service_account_email == expected_email:
            print(f"✅ Identity matches the required sentinel-growth-sa account.")
        else:
            print(f"❌ Identity MISMATCH. Expected: {expected_email}")

        # Try to access ic_origin_themav2
        dataset_id = "ic_origin_themav2"
        full_dataset_id = f"{project}.{dataset_id}"
        try:
            dataset = client.get_dataset(full_dataset_id)
            print(f"✅ Successfully connected to BigQuery dataset: {full_dataset_id}")
        except Exception as e:
            print(f"❌ BigQuery connectivity failure to {full_dataset_id}: {e}")

    except Exception as e:
        print(f"❌ Google Cloud authentication error: {e}")

if __name__ == "__main__":
    verify()
