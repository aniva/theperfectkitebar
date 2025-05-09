#!/usr/bin/env python3
"""
Cloud Function to disable public read access on a GCS bucket when a budget alert is received.
Triggered via Pub/Sub budget notification.
"""
import os
import base64
import json
from google.cloud import storage
from google.api_core.exceptions import PreconditionFailed, GoogleAPIError

def disable_bucket_public_access(event, context):
    """
    Pub/Sub-triggered Cloud Function.
    Expects a JSON payload (base64-encoded) with fields:
      - budgetDisplayName
      - alertThresholdExceeded (bool)
    Disables 'allUsers' objectViewer binding only when the named budget exceeded its threshold.
    Includes detailed logging of incoming event and payload for debugging.
    """
    # Environment variables
    bucket_name = os.environ.get('BUCKET_NAME')
    budget_name = os.environ.get('BUDGET_DISPLAY_NAME')
    print(f"👷 Received disable_bucket_public_access invocation")
    print(f"🔧 Configured bucket: {bucket_name}")
    print(f"🔧 Configured budget name: {budget_name}")
    if not bucket_name or not budget_name:
        print("❌ BUCKET_NAME or BUDGET_DISPLAY_NAME not set in environment.")
        return ('Missing environment variable', 500)

    # Log full event for debugging
    print(f"📨 Raw event payload: {event}")

    # Decode and parse the Pub/Sub message data
    data_b64 = event.get('data')
    if not data_b64:
        print("⚠️ No data in event payload.")
        return ('No data', 400)

    try:
        decoded = base64.b64decode(data_b64).decode('utf-8')
        payload = json.loads(decoded)
        print(f"🔓 Decoded payload JSON: {json.dumps(payload, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to decode/parse payload: {e}")
        return ('Bad payload', 400)

    incoming_budget = payload.get('budgetDisplayName')
    exceeded = payload.get('alertThresholdExceeded', False)
    print(f"🏷 Incoming budgetDisplayName: {incoming_budget}")
    print(f"⚠️ alertThresholdExceeded: {exceeded}")

    # Only act on the configured budget name and when exceeded
    if incoming_budget != budget_name:
        print(f"ℹ️ Ignoring alert for budget '{incoming_budget}'. Expected '{budget_name}'.")
        return ('Ignored wrong budget', 200)
    if not exceeded:
        print("ℹ️ Threshold not exceeded; no action taken.")
        return ('Threshold not exceeded', 200)

    print(f"🚀 Revoking 'allUsers' access to bucket: {bucket_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Helper to remove allUsers from policy bindings
    def remove_all_users(policy):
        new_bindings = []
        for binding in policy.bindings:
            print(f"🔍 Inspecting binding: {binding['role']} -> members: {binding['members']}")
            if binding['role'] == 'roles/storage.objectViewer':
                if 'allUsers' in binding['members']:
                    binding['members'].remove('allUsers')
                    print("➖ Removed 'allUsers' from objectViewer binding")
                else:
                    print("✅ 'allUsers' not present; nothing to remove.")
                if binding['members']:
                    new_bindings.append(binding)
                else:
                    print("ℹ️ Binding now empty; removed completely.")
            else:
                new_bindings.append(binding)
        return new_bindings

    # Retry logic for IAM preconditions
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            policy = bucket.get_iam_policy(requested_policy_version=3)
            print(f"🔐 Fetched IAM policy: {policy.bindings}")
            policy.bindings = remove_all_users(policy)
            bucket.set_iam_policy(policy)
            print("✅ Public access removed successfully.")
            return ('Public access disabled', 200)
        except PreconditionFailed as e:
            print(f"⚠️ PreconditionFailed on attempt {attempt}: {e}")
            continue
        except GoogleAPIError as e:
            print(f"❌ Google API error during IAM update: {e}")
            return ('Google API error', 500)

    print(f"❌ Failed to update IAM policy after {max_attempts} attempts.")
    return ('IAM update failed', 500)
