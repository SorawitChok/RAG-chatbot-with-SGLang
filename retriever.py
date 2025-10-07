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

import pandas as pd
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import re
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from app.vectorDB import query_QA


def retrieve_context_chroma(
    collection_name, inp_prompt, sentence_transformer_ef, mode, agent_setting
):
    client = chromadb.HttpClient(
        host="chromaDB",
        port=8000,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )

    docs = query_QA(client, collection_name, sentence_transformer_ef, inp_prompt, 3)

    instruction = f"""คุณมีชื่อว่า {agent_setting.agent_name} เป็นระบบช่วยตอบคำถามอัจฉริยะสำหรับตอบคำถามเกี่ยวกับข้อมูลต่างๆของ {agent_setting.organization}
ตอบคำถามอย่างถูกต้อง ครบถ้วน สุภาพ และ เป็นธรรมชาติ และต้องใช้คำลงท้ายประโยคทุกประโยคด้วยคำว่า {agent_setting.persona}
โปรดใช้เฉพาะข้อมูลที่ได้จากข้อมูลที่เรียกคืน ห้ามสร้างข้อมูลเอง 
"""

    context = """{}"""
    questions = []
    answers = []
    for doc in docs:
        if doc[1] >= 0.7:
            question = doc[0].page_content
            questions.append(question)

            answer = doc[0].metadata["ans"]
            answers.append(answer)
    con_text = "ข้อมูลที่เรียกคืน: \n"
    if questions != []:
        for a, q in zip(answers, questions):
            con_text += q + "\n"
            con_text += a
            con_text += "\n\n"
    else:
        if mode == "strict":
            con_text = f"ขอโทษด้วย{agent_setting.persona} ไม่สามารถตอบคำถามนี้ได้ ท่านสามารถสอบถามเพิ่มเติมได้ทาง โทรศัพท์ โทร {agent_setting.tel}"
        else:
            con_text = f"หากท่านมีคำถามเพิ่มเติม สามารถสอบถามเพิ่มเติมได้ทาง โทรศัพท์ โทร {agent_setting.tel}"

    context = context.format(con_text)

    return instruction, context
