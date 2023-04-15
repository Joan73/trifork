"""
custom_exceptions.py

Description:
     Custom exceptions

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

class UnvalidAnnotationsFile(Exception):
    """Exception raised when the annotation files do not follow technical assignment requirements"""

    def __init__(self, reason):
        
        messages = {
            'class': 'Missing class name',
            'unvalid_class': 'Unvalid class name',
            'box': 'Only bounding box are permitted',
            'unvalid_box': 'Unvalid bounding box'
        }
        
        super().__init__(messages[reason])


class UnvalidKittiFolderFormat(Exception):
    """Exception raised when input folder does not follow Kitti Format"""

    def __init__(self, reason):

        messages = {
            'folder': 'Directory structure does not follow Kitti Format',
            'empty': 'Data unavialable',
            'extension': 'Wrong file extension. Images should be .jpg and annotations .txt',
            'length': 'No one-to-one match name in the image and annotations folder'
        }
        
        super().__init__(messages[reason])

class NoSuchPath(Exception):
    """Exception raised when either the input or output path does not exist or is not a directory"""

    def __init__(self, reason):

        messages = {
            'input_exist': 'Input path does not exist',
            'input_dir': 'Input path is not a directory',
            'output_exist': 'Output path does not exist',
            'output_dir': 'Output path is not a directory'
        }
        super().__init__(messages[reason])
        