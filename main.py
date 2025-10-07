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

from fastapi import (
    FastAPI,
    __version__,
    Request,
    Response,
    Depends,
    HTTPException,
    status,
    Security,
)
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Depends, File
from langchain_community.embeddings import SentenceTransformerEmbeddings
from fastapi.middleware.cors import CORSMiddleware

from app.prompt import *
from app.model import *
from app.retriever import *
from openai import OpenAI

# import uvicorn
import os
import app.route as route


TEMP_KEY = ["ADMIN_API_KEY"]

api_key_header = APIKeyHeader(name="API_KEY")

# Using SeaLLMs
client = OpenAI(
    base_url="http://sglang:30000/v1",
    api_key="None",
)

sentence_transformer_ef = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/stsb-xlm-r-multilingual"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route.router)


@app.get("/")
async def root():
    """
    Handler for the root endpoint.

    Returns:
        HTMLResponse: The HTML response containing a basic page with links.
    """
    html = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>FastAPI</title>
                </head>
                <body>
                    <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
                        <h1>Hello from FastAPI@{__version__}</h1>
                        <ul>
                            <li><a href="/docs">/docs</a></li>
                            <li><a href="/redoc">/redoc</a></li>
                        </ul>
                        <p>Created by <a href="https://github.com/SorawitChok">Sorawit Chokphantavee</a></p>
                    </div>
                </body>
            </html>
            """
    return HTMLResponse(html)


@app.post("/generate")
def generate_response(
    payload: PayloadModel, api_key_header: str = Security(api_key_header)
):
    if api_key_header not in TEMP_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorize Access: invalid API key",
        )
    else:
        if payload.prompt.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request: missing or invalid input format",
            )
        if payload.sampling_param:
            params = payload.sampling_param.dict()  # Using SeaLLMs
        else:
            params = {"top_p": 0.9, "max_tokens": 512, "temperature": 0.7}
        tagged_prompt = f"<{payload.agent_setting.organization}>" + payload.prompt
        instruction, context = retrieve_context_chroma(
            payload.db_name,
            tagged_prompt,
            sentence_transformer_ef,
            payload.mode,
            payload.agent_setting,
        )
        conversations = conversation_generation(payload.prompt, context, instruction)
        completion = client.chat.completions.create(
            model="SorawitChok/SeaLLM3-7B-Chat-AWQ",  # SeaLLMs
            messages=conversations,
            **params,
        )

        final_outputs = completion.choices[0].message
        final_outputs_text = final_outputs.content

        # For demo phase: Add Disclaimer
        if payload.agent_setting.disclaimer:
            final_outputs_text += "\n\n Disclaimer: ระบบ Chatbot นี้อยู่ในระหว่างการพัฒนาและเป็นรุ่นทดลองเพื่อสาธิตการทำงาน อาจมีความไม่สมบูรณ์ของข้อมูลหรือข้อผิดพลาดในการตอบคำถาม รวมถึงข้อจำกัดในฟังก์ชันการทำงาน โปรดหลีกเลี่ยงการใช้ข้อมูลจากระบบนี้เป็นข้อมูลหลักในการตัดสินใจสำคัญ ระบบนี้ไม่ได้ให้คำแนะนำทางกฎหมาย การเงิน หรือวิชาชีพ และผู้ใช้งานไม่ควรป้อนข้อมูลส่วนตัวที่เป็นความลับ การใช้งานระบบถือว่าผู้ใช้ยอมรับข้อจำกัดนี้และเข้าใจวัตถุประสงค์เพื่อการทดลองและพัฒนาเท่านั้น"

        response = {
            "status_code": status.HTTP_200_OK,
            "detail": "Success",
            "context": context,
            "output": final_outputs_text,
        }
        json_response = jsonable_encoder(response)
    return JSONResponse(content=json_response)
