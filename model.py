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

from pydantic import BaseModel
from typing import Optional


class SamplingParamsModel(BaseModel):
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    seed: Optional[int] = None


class AgentSetting(BaseModel):
    agent_name: str
    persona: str
    organization: str
    tel: str
    disclaimer: Optional[bool] = False


class PayloadModel(BaseModel):
    prompt: str
    db_name: str
    sampling_param: Optional[SamplingParamsModel] = None
    agent_setting: AgentSetting
    mode: str = "strict"
