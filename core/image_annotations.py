
"""
image_annotations.py

Description:
    This class provides methods to scale and save a pair of 
    image and annotations file

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

from PIL import Image
from core.annotations import Annotations


class ImageAnnotations(object):

    # ================================================================
    # Initialization

    # ----------------------------------------------------------------
    def __init__(self, path_to_input_image, path_to_input_annotations, 
                 path_to_scaled_image, path_to_scaled_annotations):
        """
        ImageAnnotations, an abstract representation of a pair of image
        and annotations file. Provides methods to scale and save results.

        Parameters:
            path_to_input_image (str): path to input image
            path_to_input_annotations (str): path to input annotations
            path_to_scaled_image (str): path to scaled image
            path_to_scaled_annotations (str): path to scaled annotations
        """
        self._path_to_input_image = path_to_input_image
        self._path_to_input_annotations = path_to_input_annotations
        self._path_to_scaled_image = path_to_scaled_image
        self._path_to_scaled_annotations = path_to_scaled_annotations
        self._image = Image.open(self._path_to_input_image)
        self._annotations = Annotations(self._path_to_input_annotations)
        self._scaled_image = None
        self._scaled_annotations = None
    
    # ----------------------------------------------------------------  
    def scale(self, target_width, target_height):
        """
        Scale both image and annotations

        Parameters:
            target_width (int): Target width to scale the image
            target_height (int): Target height to scale the image
        """
        self._scaled_image = self._image.resize((target_width, target_height))
        image_width, image_height = self._image.size
        self._scaled_annotations = self._annotations.scale(image_width, 
                                                           image_height, 
                                                           target_width, 
                                                           target_height
                                                           )

    # ----------------------------------------------------------------
    def write(self):
        """
        Save scaled image and annotations
        """
        self._scaled_image.save(self._path_to_scaled_image)

        with open(self._path_to_scaled_annotations, 'w') as file:
            for object_label in self._scaled_annotations:
                file.write(object_label+'\n')
        