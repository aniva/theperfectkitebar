from google.cloud import storage

def disable_bucket_public_access(event, context):
    bucket_name = "theperfectkitebar-CAD-assets"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)

    new_bindings = [
        binding for binding in policy.bindings
        if "allUsers" not in binding["members"]
    ]
    policy.bindings = new_bindings
    bucket.set_iam_policy(policy)

    print(f"Public access removed from bucket {bucket_name}")
