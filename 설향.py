import glob
import json
import csv
import os

# CSV 파일에 저장할 데이터 필드 이름
fields = ["crops", "kind_type", "growth_stage","farm_id", "receive_date","ti_value", "hi_value", "ci_value", "ir_value","tl_value", "ei_value",
           "pl_value","sr_value", "cl_value", "el_value", "hl_value", "pi_value", "rp_value"]

# JSON 파일들의 데이터를 저장할 리스트
data_list = []

# JSON 파일들을 자동으로 처리합니다.
for filename in glob.glob("C:/sul/TL_2.설향*/TL_2.설향*/*.json", recursive=True):
    with open(filename, encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
            image_data = data["images"]
            env = data["envrionments"][0] # 첫번째 환경 데이터만 사용
            # 필요한 데이터를 추출하여 리스트에 추가합니다.
            row = [image_data.get("crops"), image_data.get("kind_type"), image_data.get("growth_stage"),
                   env.get("farm_id"), env.get("receive_date"), env.get("ti_value"), env.get("hi_value"), env.get("ci_value"),
                   env.get("ir_value")]
            for field in ["tl_value", "ei_value","pl_value","sr_value", "cl_value", "el_value", "hl_value", "pi_value", "rp_value"]:
                row.append(env.get(field, ""))
            data_list.append(row)
        except KeyError:
            print(f"Error: {filename} does not have 'envrionments' key")

# 리스트를 CSV 파일로 저장합니다.
output_file = os.path.join(os.getcwd(), "output.csv") 
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    writer.writerows(data_list)
