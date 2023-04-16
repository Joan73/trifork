"""
    Author:
        Joan Pont
    
    Copyright:
        Copyright © 2023, Trifork, All Rights Reserved
"""

import time
import jwt
from datetime import (
    datetime,
    timedelta
)
from tornado.web import (
    RequestHandler,
    HTTPError
)
from importlib import reload
import config


class TokenCheckHandler(RequestHandler):
    '''Child class of RequestHandler that checks for a valid token'''

    def prepare(self):
        '''custom "prepare()" method'''

        try:
            # reload the 'config' module in case live changes have been made to it while the server is running
            reload(config)
            auth = self.request.headers.get(config.AUTHORIZATION_HEADER)
            parts = auth.split()

            if len(parts) != 2:
                raise HTTPError(status_code=401)
            if parts[0].lower() != config.AUTHORIZATION_METHOD:
                raise HTTPError(status_code=401)

            token = parts[1]

            decoded = jwt.decode(
                token,
                config.SECRET,
                leeway=timedelta(seconds=config.TOKEN_EXPIRATION_LEEWAY),
                algorithms=config.ENCODING_ALGORITHM,
                options=config.JWT_DECODE_OPTIONS
            )
            self.current_user = decoded.get('user_id')
            if decoded.get('user_id') not in config.USER_IDS:
                time.sleep(config.DDOS_THROTTLE)
                raise HTTPError(status_code=401)
        except jwt.InvalidTokenError:
            time.sleep(config.DDOS_THROTTLE)
            raise HTTPError(status_code=401)
        except AttributeError:
            time.sleep(config.DDOS_THROTTLE)
            raise HTTPError(status_code=401)
        except HTTPError:
            time.sleep(config.DDOS_THROTTLE)
            raise
        except Exception:
            time.sleep(config.DDOS_THROTTLE)
            raise
