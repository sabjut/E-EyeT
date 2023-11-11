import json
import pandas as pd
import os

useless_cols = ['afe_left_m_0_6', 'afe_left_m_0_7', ]

for i in range(8):
    useless_cols.append('auxSensors_tempEt_n_' + str(i))

transform_col_names = {
    'auxSensors_tempEt_v_0': 'auxSensors_tempEt_v_left_0',
    'auxSensors_tempEt_v_1': 'auxSensors_tempEt_v_left_1',
    'auxSensors_tempEt_v_2': 'auxSensors_tempEt_v_left_2',
    'auxSensors_tempEt_v_3': 'auxSensors_tempEt_v_left_3',
    'auxSensors_tempEt_v_4': 'auxSensors_tempEt_v_right_0',
    'auxSensors_tempEt_v_5': 'auxSensors_tempEt_v_right_1',
    'auxSensors_tempEt_v_6': 'auxSensors_tempEt_v_right_2',
    'auxSensors_tempEt_v_7': 'auxSensors_tempEt_v_right_3',
    'afe_left_i_0': 'afe_left_ticktime',
    'afe_left_i_1': 'afe_left_timestamp',
    'afe_left_i_2': 'afe_left_status',
    'afe_left_i_3': 'afe_left_counter',
    'afe_right_i_0': 'afe_right_ticktime',
    'afe_right_i_1': 'afe_right_timestamp',
    'afe_right_i_2': 'afe_right_status',
    'afe_right_i_3': 'afe_right_counter',
    'auxSensors_lightAmbient_s_0': 'auxSensors_lightAmbient_status_0',
    'auxSensors_lightAmbient_s_1': 'auxSensors_lightAmbient_status_1',
    'auxSensors_lightAmbient_s_2': 'auxSensors_lightAmbient_status_2',
    'auxSensors_lightAmbient_s_3': 'auxSensors_lightAmbient_status_3',
}

def flatten_json(row):
    data = row
    out = dict()
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for i,a in enumerate(x):
                default_name = name + str(i) + '_'
                if (name == 'afe_'):
                    if (i == 0):
                        default_name = name + 'left_'
                    else:
                        default_name = name + 'right_'
                flatten(a, default_name)
        else:

            out[name[:-1]] = x

    flatten(data)
    return out

def afe_to_df(current_path):
    with open(current_path, 'r') as file:
        data = json.load(file)

    flattened_data = [flatten_json(item) for item in data]

    df = pd.DataFrame(flattened_data)

    # dropping irrelevant data
    df.drop(columns=useless_cols, inplace=True)

    # renaming columns
    df.rename(columns=transform_col_names, inplace=True)

    return df


def fetch_full_aef_df(dir_path):
    prefix = 'AFE'

    files_starting_with_prefix = [filename for filename in os.listdir(dir_path) if filename.startswith(prefix)]


    dfs = []
    df = None

    for ele in files_starting_with_prefix:
        current_path = dir_path + ele
        cur_df = afe_to_df(current_path)
        dfs.append(cur_df)
        if df is None:
            df = cur_df
        else:
            df = pd.concat([df, cur_df])

    return df