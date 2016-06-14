'''
Created on May 7, 2016

@author: lxh5147
'''
from text_file_util import TextFileUtil
from label_feature_map import LabelFeatureMap
from utilities import list_files
from  utilities import list_sub_directories

def convert_to_liblinear(lable_to_id_map, feature_name_id_map, label, training_input_file_path, feature_extractors, is_for_training = True):
    if is_for_training:
        if label in lable_to_id_map:
            label_id = lable_to_id_map[label]
        else:
            label_id = len(lable_to_id_map)
            lable_to_id_map[label] = label_id
    else:
        if label in lable_to_id_map:
            label_id = lable_to_id_map[label]
        else:
            label_id = None

    liblinear_instance = []
    liblinear_instance.append(str(label_id) if label_id is not None else "-1")
    features = {}
    for feature_extractor in feature_extractors:
        # extract features using each feature extractor
        f = TextFileUtil.open_file_read(training_input_file_path)
        for feature in feature_extractor.extract_features(f):
            if is_for_training:
                if feature.name in feature_name_id_map:
                    feature_id = feature_name_id_map[feature.name]
                else:
                    feature_id = len(feature_name_id_map) + 1
                    feature_name_id_map[feature.name] = feature_id
            else:
                if feature.name in feature_name_id_map:
                    feature_id = feature_name_id_map[feature.name]
                else:
                    feature_id = None
            # TODO: do we really support features from two extractors with the same feature name?
            if feature_id:
                if feature_id in features:
                    features[feature_id] += feature.value
                else:
                    features[feature_id] = feature.value
        f.close()

    for feature_id in sorted(features):
        liblinear_instance.append(" %s:%s" % (feature_id, features[feature_id]))
    
    return " ".join(liblinear_instance)

class Corpus(object):
    def __init__(self, input_file_path, lable_feature_map_file_path, feature_extractors):
        self._input_file_path = input_file_path
        self._lable_feature_map_file_path = lable_feature_map_file_path
        self._feature_extractors = feature_extractors

    def build(self, liblinear_output_file_path, is_for_training = True):
        f = TextFileUtil.open_file_read(self._input_file_path)
        liblinear_output_file = TextFileUtil.open_file_write(liblinear_output_file_path)
        if is_for_training:
            lable_to_id_map = {} 
            feature_name_id_map = {}
        else:
            lable_to_id_map , feature_name_id_map = LabelFeatureMap.load_label_feature_map(self._lable_feature_map_file_path)
        for line in f:
            line = line.rstrip('\n')
            label, training_input_file_path = line.split('\t')
            liblinear_instance = convert_to_liblinear(lable_to_id_map, feature_name_id_map, label, training_input_file_path, self._feature_extractors, is_for_training)
            TextFileUtil.write_file(liblinear_output_file, liblinear_instance)
        liblinear_output_file.close()
        f.close()
        if is_for_training:
            LabelFeatureMap.save_label_feature_map(lable_to_id_map, feature_name_id_map, self._lable_feature_map_file_path)

    @staticmethod
    def build_corpus_input_file(directory_root, corpus_output_file_path):
        '''
        directory_root: the root of files, if there are sub directories under the root, the name of sub directories will be category name 
        '''
        f = TextFileUtil.open_file_write(corpus_output_file_path)
        for input_file in list_files(directory_root):
            TextFileUtil.write_file(f, "UNK\t" + input_file)
        for sub_directory_name, sub_directory_path in list_sub_directories(directory_root):
            Corpus._build_corpus_input_file(sub_directory_path, sub_directory_name, f)
        f.close()

    @staticmethod
    def _build_corpus_input_file(cur_directory, category, output_file):
        for input_file in list_files(cur_directory):
            TextFileUtil.write_file(output_file, category + "\t" + input_file)

