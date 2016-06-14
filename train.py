'''
Created on Jun 4, 2016

@author: lxh5147
'''
from utilities import run
from convert_to_liblinear import Corpus
from compact_model import compact
import argparse
import os
from feature_extractor import feature_extractors

# update it to your local install
TRAIN_CMD = "/home/lxh5147/liblinear-2.1/train"

def train(model_file_path, lable_feature_map_file_path, feature_extractors, input_file_path):
    # build corpus for evaluation
    un_compacted_model_file_path = model_file_path + ".tmp"
    un_compacted_lable_feature_map_file_path = lable_feature_map_file_path + ".tmp"
    liblinear_file_path = input_file_path + ".liblinear"
    corpus = Corpus(input_file_path, un_compacted_lable_feature_map_file_path, feature_extractors)
    corpus.build(liblinear_file_path, is_for_training = True)
    # train model 
    # train -s 6 -e 0.01 -c 3.0 -p 0.1 -B -1 -W /gpfs/nlu/data/users/xiaoliu/svn/git_root/dragon-mobile-assistant-nlu-switch/training/hertz_nlucore_main_lxh_prediction_annotator_feature_extractor_with_david_model/domain_classifier/cross_validation/fold_0/train_liblinear/convert_to_liblinear.weight.liblinear /gpfs/nlu/data/users/xiaoliu/svn/git_root/dragon-mobile-assistant-nlu-switch/training/hertz_nlucore_main_lxh_prediction_annotator_feature_extractor_with_david_model/domain_classifier/cross_validation/fold_0/train_liblinear/convert_to_liblinear.train.liblinear /gpfs/nlu/data/users/xiaoliu/svn/git_root/dragon-mobile-assistant-nlu-switch/training/hertz_nlucore_main_lxh_prediction_annotator_feature_extractor_with_david_model/domain_classifier/cross_validation/fold_0/train_liblinear/model.liblinear
    run(TRAIN_CMD + " -s 6 -e 0.01 -c 3.0 -p 0.1 -B -1 %s %s" % (liblinear_file_path, un_compacted_model_file_path))
    # compact model
    compact(un_compacted_lable_feature_map_file_path, un_compacted_model_file_path, lable_feature_map_file_path, model_file_path)
    os.remove(un_compacted_model_file_path)
    os.remove(un_compacted_lable_feature_map_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Train classifier with all training files organized as sub folders under a root directory')
    parser.add_argument('train_file_root', metavar = 'TRAIN_FILE_ROOT', help = 'root directory of all training files, organized into sub directories and with sub directory name as the category name')
    parser.add_argument('--model', help = 'file path into which to write the trained model')
    parser.add_argument('--map', help = 'category and feature map file path')
    parser.add_argument('--train_input_file', nargs = '?', help = 'generated train input file')
    args = parser.parse_args()
    train_input_file = args.train_input_file
    if train_input_file is None:
        train_input_file = "train.input"
    Corpus.build_corpus_input_file(args.train_file_root, train_input_file)
    train(args.model, args.map, feature_extractors, train_input_file)
