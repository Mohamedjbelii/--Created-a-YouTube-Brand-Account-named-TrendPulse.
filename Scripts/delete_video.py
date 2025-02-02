#!/usr/bin/python

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import argparse

TOKEN_FILE = "token.json"
CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_DELETE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run, you need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, [YOUTUBE_DELETE_SCOPE])

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, [YOUTUBE_DELETE_SCOPE])
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

def delete_video(youtube, video_id):
    try:
        youtube.videos().delete(id=video_id).execute()
        print(f"Video with ID '{video_id}' was successfully deleted.")
    except HttpError as e:
        print(f"An HTTP error occurred:\n{e}")
        if e.resp.status == 403:
            print("The request is forbidden. Check your permissions.")
        elif e.resp.status == 404:
            print("The video was not found. Check the video ID.")
        else:
            print(f"An error occurred: {e.content}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", required=True, help="The ID of the video to delete")
    args = parser.parse_args()

    youtube = get_authenticated_service()

    try:
        delete_video(youtube, args.video_id)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
