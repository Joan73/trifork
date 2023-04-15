"""
setup.py

The setup.

Author: Joan Pont
Copyright © 2023, Trifork, All Rights Reserved
"""

import os, re
from   setuptools import setup, find_packages

###################################################################

NAME        = "trifork"
PKG_PATH    = os.path.abspath(os.path.dirname(__file__))
META_PATH   = os.path.join(PKG_PATH, "__init__.py")


CLASSIFIERS = [
    "Private :: Do Not Upload",
    "Natural Language :: English",
    "Topic :: Scientific/Engineering",
    "Environment :: Other Environment",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.8",
    "License :: Other/Proprietary License"
]

REQUIREMENTS = []
with open("requirements.txt", "r") as fh:
    for line in fh.readlines():
        line = line.strip()
        if not re.match(r'^#', line):
            REQUIREMENTS.append(line)

###################################################################

# ----------------------------------------------------------------
# Use regular expressions to search within a file for metadata,
# usually __init__.py.  This makes it simple to have a single
# location for all the metadata and avoids copying/duplication.

def load_meta(file_path):
    """Extract all __var__ = <value> pairs from a file."""
    
    # Read in the file
    data = open(file_path).read()

    # Search through the file data using a regular expression:
    regex = r"__([a-zA-Z]*)__\s*= ['\"]([^'\"]*)['\"]"

    # Result returned will be a dictionary of keys and
    # corresponding metadata for each key.
    result = dict()
                             
    while True:
        match = re.search(regex, data)
        if match:
            # Get the variable name and value
            key = match.group(1)
            val = match.group(2)
            
            # Set the entry in the dictionary
            result[key] = val
            
            # Get the end of the match
            pos = match.span()[1]
            
            # and strip off the match for next search.
            data = data[pos:]
            continue
        else:
            break

    return result


# ----------------------------------------------------------------
if __name__ == "__main__":

    # Load all the metadata into a dictionary
    metadata = load_meta(META_PATH)

    # Make the setup call with all the parameters as set up by meta
    # and the globals above.
    setup(
        name                 = NAME,
        packages             = find_packages(),
        classifiers          = CLASSIFIERS,
        install_requires     = REQUIREMENTS,
        include_package_data = True,
        description          = metadata["description"],
        license              = metadata["license"],
        url                  = metadata["url"],
        version              = metadata["version"],
        author               = metadata["author"],
        author_email         = metadata["email"],
        maintainer           = metadata["author"],
        maintainer_email     = metadata["email"],
        zip_safe             = False
    )

