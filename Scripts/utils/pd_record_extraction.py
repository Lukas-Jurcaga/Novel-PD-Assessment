import os
import pandas as pd

dataset_dir = '../../Study/Data/labelled/'
records_paths = os.listdir(dataset_dir)


def get_all_ids():
    dataset_ids = []
    for records_path in records_paths:
        records_labels = records_path.split('_')
        dataset_ids.append(records_labels[0])
    return dataset_ids

def get_record_set(id='', state='', med='', hand=''):
    path_set = []
    for record_path in records_paths:
        record_labels = record_path.split('.csv')[0].split('_')
        if len(record_labels) > 3 and state != 'healthy':
            if (record_labels[0] == id or id == '') and (record_labels[2] == med or med == '') and (
                    record_labels[3] == hand or hand == ''):
                path_set.append(dataset_dir + record_path)
        if len(record_labels) <= 3 and state != 'pd' and med == '':
            if (record_labels[0] == id or id == '') and (record_labels[2] == hand or hand == ''):
                path_set.append(dataset_dir + record_path)
    return path_set


def get_record_indv_groupings_set(state='', med='', hand=''):
    all_ids = get_all_ids()
    indv_groupings = []
    for indv_id in all_ids:
        grouping = get_record_set(indv_id, state=state, med=med, hand=hand)
        if len(grouping) > 0:
            indv_groupings.append(grouping)
    return indv_groupings


def get_record_df(path, columns):
    return pd.read_csv(path, usecols=columns)
