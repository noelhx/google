#!/usr/bin/env python

import httplib2

from apiclient.discovery import build
from apiclient.http import MediaFileUpload,MediaIoBaseUpload
from oauth_util import Credentials
from StringIO import StringIO


OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'


class DriveClient(object):

    def __init__(self,argparser=None):
        """Initialize API client."""
        credentials = Credentials(name='drive',scope=OAUTH_SCOPE,argparser=argparser).get()
        self.service = build('drive', 'v2', http=credentials.authorize(httplib2.Http()))

    def get_file(self,file_name):
        """Get file(s) by remote name."""
        result = []
        page_token = None
        while True:
            if page_token is not None:
                files = self.service.files().list(q="title='%s'"%file_name,pageToken=page_token).execute()
            else:
                files = self.service.files().list(q="title='%s'"%file_name).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if page_token is None:
                break
        return result

    def upload(self,file_name,mime_type,title=None,description=None):
        """Alias for upload_file."""
        return self.upload_file(file_name,mime_type,title,description)

    def upload_file(self,file_name,mime_type,title=None,description=None):
        """Upload a file by name."""
        if title is None:
            title = file_name
        if description is None:
            description = title
        body = {
            'title': title,
            'description': description,
            'mimeType': mime_type
        }
        media_body = MediaFileUpload(file_name, mimetype=mime_type)
        return self.service.files().insert(body=body, media_body=media_body, convert=True).execute()

    def upload_string(self,contents,mime_type,title,description=None):
        """Upload a string."""
        if description is None:
            description = title
        body = {
            'title': title,
            'description': description,
            'mimeType': mime_type
        }
        media_body = MediaIoBaseUpload(StringIO(contents),mimetype=mime_type)
        return self.service.files().insert(body=body, media_body=media_body, convert=True).execute()
