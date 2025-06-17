

Install required packages:

```bash
pip install -r requirements.txt
```

## 🚀 Deployment Instructions

This project uses AWS SAM (Serverless Application Model) for deployment.

### Prerequisites
- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.11 installed

### First time
```bash
sam build --use-container --profile <your aws profile>
sam deploy --guided --profile <your aws profile>
```

### Subsequent Deployments
To build and deploy the project using a single command, run the following:

```bash
./deploy.sh <your aws profile> <stackname>
```

## Test the function

```bash
curl -X POST https://<your-api-id>.execute-api.eu-west-1.amazonaws.com/Prod/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What did the Alzheimer's study focus on?\"}"
```