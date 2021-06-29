# Vladislav 16.06.21
# file control system
# remove files based on some rule in order to prevent overflow of file system

# import glob
import os
import shutil
import uuid
# from zipfile import ZipFile

RESULTS_DIR = 'results'
UPLOAD_DIR= 'results'

def create_uuid():
    return str(uuid.uuid4())


def create_dir_for_result(OUTPUT_DIR, uuid):
    full_output_dir_name = os.path.join(OUTPUT_DIR, uuid)
    full_output_dir_name = os.path.join(full_output_dir_name, RESULTS_DIR)
    os.mkdir(full_output_dir_name)
    return str(full_output_dir_name)


def make_uuid_dir(uuid):
    full_name_dir_uuid = os.path.join(UPLOAD_DIR, uuid)
    if not os.path.isdir(full_name_dir_uuid):
        os.mkdir(full_name_dir_uuid)
    return full_name_dir_uuid


