"""Rest API 

Description:
    This module is a tornado based rest api.

Author:
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
from re import S
import sys
import argparse
import json
import time
import jwt
import asyncio
from datetime import (
    datetime,
    timedelta
)
from dataclasses import dataclass
from tornado.web import (
    Application,
    RequestHandler,
    URLSpec,
    HTTPError,
    MissingArgumentError,
)

path_to_self = os.path.join(os.path.dirname(__file__))
path_to_package = os.path.abspath(os.path.join(path_to_self, '..'))
sys.path.append(path_to_package)

from token_check_handler import (
    TokenCheckHandler
)
from json_payload_conversion_handler import JSONPayloadConversionHandler
from importlib import reload
import config
import subprocess

#For debugging
import traceback
#from clabs.util  import custom_logger
from utils import custom_logger
logger = custom_logger(__file__)
args = {}

# ----------------------------------------------------------------

PYTHON3_9 = sys.version_info[0] == 3 and sys.version_info[1] == 9

# ----------------------------------------------------------------
def debug_log_prepare(handler):
    """Log message received before process it

    Parameters:
        handler (ptr): Caller function 

    """
    name = type(handler).__name__
    if 'Jira' in name:
        logger.debug(f'{name} > Jira request packages are not logged')
    else:
        logger.debug(f'{name} > Request Received : {handler.request}')
        logger.debug(f'{name} > Headers : {handler.request.headers}')
        logger.debug(f'{name} > Arguments: {handler.request.arguments}')
        logger.debug(f'{name} > Body: {handler.request.body}')


# ----------------------------------------------------------------
def debug_log_onfinish(handler):
    """Log response message after process it

    Parameters:
        handler (ptr): Caller function 

    """
    name = type(handler).__name__
    logger.debug(f'{name} > Response Code : {handler._status_code}')
    logger.debug(f'{name} > Write buffer  : {handler._write_buffer}')


# ----------------------------------------------------------------
def debug_log_missing_argument(handler, e):
    """Log missing argument exception

    Parameters:
        handler (ptr): Caller function
        e (Exception): Raised exception 

    """
    name = type(handler).__name__
    logger.error(f'{name} > MissingArgumentError - Argument: [{e.arg_name}]')
    if hasattr(handler,'json_args') and handler.json_args is not None:
        logger.error(f'{name} > Received arguments: {handler.json_args}')
    else:
        logger.error(f'{name} > Received arguments: {handler.request.arguments}')

# ----------------------------------------------------------------
def debug_log_HTTPException(handler, e):
    """Log missing argument exception

    Parameters:
        handler (ptr): Caller function
        e (Exception): Raised exception 

    """
    logger.error(f'{type(handler).__name__} > HTTPError: {e}')
    if hasattr(e,'log_message'):
        logger.error(f'{type(handler).__name__} > HTTPError log: {e.log_message}')

# ----------------------------------------------------------------
def debug_log_Exception(handler, e):
    """Log missing argument exception

    Parameters:
        handler (ptr): Caller function
        e (Exception): Raised exception 

    """
    logger.error(f'{type(handler).__name__} > Exception: {e}')
    logger.error(traceback.format_exc())
    if hasattr(e,'log_message'):
        logger.error(f'{type(handler).__name__} > Exception log: {e.log_message}')

# ----------------------------------------------------------------
def handle_exceptions(handler,error):
    """Handle any exception

    Description:
        Exception handling is very similar in most handlers so this function 
        purpose is to reduce the redundant code. Each exception will be logged
        properly and then raised as a HTTPError that will be used to produce
        the proper response message.

    Parameters:
        handler (ptr): Caller function
        e (Exception): Raised exception 
    
    """
    try:
        time.sleep(config.DDOS_THROTTLE)
        raise error
    except Exception as e:
        if type(e) is MissingArgumentError:
            debug_log_missing_argument(handler, e)
            raise HTTPError(status_code=401)
        elif type(e) is NotImplementedError: 
            logger.error(f'{type(handler).__name__} > Not Implemented: {e}')
            raise HTTPError(status_code=500, reason = 'Not implemented yet')
        elif type(e) is json.JSONDecodeError:
            logger.error(f'{type(handler).__name__} > JSON decode Error: {e}')
            raise HTTPError(status_code=415, reason = f'JSON decode error')
        elif type(e) is HTTPError:
            debug_log_HTTPException(handler,e)
            raise e
        else:
            debug_log_Exception(handler,e)
            raise HTTPError(status_code=500, reason=str(e))
# ----------------------------------------------------------------
def extract_parameters(handler, expected_param):
    """
    Extract the expected parameters from a HTTP request

    Parameters:
        handler (): the 'self' of the handler
        expected (dict): dictionary with pairs {name of the parameter: default value}
    
    Return:
        dictionary with the paramters
    """
    params =  {}
    if hasattr(handler,'json_args') and handler.json_args:
        logger.debug(f'{type(handler).__name__} > JSON Arguments')
        for p in expected_param:
            params[p] = handler.json_args.get(p) \
                        if p in handler.json_args \
                        else expected_param[p]
    else:
        for p in expected_param:
            if p in handler.request.arguments:
                if type(handler.request.arguments[p]) == list \
                    and len(handler.request.arguments[p]) > 1:
                    decoded_list = []
                    for x in handler.request.arguments[p]:
                        decoded_list.append(x.decode('utf-8','ignore'))
                    params[p] = decoded_list
                else:
                    params[p] = handler.request.arguments[p][0].decode('utf-8','ignore') 
            else:
                params[p] = expected_param[p]
    return params 

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class HomeHandler(RequestHandler):
    '''Home page'''
    # ----------------------------------------------------------------
    def prepare(self):
        debug_log_prepare(self)

    # ----------------------------------------------------------------
    def on_finish(self):
        debug_log_onfinish(self)

    # ----------------------------------------------------------------
    def get(self):
        self.write({'message': 'trifork technical assignment'})

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class AuthorizationHandler(JSONPayloadConversionHandler):
    '''Handle authorization to the API'''

    # ----------------------------------------------------------------
    def prepare(self):
        debug_log_prepare(self)
        JSONPayloadConversionHandler.prepare(self)
    # ----------------------------------------------------------------
    def on_finish(self):
        debug_log_onfinish(self)
    # ----------------------------------------------------------------
    def post(self):
        '''Create a new authorization token'''

        try:
            # reload the 'config' module in case live changes have been made to it while the server is running
            reload(config)
            if hasattr(self,'json_args') and self.json_args is not None:
                user_id = self.json_args.get('user_id')
            else:
                user_id = self.request.arguments['user_id'][0].decode('utf-8','ignore') \
                    if 'user_id' in self.request.arguments else 'MISSING'
            if user_id not in config.USER_IDS:
                time.sleep(config.DDOS_THROTTLE)
                raise HTTPError(status_code=401)
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=config.TOKEN_LIFETIME),
                'iat': datetime.utcnow()
            }
            encoded = jwt.encode(
                payload,
                config.SECRET,
                algorithm=config.ENCODING_ALGORITHM
            )
            if PYTHON3_9:
                # In 3.9 for some reason encoded is returned as a str that cant be decoded
                self.write({'token': encoded, 'user_id': user_id})
            else:
                token = encoded.decode('ascii','ignore') if type(encoded) is bytes \
                    else encoded
                self.write({'token': token, 'user_id': user_id})
        
        except Exception as e:
            handle_exceptions(self,e)

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class ScaleHandler(TokenCheckHandler, JSONPayloadConversionHandler):
    ''' Scale images and annotations '''

    # ----------------------------------------------------------------
    def prepare(self):
        '''Check authorization'''
        debug_log_prepare(self)
        JSONPayloadConversionHandler.prepare(self)
        #TokenCheckHandler.prepare(self)

    # ----------------------------------------------------------------
    def on_finish(self):
        debug_log_onfinish(self)
        
    # ----------------------------------------------------------------
    async def get(self):
        ''' Scale images '''
        try:
            params = extract_parameters(
                handler = self, 
                expected_param = {
                                 'input_path': '',
                                 'output_path': '',
                                 'target_width': 284,
                                 'target_height': 284
                                 }
            )
            for p in params:
                logger.debug(f'ScaleHandler GET > {p} = {params[p]}')

            # Prepare paths to run script
            path_to_script = os.path.join(path_to_package, 'script/run.py')

            if params['input_path'] == '':
                path_to_data = os.path.join(path_to_package, 'data')
            else:
                path_to_data = params['input_path']

            if params['output_path'] == '':
                output_path = path_to_data
            else:
                output_path = path_to_data
            
            # Run script
            subprocess.run(["python3", f"{path_to_script}", 
                            "--target_width", f"{params['target_width']}",
                            "--target_height", f"{params['target_height']}",
                            "--input_path", f"{path_to_data}",
                            "--output_path", f"{output_path}"
                            ], check = True)
                    
            self.write({'message': f"data successfully scaled"})        
        except Exception as e:
            handle_exceptions(self,e)


# ----------------------------------------------------------------
# ----------------------------------------------------------------

def make_app():
    '''Create the application hosted by the Tornado server'''
    
    settings = {
        'static_hash_cache': False,
        'debug': True,
        'serve_traceback': True,
        'autoreload': False
    }
    urls = [
        URLSpec(r'^/', \
                HomeHandler, name='home'),
        URLSpec(r'^/auth$', \
                AuthorizationHandler, name='auth'),
        URLSpec(r'^/images', \
                ScaleHandler, name='scale')
    ]
    return Application(urls, **settings)

# ----------------------------------------------------------------
def process_arguments():
    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(
        description = "REST API",
        epilog = 'Press "CTRL-C" to stop the service.',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--log_level',
                        nargs = '?',
                        dest = "log_level",
                        default = "INFO",
                        choices = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
                        help = "Set logging level")

    parser.add_argument('--rest_api_port',
                        nargs   = '?',
                        metavar = 'REST_API_PORT',
                        dest    = 'rest_api_port',
                        help    =  'rest api server port',
                        type    = int,
                        default = 8080 
    )
    
    # Parse the commandline
    args = parser.parse_args()
    return args

# ----------------------------------------------------------------
async def main():
    logger.info('Initializing REST API')

    args = process_arguments()
    logger.setLevel(args.log_level)
    logger.info(f'Parsed command arguments: {args}')

    app = make_app()
    app.listen(args.rest_api_port)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

# ----------------------------------------------------------------
if __name__ == '__main__':
    asyncio.run(main())
