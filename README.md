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
Before installing dependencies, it's recommended to create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

Then install required packages:

```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment Instructions

This project uses AWS SAM (Serverless Application Model) for deployment.

### Prerequisites
- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.11 installed

### AWS Deploy Steps

To build and deploy the project using a single command, run the following:

```bash
./deploy.sh <your aws profile>
```


This script wraps the SAM build and deploy process, using your specified AWS CLI profile.

---

## 🧱 Databricks Setup (Optional for Local or Cloud Execution)

If you want to run preprocessing or embedding jobs using Databricks, follow these steps:

### 1. Create a Databricks Account
- Visit [https://community.cloud.databricks.com](https://community.cloud.databricks.com) to register for a free Community Edition account.

### 2. Install the Databricks CLI (v2)
Recommend using Homebrew:

```bash
brew tap databricks/tap
brew install databricks
```

### 3. Authenticate with Databricks

```bash
databricks auth login --host https://<your-databricks-instance>
```

Use the URL shown in your browser (e.g., `https://dbc-xxxx.cloud.databricks.com`) when logged into Databricks.

You can name the profile when prompted, e.g. `python-langchain-databricks-demo`.

### 4. Verify the Connection

```bash
databricks workspace list / --profile <your-profile-name>
```


You should see `/Users`, `/Shared`, etc. listed.

### 5. Accessing S3 Buckets from Databricks

To allow Databricks to access your S3 buckets (e.g., for reading uploaded files or writing processed data), you need to create an IAM role in AWS and attach an appropriate policy. Then, grant access to Databricks by specifying a trust relationship.

#### 🛠 Example IAM Policy

Create a policy like this to allow read access to an upload bucket and write access to a processed bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::your-upload-bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::your-processed-bucket-name/*"
    }
  ]
}
```

Replace `your-upload-bucket-name` and `your-processed-bucket-name` with your actual bucket names.

#### 🔑 Trust Relationship for Databricks

Set the trust policy for your role to allow Databricks to assume it.

#### 🔗 Add the Role to Databricks

Once the IAM role is created:

1. Go to your Databricks workspace admin settings.
2. Add the IAM role under *Compute > Access Configuration* or during cluster setup under *Advanced Options > IAM Role*.
3. Ensure your notebook or cluster uses this role for reading and writing to S3.

This allows seamless and secure access to S3 during notebook execution.

## Test the function

```bash
curl -X POST https://<your-api-id>.execute-api.eu-west-1.amazonaws.com/Prod/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What did the Alzheimer's study focus on?\"}"
```


