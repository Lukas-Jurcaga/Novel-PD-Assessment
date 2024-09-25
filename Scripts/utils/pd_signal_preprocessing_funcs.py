import pandas as pd


def get_light_recordings(df):
    light_recordings = {'start_index': [], 'end_index': [], 'start_time': [], 'end_time': [], 'length': []}
    light_started = False
    previous_row = None
    for index, row in df.iterrows():
        if light_started:
            if row['l'] == 0 or index == len(df) - 1:
                light_recordings['end_index'].append(index - 1)
                light_recordings['end_time'].append(previous_row['t'])
                light_recordings['length'].append(
                    previous_row['t'] - light_recordings['start_time'][len(light_recordings['start_time']) - 1])
                light_started = False
        else:
            if row['l'] == 1:
                light_recordings['start_time'].append(row['t'])
                light_recordings['start_index'].append(index)
                light_started = True
        previous_row = row
    return pd.DataFrame(light_recordings)


def get_all_light_intervals_index(df):
    on_light_intervals = get_light_recordings(df)
    all_light_intervals_df = pd.DataFrame({'light': []})
    prev_index = 0
    for index, row in on_light_intervals.iterrows():
        on_light_interval = pd.DataFrame({'light': [1], 'start_index': row['start_index'], 'end_index': row['end_index']})
        # on_light_interval = row.head(2).insert(loc=0, column='light', value=['1'])
        # if not index >= len(on_light_intervals) - 1:
        if prev_index > 0:
            off_light_interval = pd.DataFrame({'light': [0], 'start_index': [prev_index], 'end_index': [row['start_index'] - 1]})
            all_light_intervals_df = pd.concat([all_light_intervals_df, off_light_interval], axis=0)
        all_light_intervals_df = pd.concat([all_light_intervals_df, on_light_interval])
        prev_index = row['end_index'] + 1
    return all_light_intervals_df.astype(int).reset_index(drop=True)


def is_time_long_enough(record, comparison):
    return record['length'] > comparison['length'] - comparison['length'] * 0.01


def base_time(df):
    times = df['t'].tolist()
    first = times[0]
    for i in range(len(times)):
        times[i] -= first
    dropped_df = df.drop('t', axis=1)
    new_df = pd.concat([pd.DataFrame({'t': times}), dropped_df], axis=1)
    return new_df
