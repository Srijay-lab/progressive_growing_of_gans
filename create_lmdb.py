import cv2
import lmdb
import numpy as np
import os
import argparse
import glob

def store_many_lmdb(images_list, save_path):
    # number of images in our folder
    num_images = len(images_list)
    # all file sizes
    file_sizes = [os.path.getsize(item) for item in images_list]
    # the maximum file size index
    max_size_index = np.argmax(file_sizes)
    # maximum database size in bytes
    map_size = num_images * cv2.imread(images_list[max_size_index]).nbytes * 10

    # create lmdb environment
    env = lmdb.open(save_path, map_size=map_size)

    # start writing to environment
    with env.begin(write=True) as txn:
        for i, image in enumerate(images_list):
            with open(image, "rb") as file:
                # read image as bytes
                data = file.read()
                # get image key
                key = f"{i:08}"
                # put the key-value into database
                txn.put(key.encode("ascii"), data)

                # close the environment
    env.close()

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='D:/warwick/datasets/digestpath/processed/images')
parser.add_argument('--output', default='D:/warwick/datasets/digestpath/processed/lmdb_dataset_for_progan')
a = parser.parse_args()

input_paths = glob.glob(os.path.join(a.input,"*.png"))

store_many_lmdb(input_paths,a.output)

# python create_lmdb.py --path D:/warwick/datasets/digestpath/processed/images --output D:/warwick/datasets/digestpath/processed/lmdb_dataset_for_progan