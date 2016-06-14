'''
Created on May 7, 2016

@author: lxh5147
'''

from __future__ import print_function
import os.path
import codecs
import sys
import argparse

'''
This script removes any feature with all zero weights from lib linear model. It takes as input the model file and feature map file, and outputs the updated model file and feature map file. 
'''

# output info for debug/log purpose
class MESSAGE_LEVEL:
    DEBUG = 0 
    INFO = 1
    WARNING = 2
    ERROR = 3
    CUR_LEVEL = 2

MESSAGES = ["DEBUG", "INFO", "WARNING", "ERROR"]    

MESSAGE_LEVEL.CUR_LEVEL = MESSAGE_LEVEL.ERROR 

def output_info(msg, level = MESSAGE_LEVEL.DEBUG):    
    if level < MESSAGE_LEVEL.DEBUG : level = MESSAGE_LEVEL.DEBUG
    if level > MESSAGE_LEVEL.ERROR : level = MESSAGE_LEVEL.ERROR

    if level >= MESSAGE_LEVEL.CUR_LEVEL:
        try:
            full_message = "%s\t%s" % (MESSAGES[level], msg)
            if (level >= MESSAGE_LEVEL.ERROR):
                print (full_message, file = sys.stderr)
            else:
                print (full_message)
        except:
            pass


def get_feature_map_header(feature_map_file):
    '''
    read feature map file header
    '''
    assert(feature_map_file)
    feature_map_header = []
    while True:
        line = feature_map_file.readline().rstrip('\n')
        feature_map_header.append(line)                
        if not line:
            break        
    return feature_map_header

def write_feature_map_header(updated_feature_map_file, feature_map_header):
    '''
    write feature map header
    '''
    assert(updated_feature_map_file)
    assert(feature_map_header)
    for line in feature_map_header:
        print(line, file = updated_feature_map_file) 

def get_feature_map_entry(feature_map_file):
    '''
    read one feature map entry
    '''
    assert(feature_map_file)    
    line = feature_map_file.readline()
    if not line:
        return None
    line = line.rstrip('\n')
    if not line:
        return None
    return line.split('\t')[0]
    
def write_feature_map_entry(updated_feature_map_file, feature_map_entry, index):
    '''
    write one feature map entry
    '''
    assert(updated_feature_map_file)
    # index starts from 1
    print('\t'.join([feature_map_entry, str(index)]), file = updated_feature_map_file)
    

def get_model_header(model_file):
    '''
    read model header
    '''
    assert(model_file)
    model_header = []
    while True:
        line = model_file.readline().rstrip('\n')
        model_header.append(line)
        if line == "w":
            break
    return model_header

def write_model_header(updated_model_file, model_header):
    '''
    write model header
    '''
    assert(updated_model_file)
    assert(model_header)
    for line in model_header:
        print(line, file = updated_model_file) 

def get_model_weight(model_file):
    '''
    read weight feature
    '''
    assert(model_file)
    line = model_file.readline()
    if not line:
        return None
    line = line.rstrip('\n')
    if not line:
        return None
    return line
    
def is_zero_weight(weight):
    '''
    if all weights of a feature are zero; a feature has N weights where N is the number of labels
    '''
    assert(weight)
    for c in weight:
        if c == ' ':
            continue
        if c != '0':
            return False
    return True
    
    # parts = weight.split()
    # return all(x == '0' for x in parts)

def write_model_weight(updated_model_file, weight):
    '''
    write back weights of one one feature
    '''
    assert(updated_model_file)
    assert(weight)
    print(weight, file = updated_model_file)
    
def is_file_exists(file_path):
    '''
    if the target file exists
    '''
    if not os.path.exists(file_path):
        return False    
    return os.path.isfile(file_path)

def compact(input_feature_map_file, input_model_file, output_updated_feature_map_file, output_updated_model_file):
    '''
    1) remove any feature whose weights are all zeros from both feature map file and model file
    2) update feature index in feature map file
    3) update feature number in model file
    '''
    assert(input_feature_map_file)
    assert(is_file_exists(input_feature_map_file))
    assert(is_file_exists(input_model_file))
    
    # first scan to get the number of features with any non-zero weight
    total_feature_with_non_zero_weight = 0
    # no need to open the model file as utf-8 which requires more CPU time
    with open(input_model_file, 'r') as model_file:
        model_header = get_model_header(model_file)
        while True:
            weight = get_model_weight(model_file)
            if not weight:                
                break
            if not is_zero_weight(weight):
                total_feature_with_non_zero_weight += 1 
           
    assert(model_header)
    model_header[3] = "nr_feature " + str(total_feature_with_non_zero_weight)
    output_info("Updated model header=" + "\n".join(model_header), MESSAGE_LEVEL.DEBUG)
    # first feature has 1 as its index             
    feature_index = 1
    with codecs.open(input_feature_map_file, 'r', encoding = 'utf8') as feature_map_file:
        with open(input_model_file, 'r') as model_file:
            with codecs.open(output_updated_feature_map_file, 'w', encoding = 'utf8') as updated_feature_map_file:
                with open(output_updated_model_file, 'w') as updated_model_file:
                            
                    feature_map_header = get_feature_map_header(feature_map_file)
                    # skip model header
                    get_model_header(model_file)
                    # write feature map header and the updated model header
                    write_feature_map_header(updated_feature_map_file, feature_map_header)
                    write_model_header(updated_model_file, model_header)
                    while True:
                        weight = get_model_weight(model_file)
                        feature_map_entry = get_feature_map_entry(feature_map_file)
                        if not weight:
                            break
                        assert(feature_map_entry)
                        # only write the feature with any non zero weight into feature map file and model file
                        if not is_zero_weight(weight):
                            write_model_weight(updated_model_file, weight)
                            write_feature_map_entry(updated_feature_map_file, feature_map_entry, feature_index)
                            feature_index += 1 
                        else: 
                            output_info ("remove feature with all zero weights: " + feature_map_entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Compact liblinear model by removing features without any non-zero weight')  
    

    parser.add_argument('--input_model_file', required = True, metavar = 'INPUT_MODEL_FILE',
                        help = 'The input liblinear model file.')
    
    parser.add_argument('--input_feature_map_file', required = True, metavar = 'INPUT_FEATURE_MAP_FILE',
                        help = 'The input liblinear feature map file.')
   
    parser.add_argument('--output_model_file', metavar = 'OUTPUT_MODEL_FILE',
                        help = 'The output liblinear model file.')
    
    parser.add_argument('--output_feature_map_file', metavar = 'OUTPUT_FEATURE_MAP_FILE',
                        help = 'The output liblinear feature map file.')
   
    
    
    args = parser.parse_args()
    
    output_info(args , MESSAGE_LEVEL.DEBUG)
    
    input_feature_map_file = args.input_feature_map_file
    input_model_file = args.input_model_file
    output_updated_feature_map_file = args.output_feature_map_file
    output_updated_model_file = args.output_model_file
        
    def check_input_files():        
        if not is_file_exists(input_feature_map_file):
            print ("Error: Input feature map file {0} does not exist".format(input_feature_map_file), file = sys.stderr)
            sys.exit(1)
        if not is_file_exists(input_model_file):
            print ("Error: Input model file {0} does not exist".format(input_model_file), file = sys.stderr)
            sys.exit(1)                    

    
    check_input_files()
    
    if not output_updated_feature_map_file:
        output_updated_feature_map_file = input_feature_map_file + ".compact"
    if not output_updated_model_file:
        output_updated_model_file = input_model_file + ".compact"
    
    compact(input_feature_map_file, input_model_file, output_updated_feature_map_file, output_updated_model_file)
