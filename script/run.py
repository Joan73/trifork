"""
run.py

Description:
    Script to scale all images and annotation files

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import os
import argparse
import traceback
from core.image_annotations import ImageAnnotations
from core.path_consistensy import InputOutputPathConsistensy
from core.custom_exceptions import NoSuchPath, UnvalidAnnotationsFile, UnvalidKittiFolderFormat
from utils import custom_logger

logger = custom_logger(__file__)

path_to_self = os.path.join(os.path.dirname(__file__))
path_to_package = os.path.abspath(os.path.join(path_to_self, '..'))

# ----------------------------------------------------------------
def debug_log_Exception(e):
    """Log missing argument exception

    Parameters:
        e (Exception): Raised exception 
    """
    logger.error(f'Exception Type: {type(e)}')
    logger.error(f'Exception message: {e}')
    logger.error(traceback.format_exc())
    raise e

# ----------------------------------------------------------------
def process_arguments():
    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(
        description = "Script",
        epilog = 'Press "CTRL-C" to stop the service.',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--target_width',
                        nargs   = '?',
                        dest    = 'target_width',
                        help    =  'target width',
                        type    = int,
                        default = 284 
    )

    parser.add_argument('--target_height',
                        nargs   = '?',
                        dest    = 'target_height',
                        help    =  'target height',
                        type    = int,
                        default = 284 
    )

    parser.add_argument('--input_path',
                        nargs   = '?',
                        dest    = 'input_path',
                        help    = 'path to data',
                        type    = str,
                        default = None
    )

    parser.add_argument('--output_path',
                        nargs   = '?',
                        dest    = 'output_path',
                        help    = 'path to store scaled images and annotations',
                        type    = str,
                        default = None
    )

    parser.add_argument('--log_level',
                        nargs = '?',
                        dest = "log_level",
                        default = "INFO",
                        choices = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
                        help = "Set logging level")
    
    # Parse the commandline
    args = parser.parse_args()
    return args

# ----------------------------------------------------------------
def main():

    logger.info('Initializing script')

    # Process arguments
    args = process_arguments()
    logger.setLevel(args.log_level)
    logger.info(f'Parsed command arguments: {args}')  

    # Store input/ output path
    if args.input_path == None:
        path_to_data = os.path.join(path_to_package, 'data')
    else:
        path_to_data = args.input_path
    
    if args.output_path == None:
        path_to_output = path_to_package
    else:
        path_to_output = args.output_path

    try:
        paths = InputOutputPathConsistensy(path_to_data, path_to_output)
    except NoSuchPath as e:
        debug_log_Exception()
    except UnvalidKittiFolderFormat as e:
        debug_log_Exception()
    
    logger.info('Input/output path are consistent with Kitti Format')
            
    # Iterate over all filenames and scale image/annotation files
    filenames = paths.get_filenames_no_extension()
    logger.info('Starting scaling all files')

    for filename in filenames:
        
        # Paths to image and annotations folder
        path_to_image = os.path.join(paths.path_to_images, filename+'.jpg')
        path_to_annotations = os.path.join(paths.path_to_annotations, filename +'.txt')
        
        # Paths to image and annotations scaled folder
        path_to_scaled_image = os.path.join(paths.path_to_scaled_images, filename+'.jpg')
        path_to_scaled_annotations = os.path.join(paths.path_to_scaled_annotations, filename+'.txt')
        
        try:
            img_ann = ImageAnnotations(path_to_image, 
                                       path_to_annotations,
                                       path_to_scaled_image, 
                                       path_to_scaled_annotations
                                       )
        except UnvalidAnnotationsFile as e:
            debug_log_Exception()
        
        img_ann.scale(target_width = args.target_width, target_height = args.target_height)
        img_ann.write()

        logger.info(f'Filename [{filename}] succesfully scaled')

# ----------------------------------------------------------------
if __name__ == '__main__':
    main()