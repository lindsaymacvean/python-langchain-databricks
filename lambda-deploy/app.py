import os
import boto3
import tempfile
from botocore.exceptions import ClientError
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

s3 = boto3.client("s3")

BUCKET_NAME = "python-langchain-databricks-demo-processed"
FAISS_INDEX_PREFIX = "faiss_index"

def download_faiss_index(tmpdir):
    files = ["index.faiss", "index.pkl"]
    for file in files:
        s3.download_file(BUCKET_NAME, f"{FAISS_INDEX_PREFIX}/{file}", os.path.join(tmpdir, file))

def load_faiss_index(tmpdir):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(tmpdir, embedding_model)

def get_openai_api_key(secret_name="OpenAIApiKey", region_name="eu-west-1"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response["SecretString"]
    except ClientError as e:
        raise Exception(f"Unable to retrieve OpenAI API key: {e}")

def lambda_handler(event, context):
    query = event.get("query", "What is this about?")
    os.environ["OPENAI_API_KEY"] = get_openai_api_key()

    with tempfile.TemporaryDirectory() as tmpdir:
        download_faiss_index(tmpdir)
        db = load_faiss_index(tmpdir)

        retriever = db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            retriever=retriever
        )
        result = qa_chain.run(query)
        return {
            "statusCode": 200,
            "body": result
        }