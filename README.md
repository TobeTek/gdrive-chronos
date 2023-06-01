# GDrive Chronos

A GitHub Action (un-official) to Monitor a Google Drive Folder for changes/modifications and invoke a webhook with changed files and their properties.

# Getting Started

## Create a Service Account

- Follow this guide on how to create a Service Account: https://www.labnol.org/google-api-service-account-220404

- Share the Google Drive folder with the Service Account email address

## Create GitHub Variables and Secrets

### Repository Secrets to Create

- `GCLOUD_SERVICE_ACCOUNT`: Google Cloud Service Account credentials in JSON format
- `ACCESS_TOKEN`: GitHub token, a Personal Access Token with `public_repo` scope if needed. If the repo is private, a Personal Access Token with `repo` scope is needed

### Repository Variables to Create

- `WEBHOOK_URL`: Optional webhook URL to receive files metadata whenever there are changes
- `GOOGLE_FOLDER_ID`: Google Folder ID to monitor

## Create a new Workflow

```yml
name: Test Action
on:
  push:
    branches: [master]
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  monitor-gdrive:
    runs-on: ubuntu-latest
    name: Test GitHub Action
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Monitor Google Drive Folder
        id: run-chronos
        env:
          GOOGLE_FOLDER_ID: ${{ vars.GOOGLE_FOLDER_ID }}
          WEBHOOK_URL: ${{ vars.WEBHOOK_URL }}
          GCLOUD_SERVICE_ACCOUNT: ${{ secrets.GCLOUD_SERVICE_ACCOUNT }}
          ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
        uses: tobetek/gdrive-chronos@master
```

# Contribute

Contributions are very much welcome. Open an Issue for bugs and feature requests. Send a PR to suggest changes!

[**Linus's law**](https://en.wikipedia.org/wiki/Linus%27s_law)

> `"given enough eyeballs, all bugs are shallow"`
