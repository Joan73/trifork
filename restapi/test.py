import os
import requests
if __name__ == '__main__':
    base_url  = 'http://localhost:8080'
    path_to_self = os.path.dirname(__file__)
    path_to_file = os.path.join(path_to_self, '../tests/files/test.jpg')
    file = open(path_to_file, 'rb')
    r = requests.post(f'{base_url}/post',
                        files={'test.jpg': file}
                    )
    