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
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
import shutil


def embed_QA(path: str, client, collection_name: str, sentence_transformer_ef):
    df = pd.read_csv(path)
    all_df = df.dropna()
    Q_list = all_df["question"].array.tolist()
    A_list = all_df["answer"].array.tolist()
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


def query_QA(
    client,
    collection_name: str,
    sentence_transformer_ef,
    query_str: str,
    num_similar: int,
):
    collections = client.list_collections()
    if collection_name in collections:
        chroma_db = Chroma(
            collection_name=collection_name,
            embedding_function=sentence_transformer_ef,
            client=client,
        )
        docs = chroma_db.similarity_search_with_relevance_scores(
            query_str, k=num_similar
        )
        return docs
    else:
        return None
