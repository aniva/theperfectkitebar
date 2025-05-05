#!/usr/bin/env python3
"""
Cloud Function to disable public read access on a GCS bucket when a budget alert is received.
Triggered via Pub/Sub budget notification.
"""
import os
import base64
import json
from google.cloud import storage

def disable_bucket_public_access(event, context):
    """
    Pub/Sub-triggered Cloud Function.
    Expects a JSON payload (base64-encoded) with fields:
      - budgetDisplayName
      - alertThresholdExceeded (bool)
    Disables 'allUsers' objectViewer binding only when the named budget exceeded its threshold.
    """
    # Environment variables
    bucket_name = os.environ.get('BUCKET_NAME')
    budget_name = os.environ.get('BUDGET_DISPLAY_NAME')
    if not bucket_name or not budget_name:
        print("❌ BUCKET_NAME or BUDGET_DISPLAY_NAME not set in environment.")
        return ('Missing environment variable', 500)

    # Decode and parse the Pub/Sub message data
    if 'data' not in event:
        print("⚠️ No data in event payload.")
        return ('No data', 400)

    payload = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    incoming_budget = payload.get('budgetDisplayName')
    exceeded = payload.get('alertThresholdExceeded', False)

    # Only act on the configured budget name
    if incoming_budget != budget_name:
        print(f"ℹ️ Ignoring alert for budget '{incoming_budget}' (looking for '{budget_name}').")
        return ('Ignored wrong budget', 200)

    # Only disable when threshold truly exceeded
    if not exceeded:
        print("ℹ️ AlertThresholdExceeded is false; no action taken.")
        return ('Threshold not exceeded', 200)

    print(f"🚀 Revoking 'allUsers' access to bucket: {bucket_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)

    # Remove 'allUsers' from objectViewer binding
    new_bindings = []
    for binding in policy.bindings:
        if binding['role'] == 'roles/storage.objectViewer':
            if 'allUsers' in binding['members']:
                binding['members'].remove('allUsers')
                print("➖ Removed 'allUsers' from objectViewer binding")
            else:
                print("✅ 'allUsers' not present; nothing to remove.")
            # Only keep the binding if other members remain
            if binding['members']:
                new_bindings.append(binding)
            else:
                print("ℹ️ Binding now empty; removed entirely.")
        else:
            new_bindings.append(binding)

    policy.bindings = new_bindings
    bucket.set_iam_policy(policy)
    print("✅ Public access removed successfully.")
    return ('Public access disabled', 200)
