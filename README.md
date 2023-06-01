# Python Github Action

Monitor Google Drive Folder for file changes and invoke a webhook

# Setup

- Run 

```bash
python src/generate_token.py
```

To generate a `token.json`. That is the actual file you pass to Chronos.


- Create a Service Account
- Share the folder with the Service Account email address

> References: 
 - https://www.labnol.org/google-api-service-account-220404
 - https://developers.google.com/drive/api/quickstart/python

# Repository Secrets to Create
 - GCLOUD_SERVICE_ACCOUNT_CONFIG_JSON
 - WEBHOOK_URL
 - GOOGLE_FOLDER_ID

# Environment Variables