import os
from pathlib import Path
import unittest
import uuid
import time
from subprocess import Popen, PIPE, TimeoutExpired
import requests
from PIL import Image
import shutil

REST_API_PORT = "8080"
LOG_LEVEL = "ERROR"

path_to_self= os.path.join(os.path.dirname(__file__))

WARMUP_TIME = 2

p = Path(os.path.realpath(__file__))
rest_api_address = str(p).rpartition('/')[0]+'/../restapi/rest_api.py'
rest_api_command = ['python3', rest_api_address]

rest_api_params = rest_api_command + \
                ["--rest_api_port"   , REST_API_PORT,
                "--log_level"       , LOG_LEVEL]

base_url = 'http://localhost:8080'
user_id = 'jponte98@gmail.com'


class TestRestApi(unittest.TestCase):
    # ===================================================================================
    def setUp(self):
        '''Spawn a memory server instance and initialize with episodes'''
        
        # Launch rest api
        self.restAPI = Popen(rest_api_params,stdout=PIPE, stderr=PIPE)
        time.sleep(WARMUP_TIME)
        if self.restAPI.poll() != None:
            print('Error Initiating Rest API')
            print(f'STDOUT:\n'+
                   '===============================\n'+
                   self.restAPI.stdout.read().decode('utf-8')+
                   '\n===============================\n'
            )
            print(f'STDERR:\n'+
                   '===============================\n'+
                   self.restAPI.stderr.read().decode('utf-8')+
                   '\n===============================\n'
                   )
            print(f'Killing process')
            self.restAPI.kill()
            raise Exception('RestAPI failed to run')
        
        # Get auth token
        try:
            r = requests.post(f'{base_url}/auth', data={'user_id': user_id})
            r.raise_for_status()
            self.token = r.json()['token']
        except requests.HTTPError as e:
            raise Exception(f'Error getting auth token: {e}')

        return 
    # ===================================================================================
    def tearDown(self):
        ''' Kill memory servers '''
        # For some reason, if not kill and restored the subprocesses can get stuck
        try:
            self.restAPI.terminate()
            self.restAPI.wait(5)
        except TimeoutExpired:
            # Failed to terminate so lets kill it
            self.restAPI.kill()
        
        # If executed too fast these IO will still open
        self.restAPI.stderr.close()
        self.restAPI.stdout.close()
    
    # ===================================================================================
    def test_rest_api_home(self):
        """Testing REST API home message"""
        try:
            r = requests.get(f'{base_url}/', 
                             timeout=20)
            r.raise_for_status()
            result = r.json()
            self.assertEqual(result['message'],'trifork technical assignment')
        except Exception as e:
            self.fail(f'Error getting home message: {e}')
    
    # ===================================================================================
    def test_rest_api_scale(self):
        """Testing REST API scaling function"""
        try:
            # Create a directory structure following Kitti format with a made up
            # image and annotations file
            Path(os.fspath(os.path.join(path_to_self,'data'))).mkdir()
            path_to_data = os.path.join(path_to_self, 'data')
            Path(os.fspath(os.path.join(path_to_data,'images'))).mkdir()
            Path(os.fspath(os.path.join(path_to_data,'annotations'))).mkdir()

            image = Image.new(mode='RGB', size = (500,500), color = (0,255,0))      
            unique_id = 'test-'+uuid.uuid1().hex
            path_to_image = os.path.join(path_to_data, 'images', unique_id+'.jpg')
            path_to_annotations = os.path.join(path_to_data, 'annotations', unique_id+'.txt')
            image.save(path_to_image)
            with open(path_to_annotations, 'w') as file:
                file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
                file.write('helmet 0 0 0 111 144 134 174 0 0 0 0 0 0 0'+'\n')
                file.write('helmet 0 0 0 272 53 325 111 0 0 0 0 0 0 0'+'\n')
                file.write('person 0 0 0 141 83 181 131 0 0 0 0 0 0 0'+ '\n')

            # Make request to Rest API to scale data
            r = requests.get(f'{base_url}/images', 
                             headers={'Authorization': f'bearer {self.token}'},
                             params={"input_path" : f'{path_to_data}',
                                     "output_path" : f'{path_to_data}'},
                             timeout=20)
            r.raise_for_status()
            result = r.json()
            self.assertEqual(result['message'], 'data successfully scaled')
        except Exception as e:
            self.fail(f'Error scaling data: {e}')
        finally:
            # Remove all testing files and directories
            shutil.rmtree(path_to_data)
 
# =======================================================================================
if __name__ == '__main__':
    unittest.main(verbosity=2)
    exit(0)