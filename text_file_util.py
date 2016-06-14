'''
Created on May 7, 2016

@author: lxh5147
'''

import codecs

class TextFileUtil(object):
    '''
    Represents a text file helper that defines some utility functions to operate on text files
    '''
    @staticmethod
    def open_file_read(input_file_path):
        return codecs.open(input_file_path, "r", "utf-8")

    @staticmethod
    def open_file_write(output_file_path):
        return codecs.open(output_file_path, "w", "utf-8")
    
    @staticmethod
    def write_file(output_file, string):
        output_file.write(string + "\n")