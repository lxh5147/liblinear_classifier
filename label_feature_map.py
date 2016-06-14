'''
Created on May 7, 2016

@author: lxh5147
'''
from text_file_util import TextFileUtil

class LabelFeatureMap(object):
    @staticmethod
    def save_label_feature_map(lable_to_id_map, feature_name_id_map, lable_feature_map_output_file_path):
        f = TextFileUtil.open_file_write(lable_feature_map_output_file_path)
        # write the label
        for label, label_id in lable_to_id_map.items():
            TextFileUtil.write_file(f, "%s\t%s" % (label, label_id))
        # one blank line
        TextFileUtil.write_file(f, "")
        # write feature
        for feature_name, feature_id in feature_name_id_map.items():
            TextFileUtil.write_file(f, "%s\t%s" % (feature_name, feature_id))
        f.close()

    @staticmethod
    def load_label_feature_map(lable_feature_map_input_file_path):
        lable_to_id_map = {}
        feature_name_id_map = {}
        f = TextFileUtil.open_file_read(lable_feature_map_input_file_path)
        for line in f:
            line = line.rstrip('\n')
            if not line:
                break
            label, label_id = line.split('\t')
            label_id = int(label_id)
            lable_to_id_map[label] = label_id

        for line in f:
            line = line.rstrip('\n')
            if not line:
                break
            feature_name, feature_id = line.split('\t')
            feature_id = int(feature_id)
            feature_name_id_map[feature_name] = feature_id
        f.close()

        return lable_to_id_map, feature_name_id_map

    @staticmethod
    def load_label_map(lable_feature_map_input_file_path):
        lable_to_id_map = {}
        f = TextFileUtil.open_file_read(lable_feature_map_input_file_path)
        for line in f:
            line = line.rstrip('\n')            
            if not line:
                break
            label, label_id = line.split('\t')
            label_id = int(label_id)
            lable_to_id_map[label] = label_id
        return lable_to_id_map