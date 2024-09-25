import os
import pandas as pd

results_root_dir = '../../Results/'


def get_all_avg_results_paths():
    all_names = os.listdir(results_root_dir + 'average/')
    all_results_paths = []
    for name in all_names:
        all_results_paths.append(results_root_dir + 'average/' + name)
    return all_results_paths


def get_all_fold_scores_paths(dataset_type):
    all_names = os.listdir(results_root_dir + 'folds/' + dataset_type + '/')
    all_scores_paths = []
    for name in all_names:
        all_scores_paths.append(results_root_dir + 'folds/' + dataset_type + '/' + name)
    return all_scores_paths



def find_best_model(results_df):
    best_model = None
    best_model_df = None
    best_model_aggr_score = 0
    for index, row in results_df.iterrows():
        curr_model_aggr_score = (row['Accuracy'] + row['F1'] + row[
            'Specificity']) / 3
        if curr_model_aggr_score > best_model_aggr_score:
            best_model_aggr_score = curr_model_aggr_score
            best_model = row['Model']
            best_model_df = row
    best_model_df = pd.DataFrame(best_model_df).transpose()
    best_model_df['AS'] = best_model_aggr_score
    return best_model, best_model_df