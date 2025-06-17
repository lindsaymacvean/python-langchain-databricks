import os
import boto3
import tempfile
import json
from botocore.exceptions import ClientError
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

s3 = boto3.client("s3")

BUCKET_NAME = "python-langchain-databricks-demo-processed"
FAISS_INDEX_PREFIX = "faiss_index"

def download_faiss_index(tmpdir):
    files = ["index.faiss", "index.pkl"]
    for file in files:
        s3.download_file(BUCKET_NAME, f"{FAISS_INDEX_PREFIX}/{file}", os.path.join(tmpdir, file))

def load_faiss_index(tmpdir):
    load_dotenv()
    embedding_model = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    return FAISS.load_local(tmpdir, embedding_model, allow_dangerous_deserialization=True)

def get_openai_api_key(secret_name="OpenAIApiKey", region_name="eu-west-1"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        import json
        return json.loads(get_secret_value_response["SecretString"])["OPENAI_API_KEY"]
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