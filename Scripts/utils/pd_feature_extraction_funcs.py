import pandas as pd
import matlab.engine as mat_eng
import matlab

Settings = {
    'Fs': 208.0,  # approximate sampling frequency deduced from the data
    'Fc_LowPassFilter': 10.0,
    # cut-off frequency used for low-pass filters: frequencies scale according to the sampling rate
    'Fc_HighPassFilter_AutoCorr': 1.0  # cut-off frequency used for high-pass filters for autocorrelation unbiased
}


def extract_all_features(df, matlab_eng, prefix_columns=None, output_df=None):
    if output_df is None:
        output_df = {}
    if prefix_columns is None:
        prefix_columns = {}
    rms_features = {}
    combination_features = {}

    # Converting data to matlab double
    data = df.to_numpy()
    mat_data = matlab.double(data.tolist())

    # extracting features using matlab functions
    rms_features = matlab_eng.extract_RMS_FirstDerivative(mat_data, Settings, rms_features)
    combination_features = matlab_eng.extract_CombinationFeaturesArticles(mat_data, Settings, combination_features)

    merged_features = prefix_columns

    # Merging features into one dictionary
    for key in rms_features.keys():
        merged_features[key] = [rms_features[key]]
    for key in combination_features.keys():
        merged_features[key] = [combination_features[key]]

    if len(output_df) < 1:
        output_df = pd.DataFrame(merged_features)
    else:
        output_df = pd.concat([output_df, pd.DataFrame(merged_features)], ignore_index=True)

    return output_df


def get_header_columns(record_path):
    file_name = record_path.split('/').pop(-1).split('.')[0]
    file_args = file_name.split('_')
    header_columns = {}
    record_id = file_args[0]
    record_medicine = 'N/A'
    record_state = file_args[1]
    record_hand = file_args[2]

    if len(file_args) > 3:
        record_medicine = file_args[2]
        record_hand = file_args[3]

    header_columns['ID'] = record_id
    header_columns['State'] = record_state
    header_columns['Hand'] = record_hand
    header_columns['Medication'] = record_medicine

    return header_columns