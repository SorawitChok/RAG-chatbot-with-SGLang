"""
Copyright (c) 2024, FAQSure.  All rights reserved.

Authors: Sorawit Chokphantavee, Sirawit Chokphantavee & Somrudee Deepaisarn

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import api_key

TEMP_KEY = ["ADMIN_API_KEY"]

api_key_header = api_key.APIKeyHeader(name="API_KEY")


async def validate_api_key(key: str = Security(api_key_header)):
    if key not in TEMP_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorize Access: invalid API key",
        )
    return None
