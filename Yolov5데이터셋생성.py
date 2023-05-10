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
    

    # JSON 파일 경로에서 파일 이름을 추출합니다.
    json_file_name = os.path.basename(json_file_path)
    # 파일 이름에서 확장자를 제거한 후 .txt 확장자를 추가합니다.
    txt_file_name = os.path.splitext(json_file_name)[0] + '.txt'
    # TXT 파일의 전체 경로를 생성합니다.
    txt_file_path = os.path.join(txt_folder_path, txt_file_name)
    
    # JSON 파일을 변환하여 TXT 파일에 저장합니다.
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        image_info = data['images']
        image_width = int(image_info['width'])
        image_height = int(image_info['height'])
        growth_stage = image_info['growth_stage']

        if 'annotations' not in data:
            return

        annotations = data['annotations']

        with open(txt_file_path, 'w') as f:
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

                line = f"{growth_stage_id} {x_center} {y_center} {width} {height}\n"
                f.write(line)

# JSON 파일이 들어있는 상위 폴더 경로
parent_folder_path = 'C:\\sull'

# 결과를 저장할 폴더 경로
result_folder_path = 'C:\\sull\\Result'

# 상위 폴더 안의 모든 폴더를 검사합니다.
for folder_name in os.listdir(parent_folder_path):
    folder_path = os.path.join(parent_folder_path, folder_name)
    
    # TL_2.설향* 폴더인지 확인합니다.
    if folder_name.startswith('TL_2.설향'):
        # TL_2.설향* 폴더 내부의 폴더를 검사합니다.
        for inner_folder_name in os.listdir(folder_path):
            inner_folder_path = os.path.join(folder_path, inner_folder_name)
            
            # TL_2.설향* 폴더 내부의 TL_2.설향* 폴더인지 확인합니다.
            if inner_folder_name.startswith('TL_2.설향'):
                # 결과를 저장할 폴더를 생성합니다.
                result_folder_name = f"Result_{inner_folder_name}"
                result_folder_path = os.path.join(parent_folder_path, result_folder_name)
                os.makedirs(result_folder_path, exist_ok=True)

                # TXT 파일 변환 및 저장
                for file_name in os.listdir(inner_folder_path):
                    if file_name.endswith('.json'):
                        json_file_path = os.path.join(inner_folder_path, file_name)
                        convert_to_yolo_format(json_file_path, result_folder_path)

