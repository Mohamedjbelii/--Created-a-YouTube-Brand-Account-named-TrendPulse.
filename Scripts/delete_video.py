#!/usr/bin/python

import httplib2
import os
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from googleapiclient.errors import HttpError


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
TOKEN_FILE = "token_{}.json"

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_DELETE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_SCOPE = "https://www.googleapis.com/auth/youtube"

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

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_DELETE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))
    
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
    argparser.add_argument("--video-id", required=True, help="The ID of the video to delete")
    args = argparser.parse_args()

    youtube = get_authenticated_service(args)

    try:
        delete_video(youtube, args.video_id)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
