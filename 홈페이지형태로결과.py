import pandas as pd

# CSV 파일 로드
data_now = pd.read_csv('now.csv')
data_detection = pd.read_csv('detection_results1.csv')

# now.csv에서 필요한 데이터 선택
selected_columns = data_now[['data_value', 'now']]  # 'data_value'와 'now' 열 선택

# detection_results1.csv에서 필요한 데이터 추출
strawberry_type = data_detection['strawberry_type'][0].split('_')[0]  # 딸기종류

# 딸기종류 한글 변환
if strawberry_type == "sul":
    strawberry_type_korean = "설향"
elif strawberry_type == "geam":
    strawberry_type_korean = "금향"
else:
    strawberry_type_korean = strawberry_type

data_detection['class'] = data_detection['class'].astype(str)  # 문자열로 변환

# 성장단계 한글 변환
growth_stage_mapping = {
    "0": "정식기",
    "1": "출뢰기",
    "2": "개화기",
    "3": "과실비대기",
    "4": "수확기",
    "5": "정식기",
    "6": "출뢰기",
    "7": "개화기",
    "8": "과실비대기",
    "9": "수확기",
    "10": "정식기",
    "11": "출뢰기",
    "12": "개화기",
    "13": "과실비대기",
    "14": "수확기",
    "15": "정식기",
    "16": "출뢰기",
    "17": "개화기",
    "18": "과실비대기",
    "19": "수확기"
}

data_detection['class_korean'] = data_detection['class'].map(growth_stage_mapping)
growth_stage_korean = data_detection['class_korean'][0]  # 첫 번째 데이터의 한글 성장단계

confidence = data_detection['confidence'][0]  # 정확도

# HTML 템플릿 생성 및 데이터 삽입
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>스마트팜 성장도</title>
  <meta content="" name="description">
  <meta content="" name="keywords">

  <!-- Favicons -->
  <link href="assets/img/favicon.png" rel="icon">
  <link href="assets/img/apple-touch-icon.png" rel="apple-touch-icon">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">

  <!-- Vendor CSS Files -->
  <link href="assets/vendor/animate.css/animate.min.css" rel="stylesheet">
  <link href="assets/vendor/aos/aos.css" rel="stylesheet">
  <link href="assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
  <link href="assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">
  <link href="assets/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
  <link href="assets/vendor/remixicon/remixicon.css" rel="stylesheet">
  <link href="assets/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">

  <link href="assets/css/style.css" rel="stylesheet">

  <style>
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: 10px;
        align-items: center;
    }}
    .image-container {{
        grid-column: span 6;
        text-align: center;
    }}
    .column-name-container {{
        grid-column: span 3;
        font-size: 18px;
        text-align: center;
        
    }}
    .now {{
        grid-column: span 3;
        font-size: 14px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }}
    img {{
        width: 100%;
        height: auto;
        max-width: 100%;
        max-height: 100%;
    }}
    .center {{
        display: flex;
        justify-content: center;
    }}
    .center1 {{
        display: flex;
        justify-content: center;
        background-color: gainsboro;
    }}
    
  </style>
</head>

<body>

  <div class="center1">
    <h1>스마트팜 성장도</h1>
  </div>
  <div class="grid-container">
    <div class="image-container">
      <img src="{image_path}">
    </div>
    <div class="column-name-container">
      <h3 style="color: dodgerblue;">딸기종류: {strawberry_type_korean}</h3>
      <h3 style="color: dodgerblue;">성장단계: {growth_stage_korean}</h3>
      <h3 style="color: dodgerblue;">정확도: {confidence}</h3>
    </div>
    <div class="now">
      <table>
        <tr>
          <th colspan="2" class="center"><h3>현재 데이터</h3></th>
        </tr>
        {data_rows}
      </table>
    </div>
  </div>
  <hr>

  <!-- ======= Footer ======= -->
  <footer id="footer">
    <div class="container">
      <h3>Smart Farm</h3>
      <p>MADE BY JEONG BEOM SEOK</p>
      <div class="social-links">
        <a href="#" class="twitter"><i class="bx bxl-twitter"></i></a>
        <a href="#" class="facebook"><i class="bx bxl-facebook"></i></a>
        <a href="#" class="instagram"><i class="bx bxl-instagram"></i></a>
        <a href="#" class="google-plus"><i class="bx bxl-skype"></i></a>
        <a href="#" class="linkedin"><i class="bx bxl-linkedin"></i></a>
      </div>
      <div class="credits">
        Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
      </div>
    </div>
  </footer><!-- End Footer -->

  <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

  <!-- Vendor JS Files -->
  <script src="assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="assets/vendor/glightbox/js/glightbox.min.js"></script>
  <script src="assets/vendor/isotope-layout/isotope.pkgd.min.js"></script>
  <script src="assets/vendor/swiper/swiper-bundle.min.js"></script>
  <script src="assets/vendor/php-email-form/validate.js"></script>

  <!-- Template Main JS File -->
  <script src="assets/js/main.js"></script>

</body>

</html>

"""

# 이미지 파일 경로
image_path = 'test.jpg'  # 이미지 파일의 경로를 지정해야 합니다.

# 데이터 행을 HTML 행으로 변환
data_rows = '\n'.join('<tr><td>{}</td><td>{}</td></tr>'.format(*values) for values in selected_columns.values)

# HTML 템플릿에 데이터 삽입
html_content = html_template.format(
    image_path=image_path,
    strawberry_type_korean=strawberry_type_korean,
    growth_stage_korean=growth_stage_korean,
    confidence=confidence,
    data_rows=data_rows
)

# HTML 파일로 저장
with open('data.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
