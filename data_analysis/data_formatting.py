import os
import pandas as pd
import json
import re

value_map_size = {
            'sss': 1,
            'ss': 2,
            's': 3,
            'm': 4,
            'l': 5,
            'xl': 6,
            'xxl': 7,
            'xxxl':8,
            'xxxxl': 9
        }

value_map_colour = {
    'black': 1,
    'green-saturated': 2,
    'cyan-saturated': 3,
    'red-saturated': 4,
    'red-light': 5,
    'red-muted': 6,
    'red-dark': 7,
    'orange-saturated': 8,
    'orange-light': 9,
    'orange-muted': 10,
    'orange-dark': 11,
    'yellow-saturated': 12,
    'yellow-light': 13,
    'yellow-muted': 14,
    'yellow-dark': 15,
    'chartreuse-saturated': 16,
    'chartreuse-light': 17,
    'chartreuse-muted': 18,
    'chartreuse-dark': 19,
    'green-light': 20,
    'green-muted': 21,
    'green-dark': 22,
    'cyan-light': 23,
    'cyan-muted': 24,
    'cyan-dark': 25,
    'blue-saturated': 26,
    'blue-light': 27,
    'blue-muted': 28,
    'blue-dark': 29,
    'purple-saturated': 30,
    'purple-light': 31,
    'purple-muted': 32,
    'purple-dark': 33,
    # beigās vienādas vērtības pēc FFFFFF iznāca šiem pēdējiem 4.
    'gray-dark': 34,
    'gray-medium': 34,
    'gray-light': 34,
    'white': 34,
}

value_map_shape = {}

for i in range(1, 11):
    value_map_shape[f'img/blob ({i}).svg'] = 'bouba'

value_map_shape['img/Kiki.png'] = 'kiki'
for i in range(2,11):
    value_map_shape[f'img/Kiki{i}.png'] = 'kiki'


base_input_folders = ["individual", "lab_tests", "online_tests"]
columns_to_drop = ["stimulus", "response", "trial_type", "plugin_version", "time_elapsed"]

for folder in base_input_folders:
    input_path = os.path.join("data", folder)
    output_folder = os.path.join("data", f"{folder}_combined")
    combined_filename = "combined_output.csv"
    participants_filename = "participants.csv"

    csv_files = [f for f in os.listdir(input_path) if f.endswith('.csv')]
    if not csv_files:
        print(f"Mapē '{input_path}' nav CSV failu")
        continue

    dataframes = []
    participants_data = {}

    for file in csv_files:
        file_path = os.path.join(input_path, file)
        df = pd.read_csv(file_path)

        match = re.search(r'_(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d+Z)', file)
        submission_time = match.group(1) if match else None

        if 'demographics' in df.columns and 'participant_id' in df.columns:
            try:
                demo = json.loads(df.loc[0, 'demographics'])
                age = demo.get('age')
                gender = demo.get('gender')
                education = demo.get('education')
                hobbies = demo.get('hobbies')
                pid = df.loc[0, 'participant_id']
                participants_data[pid] = {
                    'participant_id': pid,
                    'age': age,
                    'gender': gender,
                    'education': education,
                    'hobbies': hobbies,
                    'submission_time': submission_time
                }
                df['age'] = [age] * len(df)
                df['gender'] = [gender] * len(df)
                df['education'] = [education] * len(df)
                df['hobbies'] = [hobbies] * len(df)
                df['submission_time'] = [submission_time] * len(df)
            except Exception as e:
                print(f"Nav ok ar demogrāfiju failā: {file}: {e}")
                df['age'] = df['gender'] = df['education'] = df['hobbies'] = df['submission_time'] = None
        else:
            df['age'] = df['gender'] = df['education'] = df['hobbies'] = df['submission_time'] = None

        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        if 'demographics' in df.columns:
            df = df.drop(columns=['demographics'])

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.insert(0, 'row_number', range(1, len(combined_df) + 1))
    participants_df = pd.DataFrame(participants_data.values())

    os.makedirs(output_folder, exist_ok=True)
    combined_df.to_csv(os.path.join(output_folder, combined_filename), index=False)
    participants_df.to_csv(os.path.join(output_folder, participants_filename), index=False)

    print(f"Apvienoja {folder}: {len(combined_df)} rindu saglabātas uz '{combined_filename}', {len(participants_df)} dalībnieki uz '{participants_filename}'")

    # sadalīsim pa testu tipiem un lietosim atbilstošās vērtības, jeb skalas izveidosim
    for test_type in combined_df['test'].unique():
        df_type = combined_df[combined_df['test'] == test_type].copy()

        if test_type == 'size':
            df_type['left_item'] = df_type['left_item'].map(value_map_size)
            df_type['right_item'] = df_type['right_item'].map(value_map_size)
            df_type['clicked_item'] = df_type['clicked_item'].map(value_map_size)

        elif test_type == 'colour':
            df_type['left_item'] = df_type['left_item'].map(value_map_colour)
            df_type['right_item'] = df_type['right_item'].map(value_map_colour)
            df_type['clicked_item'] = df_type['clicked_item'].map(value_map_colour)

        elif test_type == 'shape':
            df_type['left_item'] = df_type['left_item'].map(value_map_shape)
            df_type['right_item'] = df_type['right_item'].map(value_map_shape)
            df_type['clicked_item'] = df_type['clicked_item'].map(value_map_shape)

        output_file = os.path.join(output_folder, f"{test_type}.csv")
        df_type.to_csv(output_file, index=False)