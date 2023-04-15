"""
annotations.py

Description:
    This class provides methods to scale all annotations of 
    a file

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import re
import numpy as np
from core.custom_exceptions import UnvalidAnnotationsFile

class Annotations(object):

    # ================================================================
    # Initialization

    # ----------------------------------------------------------------
    def __init__(self, path):
        """
        Annotations, an abstract representation of all the annotations
        related to an image.

        Parameters:
            path (str): path to annotations file
        """
        self._path = path
        self._annotations = None
        # Store annotations
        self.read_annotations()
        self.self_check()

    # ----------------------------------------------------------------
    def read_annotations(self):
        """
        Read annotations file and store all annotations
        """
        with open(self._path, 'r') as file:
            self._annotations = file.read().splitlines()
    
    # ---------------------------------------------------------------- 
    def self_check(self):
        """
        Consistensy check for the annotations. Its purpose is to ensure all
        annotations in the file follow the Kitti format and the requirements.
        Each annotation should have a class name followed by 14 numeric parameters.
        According to requirements, all annotations are bounding boxes, therefore only
        4 of the numeric parameters should be non zero.
        """

        for object_labels in self._annotations:

            # Check if there is a class name
            class_name = re.findall(r'[a-zA-Z]+', object_labels)
            if len(class_name) > 1:
                raise UnvalidAnnotationsFile(reason = 'unvalid_class')
                
            if len(class_name) == 0:
                raise UnvalidAnnotationsFile(reason = 'class')
            
            
            # Check if the annotation only contains the bounding box
            numeric_parameters = re.findall(r'[-]*[0-9]+[.]*[0-9]*', object_labels)

            if sum([float(parameter) for parameter in numeric_parameters[:3]]) != 0:
                raise UnvalidAnnotationsFile(reason = 'box')
            if sum([float(parameter) for parameter in numeric_parameters[3:7]]) == 0:
                raise UnvalidAnnotationsFile(reson = 'unvalid_box')
            if sum([float(parameter) for parameter in numeric_parameters[7:]]) != 0:
                raise UnvalidAnnotationsFile(reason = 'box')
    
    # ----------------------------------------------------------------
    def scale_bounding_box(self, width, height, bounding_box, 
                           target_width, target_height, decimals = 2):
        """
        Scale a given bounding box

        Parameters:
            width (int): width of the image
            height (int): height of the image
            bounding_box (list): list of the bounding box coordinates
            target_width (int): target width to scale the image
            target_height (int): target height to scale the image
            decimals (int): decimals to round scaled coordinates
        
        Return:
            Scaled bounding box coordinates
        """
        # Compute scaled width and height
        width_scale = target_width/width
        height_scale = target_height/height

        # Compute scaled bounding box coordinates
        x_min_scale = float(np.round(bounding_box[0] * width_scale, decimals))
        y_min_scale = float(np.round(bounding_box[1] * height_scale, decimals))
        x_max_scale = float(np.round(bounding_box[2] * width_scale, decimals))
        y_max_scale = float(np.round(bounding_box[3] * height_scale, decimals))
        
        return x_min_scale, y_min_scale, x_max_scale, y_max_scale

    # ----------------------------------------------------------------
    def scale(self, img_width, img_height, target_width, target_height):
        """
        Scale all annotations of the file

        Parameters:
            img_width (int): width of the image
            img_height (int): height of the image
            target_width (int): target width to scale the image
            target_height (int): target height to scale the image
        
        Return:
            List of the scaled annotations of the file
        """

        scaled_annotations = []

        for object_labels in self._annotations:

            # Get numeric parameters
            numeric_parameters = re.findall(r'[-]*[0-9]+[.]*[0-9]*', object_labels)
            # Store bounding box coordinates
            bounding_box_coord = [float(label) for label in numeric_parameters[3:7]]
            # Compute scaled bounding box coordinates
            x_min_scale, y_min_scale, x_max_scale, y_max_scale = self.scale_bounding_box(img_width, 
                                                                                         img_height, 
                                                                                         bounding_box_coord,
                                                                                         target_width,
                                                                                         target_height
                                                                                         )
            # Replace old coordinates with scaled coordinates
            numeric_parameters[3:7] = x_min_scale, y_min_scale, x_max_scale, y_max_scale
            
            # Store results
            numeric_parameters_scaled = ' '.join(str(label) for label in numeric_parameters)
            scaled_annotations.append(re.findall(r'[a-zA-Z]+', object_labels)[0]+' '+numeric_parameters_scaled)
        
        return scaled_annotations