"""
runner.py

Description:
    Script to run unittest suite

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import sys
import os
from pathlib import Path
import argparse
import unittest

p = Path(os.path.realpath(__file__))
path_to_self = os.path.join(os.path.dirname(__file__))

def process_arguments():
    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(
        description = "Unittest runner",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--base_test',
                        dest    = 'base_test',
                        required= False,
                        default = True,
                        action= 'store_true',
                        help = "Only run the basic tests")
    parser.add_argument('--rest_api_test',
                        dest    = 'rest_api_test',
                        required= False,
                        default = True,
                        action= 'store_true',
                        help = "Only run rest api tests")
    parser.add_argument('--verbosity',
                        dest    = 'verbosity',
                        required= False,
                        default = 2,
                        type = int,
                        help = "Level of verbosity")
    
    # Parse the commandline
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = process_arguments()
    tests_suite=unittest.TestSuite()

    if args.base_test:
        tests_suite.addTests(unittest.defaultTestLoader.discover(f'{p.parent}', pattern='test_base*.py'))
    
    # TODO: Uncomment lines if rest api is available
    #if args.rest_api_test:
    #    tests_suite.addTests(unittest.defaultTestLoader.discover(f'{p.parent}',pattern='test_rest_api*.py'))
    
    test_runner = unittest.TextTestRunner(verbosity=args.verbosity)
    
    print(f'Test loaded: {len(tests_suite._tests)}')
    result = test_runner.run(tests_suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)