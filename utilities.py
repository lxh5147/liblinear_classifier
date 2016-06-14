'''
Created on Jun 5, 2016

@author: lxh5147
'''

import subprocess
from os import listdir
from os.path import isfile, join

def run(cmd):
    return subprocess.check_output(cmd, shell = True)

def list_files(file_path_root):
    for f in listdir(file_path_root):
        cur_file = join(file_path_root, f)
        if isfile(cur_file):
            yield cur_file

def list_sub_directories(file_path_root):
    for f in listdir(file_path_root):
        cur_directory = join(file_path_root, f)
        if not isfile(cur_directory):
            yield (f, cur_directory)
