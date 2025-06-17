# python-langchain-databricks

This is a demo showcasing how to use Python, LangChain, and Databricks to build a Retrieval-Augmented Generation (RAG) system.

See [architecture diagram](https://lucid.app/lucidchart/4e89ddae-27ad-4dd9-bb3f-8ae9a99c00d0/edit?view_items=MvMpUUDDa4at&invitationId=inv_8e8e2bde-abf9-4345-ad46-3881f3ea2f4d)

## Test it now
```bash
curl -X POST https://ziy71um3v8.execute-api.eu-west-1.amazonaws.com/Prod/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What did the Alzheimer's study focus on?\"}"
```

## 🧠 Use Case: Query Medical Trial Data with LangChain and Databricks

This project demonstrates a workflow where a user uploads medical trial data (e.g. CSV), and then another user can ask questions about that data using a natural language interface powered by LangChain and LLMs.

---

### ✅ Step 1: Upload Data
A user uploads structured data (e.g. medical trial results) in CSV format to a designated storage location (e.g. S3).

---

### ✅ Step 2: Preprocess and Embed with Databricks
Databricks loads and cleans the CSV data. It then splits the content into chunks and generates embeddings (numerical vector representations) for each chunk using an embedding model (e.g. OpenAI or HuggingFace).

---

### ✅ Step 3: Store Embeddings
The embeddings are stored locally using FAISS that can be used by LangChain in AWS Lambda.

---

### ✅ Step 4: Query with LangChain (Lambda)
Another user sends a question about the data (e.g. “Which treatment was most effective?”). LangChain embeds the question, retrieves relevant data chunks from the embedding store, and sends the context to an LLM to generate a grounded response.


## Prerequisites
- Python 3.x
- pip

### Set Up Virtual Environment
Before installing dependencies, it's recommended to create two virtual environments:

1. For Deploying the lambda function
```bash
python3 -m venv venv-deploy
source venv-deploy/bin/activate  # On Windows use `.venv\Scripts\activate`
deactivate
```
Then see [lambda-deploy](lambda-deploy) directory

2. For running the databricks notebook locally
```bash
python3 -m venv venv-databricks
source venv-databricks/bin/activate  # On Windows use `.venv\Scripts\activate`
deactivate
```
Then see [databricks-etl](databricks-etl) directory


