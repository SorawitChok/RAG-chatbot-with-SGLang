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

import app.auth as auth
from fastapi import APIRouter, Depends, status
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
import re

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain_community.embeddings import SentenceTransformerEmbeddings
import pandas as pd

router = APIRouter(dependencies=[Depends(auth.validate_api_key)])
client = chromadb.HttpClient(
    host="chromaDB",
    port=8000,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/stsb-xlm-r-multilingual"
)

openai_client = OpenAI(
    base_url="http://sglang:30000/v1",
    api_key="None",
)


@router.post("/api/v1/upload_csv")
def upload_csv(file: UploadFile = File(...)):
    old_name = file.filename
    contents = file.file.read()
    with open(f"./file/" + old_name, "wb") as f:
        f.write(contents)
    return {"file_name": file.filename}


@router.post("/api/v2/upload_csv")
def embed_QA_from_csv(
    collection_name: str, tag: str = None, file: UploadFile = File(...)
):
    collections = client.list_collections()
    if collection_name not in collections:
        old_name = file.filename
        contents = file.file.read()
        with open(f"./file/" + old_name, "wb") as f:
            f.write(contents)
        df = pd.read_csv(f"./file/{old_name}")
        all_df = df.dropna()
        Q_list = all_df["question"].array.tolist()
        A_list = all_df["answer"].array.tolist()
        if tag:
            Q_list = [f"<{tag}>" + q for q in Q_list]
            print(Q_list)
        collection = client.get_or_create_collection(
            collection_name,
            embedding_function=sentence_transformer_ef,
            metadata={"hnsw:space": "cosine"},
        )
        collection.add(
            documents=Q_list,
            metadatas=[{"ans": f"{elem}"} for elem in A_list],
            ids=[f"{collection_name}_{idx + 1}" for idx in range(len(all_df.index))],
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"Successfully create collection named {collection_name}.",
        }
    else:
        response = {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": f"The collection named {collection_name} is already existed.",
        }
    json_response = jsonable_encoder(response)
    return JSONResponse(content=json_response)


@router.get("/api/v1/check_collections")
def check_all_collection():
    collections = client.list_collections()
    response = {
        "status_code": status.HTTP_200_OK,
        "detail": "Success",
        "collections": collections,
    }
    json_response = jsonable_encoder(response)
    return JSONResponse(content=json_response)


@router.post("/api/v1/delete_collection")
def delete_collection(collection_name: str):
    collections = client.list_collections()
    if collection_name in collections:
        client.delete_collection(name=collection_name)
        response = {
            "status_code": status.HTTP_200_OK,
            "detail": "Success",
            "deleted_collection": collection_name,
        }
    else:
        response = {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": f"Collection named {collection_name} not found",
        }
    json_response = jsonable_encoder(response)
    return JSONResponse(content=json_response)
