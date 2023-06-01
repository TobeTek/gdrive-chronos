# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from src.main import GdriveFile

# def render_slack_message(files: list["GdriveFile"]):
#     blocks:list[dict] = []
#     if not files:
#         return {
# 	"blocks": [
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "Hello, changes have been made to Gdrive: *FOLDER_ID*. The following files have been created or modified"
# 			}
# 		},
#     return {
# 	"blocks": [
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "Hello, changes have been made to Gdrive: *FOLDER_ID*. The following files have been created or modified"
# 			}
# 		},
# 		{
# 			"type": "divider"
# 		},
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "*File Name*\n File Description\n Size: $SIZE bytes\n Modified By: $Name, $email\n Modified At: $Time"
# 			},
#             "accessory": {
# 				"type": "image",
# 				"image_url": "https://lh3.googleusercontent.com/a-/AD_cMMRKocmME-2X6P_KyEsxnqIZwgY-r2t7MmGNoGPY=s64",
# 				"alt_text": "File Image"
# 			}
# 		}
# 	]
# }
#     ...
