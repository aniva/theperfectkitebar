#!/usr/bin/env python3
"""h
Cloud Function to re-enable public read access on a GCS bucket.
Called via HTTP trigger.
"""
import os
from google.cloud import storage


def enable_bucket_public_access(request):
    """
    HTTP Cloud Function entrypoint.
    Restores 'allUsers' objectViewer binding to the bucket.
    """
    bucket_name = os.environ.get('BUCKET_NAME')
    if not bucket_name:
        print("❌ BUCKET_NAME is not set in environment.")
        return ("Missing BUCKET_NAME environment variable", 500)

    print(f"🚀 Enabling public read access on bucket: {bucket_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)

    # Find existing objectViewer binding
    binding = next((b for b in policy.bindings if b['role'] == 'roles/storage.objectViewer'), None)
    if binding:
        if 'allUsers' not in binding['members']:
            binding['members'].append('allUsers')
            print("➕ Added 'allUsers' to existing objectViewer binding")
        else:
            print("✅ 'allUsers' already present in objectViewer binding")
    else:
        # Create new binding if none exists
        policy.bindings.append({
            'role': 'roles/storage.objectViewer',
            'members': ['allUsers']
        })
        print("➕ Created new objectViewer binding with 'allUsers'")

    # Apply updated IAM policy
    bucket.set_iam_policy(policy)
    print("✅ Public access restored successfully.")
    return ("Public access enabled", 200)
