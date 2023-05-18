import os
import json

def get_growth_stage_mapping(growth_stage, category_name):
    if category_name == "과실":
        mapping = {
            "정식기": 0,
            "출뢰기": 1,
            "개화기": 2,
            "과실비대기": 3,
            "수확기": 4
        }
    elif category_name == "화방":
        mapping = {
            "정식기": 5,
            "출뢰기": 6,
            "개화기": 7,
            "과실비대기": 8,
            "수확기": 9
        }
    elif category_name == "잎":
        mapping = {
            "정식기": 10,
            "출뢰기": 11,
            "개화기": 12,
            "과실비대기": 13,
            "수확기": 14
        }
    elif category_name == "줄기":
        mapping = {
            "정식기": 15,
            "출뢰기": 16,
            "개화기": 17,
            "과실비대기": 18,
            "수확기": 19
        }
    else:
        return -1
    
    return mapping.get(growth_stage, -1)  # 매핑되지 않은 경우 -1을 반환

def convert_to_yolo_format(json_file_path, txt_folder_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    image_info = data['images']
    image_width = int(image_info['width'])
    image_height = int(image_info['height'])
    growth_stage = image_info['growth_stage']

    if 'annotations' not in data:
        return

    annotations = data['annotations']
    
    for annotation in annotations:
        category_id = annotation['category_id']
        category_name = data['categories'][category_id]['name']
        bbox = annotation['bbox']

        growth_stage_id = get_growth_stage_mapping(growth_stage, category_name)

        if growth_stage_id == -1:
            continue  # 유효하지 않은 growth_stage인 경우 건너뜁니다.

        x_center = (bbox[0] + bbox[2] / 2) / image_width
        y_center = (bbox[1] + bbox[3] / 2) / image_height
        width = bbox[2] / image_width
        height = bbox[3] / image_height

        txt_file_name = os.path.splitext(os.path.basename(json_file_path))[0] + '.txt'  # JSON 파일 이름에서 확장자를 제거하고 .txt로 변경
        txt_file_path = os.path.join(txt_folder_path, txt_file_name)
        line = f"{growth_stage_id} {x_center} {y_center} {width} {height}\n"

        with open(txt_file_path, 'a', encoding='utf-8') as txt_file:
            txt_file.write(line)

# 기본 폴더 경로
base_folder_path = 'C:\\sul'

for i in range(1, 11):
    json_folder_name = f'TL_2.설향{i}\\TL_2.설향{i}'
    json_folder_path = os.path.join(base_folder_path, json_folder_name)
    txt_folder_name = f'TL_2.설향{i}_txt'
    txt_folder_path = os.path.join(base_folder_path, txt_folder_name)

    # 폴더가 없으면 생성합니다.
    if not os.path.exists(txt_folder_path):
        os.makedirs(txt_folder_path)

    # JSON 파일들을 변환하여 YOLO 형식의 텍스트 파일로 저장합니다.
    json_files = os.listdir(json_folder_path)
    for json_file in json_files:
        json_file_path = os.path.join(json_folder_path, json_file)
        convert_to_yolo_format(json_file_path, txt_folder_path)
