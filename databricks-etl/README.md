Get an OpenAI API Key and put it into env as
`OPENAI_API_KEY=`

Install required packages:

```bash
pip install -r requirements.txt
```

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