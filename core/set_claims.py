import firebase_admin
from firebase_admin import auth, credentials
import sys

# 1. Load Credentials
try:
    # Looks for file in the same directory
    cred = credentials.Certificate('service-account.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"❌ Error: Could not load 'service-account.json'.")
    print(f"   Make sure you download it from Firebase and save it in this folder!\n")
    print(f"Details: {e}")
    sys.exit(1)

# 2. Configure target user account
email = "alastair@iapetusai.com"
tenant_id = "default"  # 👈 CHANGE THIS to isolate this client (e.g., "client-abc")
role = "ADMIN"         # Keeps you as Admin for that tenant

try:
    print(f"Searching for user: {email}...")
    user = auth.get_user_by_email(email)
    
    print(f"Assigning claims to UID: {user.uid}...")
    
    # 3. Apply Claims
    auth.set_custom_user_claims(user.uid, {
        "tenant_id": tenant_id,
        "role": role
    })
    
    print(f"\n✅ SUCCESS: Custom Claims assigned!")
    print(f"   - Tenant ID: '{tenant_id}'")
    print(f"   - Role:      '{role}'")
    print("\n⚠️ IMPORTANT: You MUST fully Sign Out of the Dashboard and Sign Back In to load the new token claims!")
    
except Exception as e:
    print(f"\n❌ Error assigning claims: {e}")
