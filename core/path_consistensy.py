"""
path_consistensy.py

Description:
    Utility class to work with the input and output path. 
    Provides methods to check path consistensy, prepare
    output folders and get files unique identifier (unique
    id for each pair of image and annotation files)

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
from pathlib import Path
import uuid
import re
from core.custom_exceptions import UnvalidKittiFolderFormat, NoSuchPath


class InputOutputPathConsistensy(object):

    # ================================================================
    # Initialization

    # ----------------------------------------------------------------
    def __init__(self, input_path, output_path):
        """
        Input and output paths should be checked for consistensy and 
        ensure the structure follows Kitti Format. This class provides
        methods for that purpose.
        
        Parameters:
            input_path (str): path to where the data to be sacaled is stored
            output_path (str): path to where the scaled data must be stored
        """
        self._path_to_data = input_path
        self._path_to_output = output_path
        self._path_to_images = None
        self._path_to_annotations = None
        self._path_to_scaled_images = None
        self._path_to_scaled_annotations = None

        # Check input/output consistensy
        self.self_input_check()
        self.self_output_check()

        # Prepare output folder following Kitti format
        self.prepare_output_folders()
    
    # ----------------------------------------------------------------
    @property
    def path_to_images(self):
        return self._path_to_images
    
    @property
    def path_to_annotations(self):
        return self._path_to_annotations
    
    @property
    def path_to_scaled_images(self):
        return self._path_to_scaled_images
    
    @property
    def path_to_scaled_annotations(self):
        return self._path_to_scaled_annotations
    
    # ----------------------------------------------------------------
    def self_input_check(self):
        """
        Consistency check for input path. Data should be stored following
        Kitti Format. 
        """

        # Basic checks for folder existance
        if not Path(os.fspath(self._path_to_data)).exists():
            raise NoSuchPath(reason = 'input_exist')
        if not Path(os.fspath(self._path_to_data)).is_dir():
            raise NoSuchPath(reason = 'input_dir')
        
        # There should be only two subdirectories according to Kitti Format
        subfolders = [f.path for f in os.scandir(self._path_to_data) if f.is_dir()]

        if len(subfolders) != 2:
            raise UnvalidKittiFolderFormat(reason = 'folder')

        # Each subdirectory should not be empty, and should contain either 
        # .jpg files or .txt files
        files = os.listdir(subfolders[0])
        if len(files) == 0:
            raise UnvalidKittiFolderFormat(reason = 'empty')
        elif len(re.findall(r'\.jpg$', files[0])) != 0:
            self._path_to_images = subfolders[0]
        elif len(re.findall(r'\.txt$', files[0])) !=0:
            self._path_to_annotations = subfolders[0]
        else:
            raise UnvalidKittiFolderFormat(reason = 'extension')
        
        files = os.listdir(subfolders[1])
        if len(files) == 0:
            raise UnvalidKittiFolderFormat(reason = 'empty')
        elif len(re.findall(r'\.jpg$', files[0])) != 0:
            self._path_to_images = subfolders[1]
        elif len(re.findall(r'\.txt$', files[0])) !=0:
            self._path_to_annotations = subfolders[1]
        else:
            raise UnvalidKittiFolderFormat(reason = 'extension')

        # There should be a one-to-one match between image and annotation files
        image_names = os.listdir(self._path_to_images)
        annotations = os.listdir(self._path_to_annotations)

        file_image_no_extension = [re.sub(r'\.jpg$', '', image_name) for image_name in image_names]
        file_annotations_no_extension = [re.sub(r'\.txt$', '', filename) for filename in annotations]

        if set(file_image_no_extension) != set(file_annotations_no_extension):
            raise UnvalidKittiFolderFormat(reason = 'length')

    # ----------------------------------------------------------------
    def self_output_check(self):
        """
        Consistency check for output path.
        """

        if not Path(os.fspath(self._path_to_output)).exists():
            raise NoSuchPath(reason = 'output_exist')
        if not Path(os.fspath(self._path_to_output)).is_dir():
            raise NoSuchPath(reason = 'output_dir')

    # ----------------------------------------------------------------
    def prepare_output_folders(self):
        """
        Create Kitti Format output folder structure and store paths to 
        image and annotation folders
        """
        target_folder = 'output-'+uuid.uuid1().hex
        Path(os.fspath(os.path.join(self._path_to_output, target_folder))).mkdir()
        Path(os.fspath(os.path.join(self._path_to_output, target_folder, 'images'))).mkdir()
        Path(os.fspath(os.path.join(self._path_to_output, target_folder, 'annotations'))).mkdir()

        self._path_to_scaled_images = os.path.join(self._path_to_output, target_folder, 'images')
        self._path_to_scaled_annotations = os.path.join(self._path_to_output, target_folder, 'annotations')

    # ----------------------------------------------------------------
    def get_filenames_no_extension(self):
        """
        Get unique ids for every pair of image and annotation files
        """
        images_files = os.listdir(self._path_to_images)
        return [re.sub(r'\.jpg$', '', image_name) for image_name in images_files]
    