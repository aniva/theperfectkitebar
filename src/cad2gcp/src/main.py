#!/usr/bin/env python3
import os, base64, json
from google.api_core.exceptions import PreconditionFailed, GoogleAPIError
from google.cloud import storage

# bring in your real handler and its prints
import disable_public_access as disable_mod  
import enable_public_access as enable_mod

# cold-start banner
print("⚡️ main.py loaded – dispatching to handlers ⚡️", flush=True)

def disable_bucket_public_access(event, context):
    print("🚧 [v2] dispatching to disable_mod.disable_bucket_public_access 🚧", flush=True)
    return disable_mod.disable_bucket_public_access(event, context)

def enable_bucket_public_access(request):
    print("🚧 [v2] dispatching to enable_mod.enable_bucket_public_access 🚧", flush=True)
    return enable_mod.enable_bucket_public_access(request)
