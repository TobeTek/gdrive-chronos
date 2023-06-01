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

- GCLOUD_SERVICE_ACCOUNT: Google Cloud Service Account credentials in JSON format
- ACCESS_TOKEN: Optional, GitHub token, a Personal Access Token with `public_repo` scope if needed. Required, if the artifact is from a different repo. Required, if the repo is private a Personal Access Token with `repo` scope is needed or GitHub token in a job where the permissions `action` scope set to `read`

# Repository Variable

- WEBHOOK_URL: Optional webhook URL to receive files metadata whenever there are changes
- GOOGLE_FOLDER_ID: Google Folder ID to monitor

# Environment Variables
