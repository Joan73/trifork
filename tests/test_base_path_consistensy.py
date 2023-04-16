"""
test__base_path_consistensy.py

Description:
    Unnitest for path consistensy

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
import uuid
import re
from pathlib import Path
from PIL import Image
import unittest
from core.path_consistensy import InputOutputPathConsistensy
from core.custom_exceptions import UnvalidKittiFolderFormat, NoSuchPath

path_to_self = os.path.join(os.path.dirname(__file__))
path_to_package = os.path.abspath(os.path.join(path_to_self, '..'))

class TestPathConsistensy(unittest.TestCase):

    # ===================================================================================
    @classmethod
    def setUpClass(self):
        """Initialize data input folder for testing"""

        # Create data folders following Kitti Format
        Path(os.fspath(os.path.join(path_to_self,'data'))).mkdir()
        Path(os.fspath(os.path.join(path_to_self, 'data', 'images'))).mkdir()
        Path(os.fspath(os.path.join(path_to_self, 'data', 'annotations'))).mkdir()

        self.path_to_input = os.path.join(path_to_self, 'data')
        self.path_to_output = path_to_self
        
        # Create 3 different images and annotation files and store them in the proper directory
        for i in range(3):
            img = Image.new(mode='RGB', size = (500,500), color = (0,255,0))
            path_to_image = os.path.join(path_to_self, f'data/images/test{i}.jpg')
            path_to_annotations = os.path.join(path_to_self, f'data/annotations/test{i}.txt')
            img.save(path_to_image)
            with open(path_to_annotations, 'w') as file:
                file.write(f'helmet 0 0 0 {178+i} {84+i} {230+i} {143+i} 0 0 0 0 0 0 0'+'\n')
                file.write(f'helmet 0 0 0 {111+i} {144+i} {134+i} {174+i} 0 0 0 0 0 0 0'+'\n')
        
        
    # ===================================================================================
    @classmethod
    def tearDownClass(self):
        """
        Delete testing files and folders
        """
        for i in range(3):
            os.remove(os.path.join(path_to_self, f'data/images/test{i}.jpg'))
            os.remove(os.path.join(path_to_self, f'data/annotations/test{i}.txt'))
        
        Path(os.fspath(os.path.join(path_to_self,'data/images'))).rmdir()
        Path(os.fspath(os.path.join(path_to_self,'data/annotations'))).rmdir()
        Path(os.fspath(os.path.join(path_to_self,'data'))).rmdir()
    
    # ===================================================================================
    def test_path_consistensy_valid_input_output_path(self):
        """
        Testing consistensy of input and output path
        """
        try:
            paths_handler = InputOutputPathConsistensy(self.path_to_input, self.path_to_output)
        except Exception as e:
            self.fail(f'Error checking input/output consistensty: {e}')
        finally:
            # Delete output folders
            try:
                Path(os.fspath(paths_handler.path_to_scaled_images)).rmdir()
                Path(os.fspath(paths_handler.path_to_scaled_annotations)).rmdir()
                Path(os.fspath(os.path.dirname(paths_handler.path_to_scaled_images))).rmdir()
            except FileNotFoundError as e:
                self.fail(f'Error preparing output folder: {e}')
    
    # ===================================================================================
    def test_path_consistensy_ids(self):
        """
        Testing unique ids
        """
        try:
            paths_handler = InputOutputPathConsistensy(self.path_to_input, self.path_to_output)
            ids = paths_handler.get_filenames_no_extension()
            self.assertEqual(len(ids), 3)
            for id in ids:
                self.assertGreater(len(re.findall(r'test',id)), 0)
        except Exception as e:
            self.fail(f'Error checking file ids: {e}')
        finally:
            try:
                # Delete output folders
                Path(os.fspath(paths_handler.path_to_scaled_images)).rmdir()
                Path(os.fspath(paths_handler.path_to_scaled_annotations)).rmdir()
                Path(os.fspath(os.path.dirname(paths_handler.path_to_scaled_images))).rmdir()
            except FileNotFoundError as e:
                self.fail(f'Error preparing output folder: {e}')

    # ===================================================================================
    def test_path_consistensy_non_existent_input_path(self):
        """
        Testing non existent input path
        """
        try:
            non_existent_path = os.path.join(path_to_self, ''+uuid.uuid1().hex)
            _ = InputOutputPathConsistensy(non_existent_path, self.path_to_output)
            self.fail("Should have failed. Input path does not exist")
        except NoSuchPath as e:
            self.assertEqual(str(e), 'Input path does not exist') 
    
    # ===================================================================================
    def test_path_consistensy_input_path_not_directory(self):
        """
        Testing an input path which is not a directory
        """
        try:
            path_is_not_directory = os.path.join(self.path_to_input, 'images/test0.jpg')
            _ = InputOutputPathConsistensy(path_is_not_directory, self.path_to_output)
            self.fail("Should have failed. Input path does is not a directory")
        except NoSuchPath as e:
            self.assertEqual(str(e), 'Input path is not a directory')

    # ===================================================================================
    def test_path_consistensy_non_existent_output_path(self):
        """
        Testing a non exitent output path
        """
        try:
            non_existent_path = os.path.join(path_to_self, ''+uuid.uuid1().hex)
            _ = InputOutputPathConsistensy(self.path_to_input, non_existent_path)
            self.fail("Should have failed. Output path does not exist")
        except NoSuchPath as e:
            self.assertEqual(str(e), 'Output path does not exist') 
    
    # ===================================================================================
    def test_path_consistensy_output_path_not_directory(self):
        """
        Testing an output path that is not a directory
        """
        try:
            path_is_not_directory = os.path.join(self.path_to_input, 'images/test0.jpg')
            _ = InputOutputPathConsistensy(self.path_to_input, path_is_not_directory)
            self.fail("Should have failed. Output path does is not a directory")
        except NoSuchPath as e:
            self.assertEqual(str(e), 'Output path is not a directory') 
    
    # ===================================================================================
    def test_path_consistensy_unvalid_kitti_folder_structure(self):
        """
        Testing an input path that does not follow Kitti format folder structure
        """
        try:
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).mkdir()
            path_to_data = os.path.join(path_to_self, 'unvalid_data')
            _ = InputOutputPathConsistensy(path_to_data, self.path_to_output)
            self.fail("Should have failed. Input path does not follow Kitti format folder structure")
        except UnvalidKittiFolderFormat as e:
            self.assertEqual(str(e), 'Directory structure does not follow Kitti Format')
        finally:
            # Delete data folder
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).rmdir()
    
    # ===================================================================================
    def test_path_consistensy_no_data_available(self):
        """
        Testing data folder without any data in it
        """
        try:
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).mkdir()
            path_to_data = os.path.join(path_to_self, 'unvalid_data')

            _ = InputOutputPathConsistensy(path_to_data, self.path_to_output)
            self.fail("Should have failed. There is no data in the input folder")
        except UnvalidKittiFolderFormat as e:
            self.assertEqual(str(e), 'Data unavialable')
        finally:
            # Delete created folders
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).rmdir()
    
    # ===================================================================================
    def test_path_consistensy_unvalid_file_extension(self):
        """
        Testing data path with unvalid file extension according to Kitti Format
        """
        try:
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).mkdir()

            # Create image and annotation files
            img = Image.new(mode='RGB', size = (500,500), color = (0,255,0))
            unique_tmp_id = 'test'
            path_to_image = os.path.join(path_to_self, 'unvalid_data/images', unique_tmp_id+'.png')
            path_to_annotations = os.path.join(path_to_self, 'unvalid_data/annotations', unique_tmp_id+'.txt')
            img.save(path_to_image)
            with open(path_to_annotations, 'w') as file:
                file.write(f'helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            path_to_data = os.path.join(path_to_self, 'unvalid_data')

            _ = InputOutputPathConsistensy(path_to_data, self.path_to_output)
            self.fail("Should have failed. Data have the wrong extension")
        except UnvalidKittiFolderFormat as e:
            self.assertEqual(str(e).startswith('Wrong file extension'), True)
        finally:
            os.remove(path_to_image)
            os.remove(path_to_annotations)
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).rmdir()
    
    # ===================================================================================
    def test_path_consistensy_no_image_to_label_correspondence(self):
        """
        Testing a data folder structure without a one-to-one match between the images and 
        annotations files
        """
        try:
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).mkdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).mkdir()

            # Create image and annotation files
            img = Image.new(mode='RGB', size = (500,500), color = (0,255,0))
            unique_tmp_id = 'test'
            path_to_image = os.path.join(path_to_self, 'unvalid_data/images', unique_tmp_id+'.jpg')
            # Annotation file has different id to force the error
            path_to_annotations = os.path.join(path_to_self, 'unvalid_data/annotations', unique_tmp_id+'-flag.txt')
            img.save(path_to_image)
            with open(path_to_annotations, 'w') as file:
                file.write(f'helmet 0 0 0 178 84 230 143 0 0 0 0 0 0 0'+'\n')
            path_to_data = os.path.join(path_to_self, 'unvalid_data')

            _ = InputOutputPathConsistensy(path_to_data, self.path_to_output)
            self.fail("Should have failed. There is not a one-to-one match between images and annotations")
        except UnvalidKittiFolderFormat as e:
            self.assertEqual(str(e).startswith('No one-to-one match'), True)
        finally:
            os.remove(path_to_image)
            os.remove(path_to_annotations)
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/images'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data/annotations'))).rmdir()
            Path(os.fspath(os.path.join(path_to_self,'unvalid_data'))).rmdir()

# =======================================================================================
if __name__ == '__main__':
    unittest.main(verbosity=2)
    exit(0)
