#!/usr/bin/env python3
import os
import base64
import json
import disable_public_access as disable_mod  
import enable_public_access as enable_mod

# cold-start banner
print("⚡️ main.py loaded – dispatching to handlers ⚡️", flush=True)

def disable_bucket_public_access(cloud_event):
    print("🚧 [v2] dispatching to disable_mod.disable_bucket_public_access 🚧", flush=True)
    return disable_mod.disable_bucket_public_access(cloud_event)

def enable_bucket_public_access(request):
    print("🚧 [v2] dispatching to enable_mod.enable_bucket_public_access 🚧", flush=True)
    return enable_mod.enable_bucket_public_access(request)
