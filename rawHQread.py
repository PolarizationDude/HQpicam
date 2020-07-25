# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Run imports
import os
try: 
    import numpy as np
except:
    error_msg = """Package numpy not included. It can be found on www.pypi.com 
    , installed using "pip install numpy" or similar formatting if using conda.
    """
    raise ImportError(error_msg)
    
# Define support functions
def HQjpeg_to_raw(path_in):
    """Convert raw JPEG to numpy.array(dtype=uint16)
    
    Arguments:
    path_in -- file path to *.jpeg file to convert
    
    Returns Numpy array [3040, 4056] dtype = unit16
    """    
    file_data = open_pic(path_in)
    # Search the file for the start of the raw data
    raw_start = file_data.find(b'BRCM')
    # Separate the file
    file_data = file_data[raw_start:]
    # pull the header info
    # pic_header = np.fromstring(file_data[:32768], dtype=np.uint8)
    # Separate the image data from the header
    pic_jumble = file_data[32768:]
    # Convert the jumble of bits into uints
    pic_flat = np.fromstring(pic_jumble, dtype=np.uint8)
    # Create array from things
    pic_array = pic_flat.reshape([(3040+16) , 6112])[:3040, :6084]
    bayer_array = pic_array.astype(np.uint16) << 4
    for byte in range(2):
        bayer_array[:, byte::3] |= ((bayer_array[:, 2::3] >> ((1 - byte) * 4))  & 0b1111)
    bayer_array = np.delete(bayer_array, np.s_[2::3], 1)
    return [bayer_array]

def open_pic(path):
    """Check that file exists, is a jpeg, and open it"""
    # Conform that the file exists 
    if not os.path.isfile(path):
        raise IOError('File not there man')    
    # Check that the files is a jpeg
    main_path, ext = os.path.splitect(path)
    extensions = ['jpeg','JPEG','jpg','JPG']
    if ext not in extensions:
        raise ValueError(
            'File extension is not compatible with routine Must be in {}'.format(
                extensions))
    with open(path, 'rb') as raw_file:
        # Read in the image as a binary file to read
        file_data = raw_file.read()
    return file_data
