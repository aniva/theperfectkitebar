#!/usr/bin/env python3
import os, base64, json
from google.cloud import storage
from google.api_core.exceptions import PreconditionFailed, GoogleAPIError

# Module‐level banner — you'll see this once on cold start.
print("⚡️ disable_public_access.py v2 loaded ⚡️", flush=True)

def disable_bucket_public_access(event, context):
    # Function‐entry banner — you'll see this on every Pub/Sub trigger.
    print("🚧 [v2] disable_bucket_public_access invoked 🚧", flush=True)

    bucket_name = os.environ.get('BUCKET_NAME')
    budget_name = os.environ.get('BUDGET_DISPLAY_NAME')
    print(f"👷 Config: bucket={bucket_name}, budget={budget_name}", flush=True)

    if not bucket_name or not budget_name:
        print("❌ Missing BUCKET_NAME or BUDGET_DISPLAY_NAME", flush=True)
        return ('Missing env var', 500)

    print(f"📨 Raw event: {event}", flush=True)
    data_b64 = event.get('data')
    if not data_b64:
        print("⚠️  No data in Pub/Sub message", flush=True)
        return ('No data', 400)

    try:
        decoded = base64.b64decode(data_b64).decode()
        payload = json.loads(decoded)
        print("🔓 Payload:", json.dumps(payload, indent=2), flush=True)
    except Exception as e:
        print(f"❌ Payload parse error: {e}", flush=True)
        return ('Bad payload', 400)

    incoming = payload.get('budgetDisplayName')
    exceeded = payload.get('alertThresholdExceeded', False)
    print(f"🏷 budgetDisplayName: {incoming}", flush=True)
    print(f"⚠️  alertThresholdExceeded: {exceeded}", flush=True)

    if incoming != budget_name:
        print(f"ℹ️  Ignoring alert for `{incoming}`", flush=True)
        return ('Wrong budget', 200)
    if not exceeded:
        print("ℹ️  Threshold not exceeded", flush=True)
        return ('Not exceeded', 200)

    print(f"🚀 Revoking allUsers on {bucket_name}", flush=True)
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # remove-allUsers helper
    def remove_all_users(policy):
        new = []
        for b in policy.bindings:
            print(f"🔍 Binding: {b['role']} → {b['members']}", flush=True)
            if b['role']=='roles/storage.objectViewer' and 'allUsers' in b['members']:
                b['members'].remove('allUsers')
                print("➖ allUsers removed", flush=True)
            if b['members']:
                new.append(b)
        return new

    # retry loop
    for i in range(3):
        try:
            policy = bucket.get_iam_policy(requested_policy_version=3)
            print("🔐 Fetched policy", flush=True)
            policy.bindings = remove_all_users(policy)
            bucket.set_iam_policy(policy)
            print("✅ allUsers binding removed", flush=True)
            return ('Disabled', 200)
        except PreconditionFailed as e:
            print(f"⚠️  PreconditionFailed (attempt {i+1}): {e}", flush=True)
        except GoogleAPIError as e:
            print(f"❌ API error: {e}", flush=True)
            return ('API error', 500)

    print("❌ Failed to update IAM after 3 tries", flush=True)
    return ('Failed', 500)
