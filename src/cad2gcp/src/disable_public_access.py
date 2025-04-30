import os
from google.cloud import storage

def disable_bucket_public_access(event, context):
    bucket_name = os.environ["BUCKET_NAME"]
    print(f"Revoking 'allUsers' access to bucket: {bucket_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings = [
        binding for binding in policy.bindings
        if not (binding["role"] == "roles/storage.objectViewer" and "allUsers" in binding["members"])
    ]

    bucket.set_iam_policy(policy)

    print("Public access removed successfully.")
