import os
from google.cloud import storage

def enable_bucket_public_access(request):
    bucket_name = os.environ["BUCKET_NAME"]
    print(f"Granting 'allUsers' access to bucket: {bucket_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({
        "role": "roles/storage.objectViewer",
        "members": {"allUsers"},
    })

    bucket.set_iam_policy(policy)

    print("Public access granted successfully.")
    return "Public access granted.", 200
