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


def conversation_generation(prompt: str, context: str, sys_prompt: str = None):
    context_template = f"""
    ตอบคำถามของผู้ใช้โดยใช้ข้อมูลเหล่านี้เท่านั้น:
    {context}
    คำถามของผู้ใช้คือ: {prompt}
    คำตอบ:
    """
    conversations = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": context_template},
    ]

    return conversations
