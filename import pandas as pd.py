import torch
import torchvision.transforms as T
from PIL import Image
import pandas as pd
import csv
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

# 이미지 전처리 함수
transform = T.Compose([
    T.Resize(640),
    T.ToTensor(),
    T.ToPILImage()  # 이미지를 PIL 이미지로 변환
])

def detect_objects(image_path):
    # 이미지 로드 및 전처리
    image = Image.open(image_path)
    image = transform(image)

    # 이미지를 모델에 입력하여 객체 감지
    results = model(image)

    # 감지된 객체 정보 추출
    detections = results.pandas().xyxy[0]

    # 객체 정보를 DataFrame으로 변환
    df = pd.DataFrame(detections)

    # confidence를 소수에서 정수로 변환하고 % 기호 추가
    df['confidence'] = (df['confidence'] * 100).astype(int).astype(str) + '%'

    # sul로 시작하는 name을 '설향'으로, geum으로 시작하는 name을 '금실'로 분류하여 strawberry_type 열에 추가
    df['strawberry_type'] = df['name'].apply(lambda x: f"sul_{x[-1]}" if x.startswith('sul') else f"geum_{x[-1]}" if x.startswith('geum') else '')

    # 정확도를 기준으로 내림차순으로 정렬
    df = df.sort_values(by='confidence', ascending=False)

    # 열 순서 변경

    df = df[['name', 'strawberry_type', 'class', 'confidence']]

    # DataFrame을 CSV 파일로 저장
    csv_path = 'detection_results1.csv'
    df.to_csv(csv_path, index=False)

    return csv_path

# 이미지 경로 설정
image_path = 'test.jpg'

# 객체 감지 및 결과 저장
csv_path = detect_objects(image_path)
print(f"객체 감지 결과가 {csv_path}에 저장되었습니다.")

# detection_results1.csv 파일에서 2번째 행의 4번째열의 데이터를 가져와 정확도가 80보다 낮으면 문구출력, 높으면 2번째 열의 값을 가져옵니다.
with open('detection_results1.csv', 'r') as file1:
    reader1 = csv.reader(file1)
    next(reader1)  # 헤더 행을 건너뜁니다.
    for i, row in enumerate(reader1):
        if i == 1:  # 2번째 행에 접근합니다.
            accuracy = float(row[3].replace('%', ''))  # 4번째 열의 값을 가져옵니다. '%' 문자를 제거하고 실수로 변환합니다.
            if accuracy < 80:
                print("정확도가 낮아 새로운 사진을 넣어주세요")
                print(f"현재 정확도: {accuracy}%")
            else:
                print(f"현재 정확도: {accuracy}%")
                value_to_compare = row[1]  # 2번째 열의 값을 가져옵니다.
                break

# mean_per_stage.csv 파일에서 일치하는 값을 가진 열 데이터를 추출합니다.
matching_data = []
matching_indices = []  # 일치하는 인덱스를 저장할 리스트
with open('mean_per_stage.csv', 'r') as file2:
    reader2 = csv.reader(file2)
    header = next(reader2)
    column_index = None
    for i, value in enumerate(header):
        if value == value_to_compare:
            column_index = i
            break

    if column_index is not None:
        for row in reader2:
            matching_data.append(row[column_index])
            matching_indices.append(row[0])  # 일치하는 인덱스를 저장합니다.

# 결과 출력
print(f"Matching value: {value_to_compare}")
print("Matching data in mean_per_stage.csv:")
for index, data in zip(matching_indices, matching_data):
    print(f"{index}: {data}")

# now.csv 파일에서 2번째 열의 데이터를 2번째 행부터 나타냅니다.
now_csv_data = []
now_csv_indices = []  # now.csv 파일의 인덱스를 저장할 리스트
with open('now.csv', 'r') as file3:
    reader3 = csv.reader(file3)
    for i, row in enumerate(reader3):
        if i >= 1:  # 2번째 행부터 데이터를 가져옵니다.
            now_csv_data.append(row[1])
            now_csv_indices.append(row[0])  # now.csv 파일의 인덱스를 저장합니다.

# 결과 출력
print("Data in now.csv (2nd column, starting from 2nd row):")
for index, data in zip(now_csv_indices, now_csv_data):
    print(f"{index}: {data}")

# Assuming the first column of the "now.csv" file contains the names
with open('now.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row if it exists
    next(csv_reader)
    # Read the names into a list
    names = [row[0] for row in csv_reader]

# matching_data와 now_csv_data의 각 인덱스의 차이를 계산하여 출력
print("Differences between matching_data and now_csv_data:")
for i in range(len(matching_data)):
    if matching_data[i] is None:
        print("matching_data의 값이 존재하지 않는다")
    else:
        if matching_data[i] == '' or now_csv_data[i] == '':
            print(f"Index {i}: matching_data is empty")
        else:
            matching_value = float(matching_data[i])
            csv_value = float(now_csv_data[i])
            
            diff = matching_value - csv_value
            # Print the name along with the index
            print(f"{names[i]}: {diff}")
# Add last line
print("ti_value:", "내부 온도", "hi_value:", "내부 습도", "ci_value:", "내부 CO2", "ir_value:", "광량", "tl_value:", "양액 온도 ", "ei_value:", "양액 EC ", "pl_value:", "양액 PH", "sr_value:", "일사량", "cl_value:", "배지 온도", "el_value:", "배지 EC", "hl_value:", "배지 지습", "pi_value:", "배지 PH")



# CSV 파일에서 데이터 가져오기
data = pd.read_csv('7days_data.csv')

# 입력 데이터 추출
new_input_data = data[['ti_value', 'hi_value', 'ci_value', 'ir_value', 'tl_value']].values

# 입력 데이터 전처리
scaler = MinMaxScaler()
new_input_data = scaler.fit_transform(new_input_data)
new_input_data = new_input_data.reshape(1, 7, 5)

# 모델 로드
loaded_model = keras.models.load_model('trained_model.h5')

# 입력 데이터를 모델에 적용하여 예측 수행
prediction = loaded_model.predict(new_input_data)

# 입력 데이터 역변환
new_input_data_inverse = scaler.inverse_transform(new_input_data.reshape(-1, 5))

# 예측값 역변환
prediction_inverse = scaler.inverse_transform(prediction)

# 데이터 레이블
data_labels = ['ti_value', 'hi_value', 'ci_value', 'ir_value', 'tl_value']

# 7일 다음날의 값 출력 (정수로 변환하여 출력)
for i, value in enumerate(prediction_inverse.flatten().astype(int)):
    print(f"prediction {data_labels[i]}: {value}")




# 'now.csv' 파일로부터 데이터 읽기
with open('now.csv', 'r') as file:
    reader = csv.reader(file)
    now_data = list(reader)

# 2열 2행부터 6행까지의 값 추출
now_values = []
for row in now_data[1:6]:
    now_values.append([float(value) for value in row[1:]])

# 예측값과 차이 계산
prediction_diff = prediction_inverse.flatten() - np.array(now_values).flatten()

# 차이 출력
print("Differences between predicition_data and now_csv_data:")
for i, diff in enumerate(prediction_diff):
    print(f"Difference for {data_labels[i]}: {diff}")





















# ...

# Define a function to save data to a CSV file
def save_to_csv(filename, headers, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

# ...

# Update the detect_objects function to return the df DataFrame
def detect_objects(image_path):
    # ...

    return df

# ...

# Call the detect_objects function to get the df DataFrame
df = detect_objects(image_path)

# Save detection results to a CSV file
csv_path = 'detection_results1.csv'
df.to_csv(csv_path, index=False)
print(f"객체 감지 결과가 {csv_path}에 저장되었습니다.")

# ...

# Save matching data to a CSV file
matching_data_path = 'matching_data.csv'
matching_data_rows = zip(matching_indices, matching_data)
save_to_csv(matching_data_path, ['Index', 'Data'], matching_data_rows)
print(f"Matching data has been saved to {matching_data_path}.")

# ...

# Save differences between matching_data and now_csv_data to a CSV file
differences_path = 'differences.csv'
differences_data_rows = zip(names, prediction_diff)
save_to_csv(differences_path, ['Name', 'Difference'], differences_data_rows)
print(f"Differences between matching_data and now_csv_data have been saved to {differences_path}.")

# ...

# Save prediction data to a CSV file
prediction_path = 'prediction_data.csv'
prediction_data_rows = zip(data_labels, prediction_inverse.flatten().astype(int))
save_to_csv(prediction_path, ['Label', 'Value'], prediction_data_rows)
print(f"Prediction data has been saved to {prediction_path}.")


