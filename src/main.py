import json
import os
from datetime import datetime
from typing import Optional

from google.oauth2.service_account import Credentials as ServiceCredentials
from googleapiclient.discovery import build
from pydantic import BaseModel
from pydantic.json import pydantic_encoder
import requests

from utils import write_output_variable

SERVICE_ACCOUNT_CREDENTIALS = os.environ["GCLOUD_SERVICE_ACCOUNT"]
SERVICE_ACCOUNT_CREDENTIALS = json.loads(SERVICE_ACCOUNT_CREDENTIALS)
GOOGLE_FOLDER_ID = os.environ["GOOGLE_FOLDER_ID"]
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)


GITHUB_PATH = os.environ["GITHUB_WORKSPACE"]

LOG_FILE = os.path.join(GITHUB_PATH, "chronos/", "gdrive-chronos-dump.json")
OUTPUT_VARIABLE_NAME = "updated_files"
GDRIVE_API_PAGE_SIZE = 10


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS = ServiceCredentials.from_service_account_info(
    SERVICE_ACCOUNT_CREDENTIALS,
    scopes=SCOPES,
)


service = build("drive", "v3", credentials=CREDENTIALS)


class GdriveUser(BaseModel):
    displayName: str
    emailAddress: Optional[str]
    photoLink: Optional[str]


class GdriveFile(BaseModel):
    id: str
    name: str
    description: Optional[str]
    mimeType: Optional[str]
    iconLink: Optional[str]
    size: Optional[str]
    lastModifyingUser: Optional[GdriveUser]
    modifiedTime: datetime

    # Calculated
    folder_path: str

    def has_been_updated(self, old_cache: dict[str, "GdriveFile"]) -> bool:
        if old_version := old_cache.get(self.id, None):
            if self.modifiedTime == old_version.modifiedTime:
                return False
        return True


def get_files_from_google_folder(folder_id, folder_path=".") -> list[GdriveFile]:
    gdrive_files = []
    gdrive_subfolders = []

    query = f"'{folder_id}' in parents"
    files_service = service.files()
    request = files_service.list(
        q=query,
        pageSize=GDRIVE_API_PAGE_SIZE,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields="nextPageToken, files(id, name, kind, mimeType, iconLink, lastModifyingUser, size, description, modifiedTime)",
    )

    while request is not None:
        results = request.execute()
        files, folders = _process_response(results, folder_path=folder_path)
        gdrive_files.extend(files)
        gdrive_subfolders.extend(folders)
        request = files_service.list_next(request, results)

    # Recursively get files for subfolders
    subfolder_results = [
        get_files_from_google_folder(folder_id, folder_path)
        for [folder_id, folder_path] in gdrive_subfolders
    ]
    for files in subfolder_results:
        gdrive_files.extend(files)

    return gdrive_files


def _process_response(
    results, folder_path
) -> tuple[list[GdriveFile], list[tuple[str, str]]]:
    folders = []
    files: list[GdriveFile] = []
    for file in results.get("files", []):
        file.update({"folder_path": folder_path})
        if file["mimeType"] == "application/vnd.google-apps.folder":
            subfolder_path = folder_path + f"/{file['name']}"
            folders.append(
                (
                    file["id"],
                    subfolder_path,
                )
            )
        else:
            files.append(GdriveFile.parse_obj(file))

    return files, folders


NEW_FILES = get_files_from_google_folder(GOOGLE_FOLDER_ID)
NEW_FILES = {file.id: file for file in NEW_FILES}


def _read_log_file() -> dict[str, dict]:
    try:
        with open(LOG_FILE) as f:
            data = f.read()
            if data == "":
                return {}
            else:
                return json.loads(data)
    except FileNotFoundError:
        return {}


def _persist_log_file(files: dict[str, GdriveFile]):
    json_files = json.dumps(
        {k: file.dict() for k, file in files.items()}, default=pydantic_encoder
    )
    with open(LOG_FILE, "w") as f:
        f.write(json_files)


OLD_FILES = _read_log_file()
OLD_FILES = {k: GdriveFile.parse_obj(v) for k, v in OLD_FILES.items()}
updated_files = [
    file for file in NEW_FILES.values() if file.has_been_updated(OLD_FILES)
]
updated_files = (
    json.dumps(
        updated_files,
        default=pydantic_encoder,
    ),
)


if WEBHOOK_URL:
    requests.post(url=WEBHOOK_URL, json=updated_files)


OLD_FILES.update(NEW_FILES)
_persist_log_file(OLD_FILES)
write_output_variable(
    OUTPUT_VARIABLE_NAME,
    updated_files,
)
write_output_variable(
    "slack_message",
    json.dumps({"text": f"[Chronos Update]: \n{updated_files}"}),
)
