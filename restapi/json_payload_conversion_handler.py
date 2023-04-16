"""
    Author:
        Joan Pont
    
    Copyright:
        Copyright © 2023, Trifork, All Rights Reserved
"""

import json
from tornado.web import (
    RequestHandler,
    HTTPError
)


class JSONPayloadConversionHandler(RequestHandler):
    '''Child class of RequestHandler checks if a request body is in JSON format and converts it to a dictionary'''

    def prepare(self):
        '''Decode serialized JSON content'''

        try:
            if self.request.headers.get("Content-Type", "").startswith("application/json"):
                self.json_args = json.loads(self.request.body)
            else:
                self.json_args = None
        except Exception:
            raise
