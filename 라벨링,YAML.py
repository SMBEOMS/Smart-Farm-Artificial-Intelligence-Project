import os
import json
import yaml

# JSON 파일을 처리하여 YAML 데이터에 추가하는 함수
def process_json_file(file_path, yaml_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        for annotation in json_data['annotations']:
            category_id = annotation['category_id']
            if 'name' in json_data['categories'][category_id] and json_data['categories'][category_id]['name'] == '과실':
                crops = json_data['images'].get('crops')
                kind_type = json_data['images'].get('kind_type')
                growth_stage = json_data['images'].get('growth_stage')

                if crops is not None and kind_type is not None and growth_stage is not None:
                    bbox = annotation['bbox']
                    label = f"{crops}_{kind_type}_{growth_stage}"
                    yaml_data['annotations'].append({'bbox': bbox, 'label': label})

# 폴더 내의 모든 JSON 파일을 처리합니다.
def process_folder(folder_path, yaml_data):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                process_json_file(file_path, yaml_data)

# 처리할 폴더의 최상위 경로를 지정합니다.
top_folder = 'TL_2.설향1'

# YAML 데이터를 초기화합니다.
yaml_data = {'annotations': []}

# 최상위 폴더 내의 모든 JSON 파일을 처리합니다.
process_folder(top_folder, yaml_data)

# YAML 파일로 출력합니다.
with open('output.yaml', 'w') as f:
    yaml.dump(yaml_data, f)
