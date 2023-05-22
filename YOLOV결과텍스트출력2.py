import torch
import torchvision.transforms as T
from PIL import Image
import pandas as pd

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
    csv_path = 'detection_results.csv'
    df.to_csv(csv_path, index=False)

    return csv_path

# 이미지 경로 설정
image_path = 'test.jpg'

# 객체 감지 및 결과 저장
csv_path = detect_objects(image_path)
print(f"객체 감지 결과가 {csv_path}에 저장되었습니다.")
