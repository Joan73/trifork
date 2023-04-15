"""
test_base_image_annotations.py

Description:
    Unnitest for image annotations

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
import uuid
from pathlib import Path
import unittest
from PIL import Image
from core.image_annotations import ImageAnnotations

path_to_self = os.path.join(os.path.dirname(__file__))
path_to_package = os.path.abspath(os.path.join(path_to_self, '..'))

class TestImageAnnotations(unittest.TestCase):

    # ===================================================================================
    @classmethod
    def setUpClass(self):
        """Initialize folders and files for testing"""

        self.target_width = 284
        self.target_height = 284

        # Create a folder to store a made up image and annotations file
        Path(os.fspath(os.path.join(path_to_self,'data'))).mkdir()
        self.image = Image.new(mode='RGB', size = (500,500), color = (0,255,0))      
        self.unique_id = 'test-'+uuid.uuid1().hex
        self.path_to_image = os.path.join(path_to_self, 'data', self.unique_id+'.jpg')
        self.path_to_annotations = os.path.join(path_to_self, 'data', self.unique_id+'.txt')
        self.image.save(self.path_to_image)
        with open(self.path_to_annotations, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 0 111 144 134 174 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 0 272 53 325 111 0 0 0 0 0 0 0'+'\n')
            file.write('person 0 0 0 141 83 181 131 0 0 0 0 0 0 0'+ '\n')
        
        # Create a folder to store a scaled made up image and annotations file
        Path(os.fspath(os.path.join(path_to_self,'output'))).mkdir()
        self.path_to_scaled_image = os.path.join(path_to_self, 'output', self.unique_id+'.jpg')
        self.path_to_scaled_annotations = os.path.join(path_to_self, 'output', self.unique_id+'.txt')
        
        # Expected results for testing
        self.expected_scaled_annotations = ['helmet 0 0 0 101.1 47.71 130.64 81.22 0 0 0 0 0 0 0', 
                                            'helmet 0 0 0 63.05 81.79 76.11 98.83 0 0 0 0 0 0 0', 
                                            'helmet 0 0 0 154.5 30.1 184.6 63.05 0 0 0 0 0 0 0', 
                                            'person 0 0 0 80.09 47.14 102.81 74.41 0 0 0 0 0 0 0']
        
    
    # ===================================================================================
    @classmethod
    def tearDownClass(self):
        """Remove testing files and folders"""    

        os.remove(os.path.join(path_to_self, 'data', self.unique_id+'.jpg'))
        os.remove(os.path.join(path_to_self, 'data', self.unique_id+'.txt'))
        Path(os.fspath(os.path.join(path_to_self,'data'))).rmdir()
        try:
            os.remove(os.path.join(path_to_self, 'output', self.unique_id+'.jpg'))
            os.remove(os.path.join(path_to_self, 'output', self.unique_id+'.txt'))
        except FileNotFoundError:
            pass
        Path(os.fspath(os.path.join(path_to_self,'output'))).rmdir()
        
    
    # ===================================================================================
    def test_image_annotations_scale(self):
        """
        Testing scale() function from ImageAnnotations class
        """
        try:
            img_ann = ImageAnnotations(self.path_to_image,
                                       self.path_to_annotations,
                                       self.path_to_scaled_image,
                                       self.path_to_scaled_annotations
                                       )
            img_ann.scale(self.target_width, self.target_height)

            width, height = img_ann._scaled_image.size
            self.assertEqual(width, self.target_width)
            self.assertEqual(height, self.target_height)
            self.assertEqual(img_ann._scaled_annotations, self.expected_scaled_annotations)
        except Exception as e:
            self.fail(f'Error scaling image and annotation file: {e}')
    
    # ===================================================================================
    def test_image_annotations_save(self):
        """
        Testing write() function from ImageAnnotations class
        """
        try:
            img_ann = ImageAnnotations(self.path_to_image,
                                       self.path_to_annotations,
                                       self.path_to_scaled_image,
                                       self.path_to_scaled_annotations
                                       )
            img_ann.scale(self.target_width, self.target_height)
            img_ann.write()

            # Check stored scaled image and annotation files exist
            self.assertEqual(Path(os.fspath(self.path_to_scaled_image)).exists(), True)
            self.assertEqual(Path(os.fspath(self.path_to_scaled_annotations)).exists(), True)
            
            # Check that the stored scaled image and annotation files are acccurately scaled
            with Image.open(self.path_to_scaled_image) as img:
                width, height = img.size
                self.assertEqual(width, self.target_width)
                self.assertEqual(height, self.target_height)

            with open(self.path_to_scaled_annotations, 'r') as file:
                scaled_annotations = file.read().splitlines()
            self.assertEqual(scaled_annotations, self.expected_scaled_annotations)
            
        except Exception as e:
            self.fail(f'Error saving scaled image and annotation files to output folder: {e}')

# =======================================================================================
if __name__ == '__main__':
    unittest.main(verbosity=2)
    exit(0)
