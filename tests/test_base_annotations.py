"""
test_base_annotations.py

Description:
    Unnitest for annotations

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
import uuid
from pathlib import Path
import unittest
from core.annotations import Annotations
from core.custom_exceptions import UnvalidAnnotationsFile

path_to_self = os.path.join(os.path.dirname(__file__))
path_to_package = os.path.abspath(os.path.join(path_to_self, '..'))

class TestAnnotations(unittest.TestCase):

    # ===================================================================================
    @classmethod
    def setUpClass(self):
        """Initialize annotations files for testing"""

        self.image_width = 500
        self.image_height = 375
        self.target_width = 284
        self.target_height = 284
        self.bounding_box = [178, 84, 230, 143]

        # Create a folder to store a made up annotations file
        Path(os.fspath(os.path.join(path_to_self,'data'))).mkdir()

        # Write some made up annotations into a file
        self.file_name = 'test-'+uuid.uuid1().hex+'.txt'
        self.path_to_annotations = os.path.join(path_to_self, 'data', self.file_name)

        with open(self.path_to_annotations, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 0 111 144 134 174 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 0 272 53 325 111 0 0 0 0 0 0 0'+'\n')
            file.write('person 0 0 0 141 83 181 131 0 0 0 0 0 0 0'+ '\n')
        
        # Write some made up unvalid annotations into a file (other numeric params)
        self.file_name_unvalid_numeric_params = ''+uuid.uuid1().hex+'.txt'
        self.path_to_unvalid_numeric_params = os.path.join(path_to_self, 'data', self.file_name_unvalid_numeric_params)

        with open(self.path_to_unvalid_numeric_params, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 2 111 144 134 174 0 0 0 0 0 0 0'+'\n')
        
        # Write some made up unvalid annotations into a file (no bounding box)
        self.file_name_no_box = ''+uuid.uuid1().hex+'.txt'
        self.path_to_annotations_no_box = os.path.join(path_to_self, 'data', self.file_name_no_box)

        with open(self.path_to_annotations_no_box, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('helmet 0 0 0 0 0 0 0 0 0 0 0 0 0 0'+'\n')
        
        # Write some made up unvalid annotations into a file (no class name)
        self.file_name_no_class = ''+uuid.uuid1().hex+'.txt'
        self.path_to_annotations_no_class = os.path.join(path_to_self, 'data', self.file_name_no_class)

        with open(self.path_to_annotations_no_class, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('0 0 0 111 144 134 174 0 0 0 0 0 0 0'+'\n')
        
        # Write some made up unvalid annotations into a file (unvalid class name)
        self.file_name_unvalid_class = ''+uuid.uuid1().hex+'.txt'
        self.path_to_annotations_unvalid_class = os.path.join(path_to_self, 'data', self.file_name_unvalid_class)

        with open(self.path_to_annotations_unvalid_class, 'w') as file:
            file.write('helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            file.write('hel met 0 0 0 111 144 134 174 0 0 0 0 0 0 0'+'\n')
        
        # Expected returned values for the tests
        self.expected_annotations = ['helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0',
                                     'helmet 0 0 0 111 144 134 174 0 0 0 0 0 0 0',
                                     'helmet 0 0 0 272 53 325 111 0 0 0 0 0 0 0',
                                     'person 0 0 0 141 83 181 131 0 0 0 0 0 0 0']
        
        self.expected_scaled_bounding_box = [101.1, 63.62, 130.64, 108.3]

        self.expected_scaled_annotations = ['helmet 0 0 0 101.1 63.62 130.64 108.3 0 0 0 0 0 0 0', 
                                            'helmet 0 0 0 63.05 109.06 76.11 131.78 0 0 0 0 0 0 0', 
                                            'helmet 0 0 0 154.5 40.14 184.6 84.06 0 0 0 0 0 0 0', 
                                            'person 0 0 0 80.09 62.86 102.81 99.21 0 0 0 0 0 0 0']
    
    # ===================================================================================
    @classmethod
    def tearDownClass(self):
        """Remove testing files and folder"""

        os.remove(self.path_to_annotations)
        os.remove(self.path_to_unvalid_numeric_params)
        os.remove(self.path_to_annotations_no_box)
        os.remove(self.path_to_annotations_no_class)
        os.remove(self.path_to_annotations_unvalid_class)
        Path(os.fspath(os.path.join(path_to_self,'data'))).rmdir()
    
    # ===================================================================================
    def test_annotations_self_consistensy(self):
        try:
            _ = Annotations(self.path_to_annotations) 
        except Exception as e:
            self.fail(f'Error checking consistensy of annotations: {e}')
    
    # ===================================================================================
    def test_annotations_no_class(self):
        """
        Testing a annotation file with an entry missing class name 
        """
        try:
            _ = Annotations(self.path_to_annotations_no_class) 
        except UnvalidAnnotationsFile as e:
            self.assertEqual(str(e), 'Missing class name')
    
    # ===================================================================================
    def test_annotations_unvalid_class_name(self):
        """
        Testing a annotation file with no bounding box
        """
        try:
            _ = Annotations(self.path_to_annotations_unvalid_class) 
        except UnvalidAnnotationsFile as e:
            self.assertEqual(str(e), 'Unvalid class name')
    
    # ===================================================================================
    def test_annotations_unvalid_numeric_params(self):
        """
        Testing a annotation file with unvalid numeric parameters
        """
        try:
            _ = Annotations(self.path_to_unvalid_numeric_params) 
        except UnvalidAnnotationsFile as e:
            self.assertEqual(str(e), 'Only bounding box are permitted')
    
    # ===================================================================================
    def test_annotations_no_box(self):
        """
        Testing a annotation file with no bounding box
        """
        try:
            _ = Annotations(self.path_to_annotations_no_box) 
        except UnvalidAnnotationsFile as e:
            self.assertEqual(str(e), 'Unvalid bounding box')

    # ===================================================================================
    def test_annotations_read(self):
        """
        Testing annotation file consistensy and accurate label extraction
        """
        try:
            annotations = Annotations(self.path_to_annotations)
            self.assertEqual(set(annotations._annotations), set(self.expected_annotations))
        except Exception as e:
            self.fail(f'Error reading annotation file: {e}')

    # ===================================================================================
    def test_annotations_scale_bounding_box(self):
        """
        Testing scale_bound_box() function from Annotations class
        """
        try:
            annotations = Annotations(self.path_to_annotations)
            x_min_scale, y_min_scale, x_max_scale, y_max_scale = annotations.scale_bounding_box(self.image_width, 
                                                                                                self.image_height, 
                                                                                                self.bounding_box, 
                                                                                                self.target_width,
                                                                                                self.target_height
                                                                                                )
            scaled_bounding_box = [x_min_scale, y_min_scale, x_max_scale, y_max_scale]
            self.assertEqual(scaled_bounding_box, self.expected_scaled_bounding_box)
        except Exception as e:
            self.fail(f'Error scaling bounding box: {e}')
    
    # ===================================================================================
    def test_annotations_scale_all(self):
        """
        Testing scale() function from Annotations class
        """
        try:
            annotations = Annotations(self.path_to_annotations)
            scaled_annotations = annotations.scale(self.image_width, 
                                                   self.image_height, 
                                                   self.target_width,
                                                   self.target_height)
            
            self.assertEqual(scaled_annotations, self.expected_scaled_annotations)
        except Exception as e:
            self.fail(f'Error scaling annotation file: {e}')

# =======================================================================================
if __name__ == '__main__':
    unittest.main(verbosity=2)
    exit(0)
