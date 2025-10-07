# RAG Chatbot with SGLang

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A Retrieval-Augmented Generation (RAG) chatbot framework built with **SGLang**, combining vector retrieval and language generation for more accurate and context-aware responses.

---

## 🚀 Table of Contents

1. [Features](#features)  
2. [Architecture Overview](#architecture-overview)  
3. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Configuration](#configuration)  
   - [Running Locally](#running-locally)  
   - [Using Docker / Compose](#using-docker--compose)  
4. [Code Structure](#code-structure)  
5. [Contributing](#contributing)  
6. [License](#license)  
7. [Acknowledgments](#acknowledgments)

---

## Features

- Retrieval-Augmented Generation (RAG) approach: combining a retriever module + generative language model  
- Modular design: easily swap components (retriever, vector database, generation model)  
- Clean separation between prompt, retriever, model, vector DB, and routing layers  
- REST API interface (via `route.py`)  
- Authentication support (`auth.py`)  
- Docker-friendly (Dockerfile + `compose.yaml`)  
- Easy deployment and reproducibility  
- Apache-2.0 Licensed (see [LICENSE](LICENSE))

---

## Architecture Overview

The system follows a modular pipeline:

1. **Retriever** — uses vector embeddings and a vector database to fetch the most relevant context segments.  
2. **Model / Generator** — consumes retrieved context + prompt to generate a response.  
3. **Prompt module** — constructs prompts combining user query + retrieved passages.  
4. **Routing / API** — handles incoming requests, authentication, and interfaces with the core modules.  
5. **Vector DB layer** — responsible for embedding text, storing vectors, and similarity search.  

---

## Getting Started

### Prerequisites

- Python 3.8+  
- pip (or venv)  
- Docker & Docker Compose  
- Access to an LLM / generative model API (e.g. OpenAI, local LLM models)  
- Access to a vector DB or library (FAISS, Pinecone, etc.)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SorawitChok/RAG-chatbot-with-SGLang.git
   cd RAG-chatbot-with-SGLang
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Using Docker / Compose

To run the whole stack with Docker:

```bash
docker compose up --build
```

This will build and spin up containers for your service (and any dependent services, e.g. a vector DB if included in `compose.yaml`).

---

## Code Structure

```
RAG-chatbot-with-SGLang/
├── auth.py
├── main.py
├── model.py
├── prompt.py
├── retriever.py
├── route.py
├── vectorDB.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── LICENSE
```

* **auth.py** — handles authentication logic
* **main.py** — application entrypoint (startup, server setup)
* **model.py** — generation / inference wrapper for LLM
* **prompt.py** — prompt engineering and assembly
* **retriever.py** — vector retrieval logic
* **route.py** — API routing & HTTP handlers
* **vectorDB.py** — vector database operations (indexing, querying)
* **compose.yaml / Dockerfile** — containerization and local orchestration
* **requirements.txt** — Python dependencies
* **LICENSE** — Apache-2.0 license for the project

---

## Contributing

Thank you for your interest in contributing! Here’s how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes and push: `git commit -m "Add XYZ"` / `git push`
4. Open a Pull Request
5. Ensure tests (if any) pass and include documentation updates

Please adhere to the existing code structure, maintain module separation, and document new features.

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

* Inspiration from RAG-based architectures and libraries in the open-source community
* Thanks to contributors, open-source tooling, and model providers
* If you reuse parts of this repository or integrate into academic or public work, attribution is appreciated

---
