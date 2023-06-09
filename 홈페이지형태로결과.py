import pandas as pd

# CSV 파일 로드
data_now = pd.read_csv('now.csv')
data_detection = pd.read_csv('detection_results1.csv')
data_results = pd.read_csv('results.csv')

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

# results.csv에서 필요한 데이터 선택
start_index = data_results[data_results['Type'] == 'Matching data in mean_per_stage.csv:'].index[0]
end_index = data_results[data_results['Type'] == 'Data in now.csv (2nd column, starting from 2nd row):'].index[0]
selected_results = data_results.loc[start_index+1:end_index-1, ['Type', 'Value']]

# results.csv에서 필요한 데이터 선택2
start_index2 = data_results[data_results['Type'] == 'Predicted values for the next day:'].index[0]
end_index2 = data_results[data_results['Type'] == 'Differences between prediction_data and now_csv_data:'].index[0]
selected_results2 = data_results.loc[start_index2+1:end_index2-1, ['Type', 'Value']]

start_index3 = data_results[data_results['Type'] == 'Differences between prediction_data and now_csv_data:'].index[0]
end_index3 = len(data_results)
selected_differences = data_results.loc[start_index3+1:end_index3, ['Type', 'Value']]

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
    body {{
      padding: 20px;
    }}

    .grid-container {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 20px;
      align-items: center;
      margin-bottom: 40px;
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
      background-color: gainsboro;
    }}

    th, td {{
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
      background-color: white;
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
      padding: 20px;
      margin-bottom: 40px;
    }}

    .grid-container2 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      align-items: center;
      margin-bottom: 40px;
    }}

    .table-container2 {{
      grid-column: span 4;
      border:10px solid rgb(253, 173, 1);
    }}

    back-to-top {{
      position: fixed;
      display: none;
      width: 40px;
      height: 40px;
      border-radius: 50px;
      right: 15px;
      bottom: 15px;
      background: #3366cc;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease-in-out;
      opacity: 0.6;
      z-index: 9999;
    }}

    .back-to-top:hover {{
      background: #1e4ba5;
      color: #fff;
      opacity: 1;
    }}
  </style>
</head>
<body style="background-image: url('https://d18-invdn-com.investing.com/content/pic70e5f5fbd740abf686f7ff084068c49e.jpg'); background-repeat: no-repeat; background-size: contain;">
  <div class="center1">
    <h1><span style="background-color:rgb(199, 173, 22); font-size: 70px; font-weight: bold;">스마트팜 성장도</span></h1>
  </div>
  <div class="grid-container">
    <div class="image-container">
      <h1 style="font-weight: bold; font-size: 40px; background-color: white;">입력이미지</h1>
      <img src="{image_path}">
    </div>

    <div class="column-name-container" style="border:10px solid red; padding: 10px; background-color: white;">
      <h3 style="color: rgb(41, 0, 25); font-size: 50px; font-weight: bold;">딸기종류: {strawberry_type_korean}</h3><br>
      <h3 style="color: rgb(41, 0, 25); font-size: 50px; font-weight: bold;">성장단계: {growth_stage_korean}</h3><br>
      <h3 style="color: rgb(41, 0, 25); font-size: 50px; font-weight: bold;">정확도: {confidence}</h3>
    </div>

    <div class="now"  style="border:10px solid skyblue;">
      <table>
        <tr>
          <th colspan="2" class="center">
            <h3 style="font-weight: bold; font-size: 40px;">현재 데이터</h3>
          </th>
        </tr>
        {data_rows}
      </table>
    </div>
  </div>
  <hr>
  <div class="grid-container">
    <div class="table-container2">
      <table>
        <tr>
          <th colspan="2" class="center">
            <h3 style="font-weight: bold; font-size: 40px;">최적값</h3>
          </th>
        </tr>
        {result_rows}
      </table>
    </div>
    <div class="table-container2">
      <table>
        <tr>
          <th colspan="2" class="center">
            <h3 style="font-weight: bold; font-size: 40px;">내일 예상 데이터</h3>
          </th>
        </tr>
        {result_rows2}
      </table>
    </div>
    <div class="table-container2">
      <table>
        <tr>
          <th colspan="2" class="center">
            <h3 style="font-weight: bold; font-size: 40px;">예상과 현재의 차이</h3>
          </th>
        </tr>
        {result_row3}
      </table>
    </div>
  </div>


  <!-- ======= Footer ======= -->
  <footer id="footer">
    <div class="container">
      <h3>스마트팜</h3>
      <p>© 2023 정범석</p>
    </div>
  </footer><!-- End Footer -->

  <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

  <!-- Vendor JS Files -->
  <script src="assets/vendor/aos/aos.js"></script>
  <script src="assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="assets/vendor/glightbox/js/glightbox.min.js"></script>
  <script src="assets/vendor/isotope-layout/isotope.pkgd.min.js"></script>
  <script src="assets/vendor/php-email-form/validate.js"></script>
  <script src="assets/vendor/purecounter/purecounter.js"></script>
  <script src="assets/vendor/swiper/swiper-bundle.min.js"></script>
  <script src="assets/vendor/waypoints/noframework.waypoints.js"></script>

  <!-- Template Main JS File -->
  <script src="assets/js/main.js"></script>

</body>

</html>

"""

# 이미지 경로 설정
image_path = "test.jpg"  # 이미지 파일 경로

# 현재 데이터 테이블 생성
now_table = selected_columns.to_html(index=False, header=False).replace('<table', '<table style="margin-left:auto;margin-right:auto;"')

# 결과 데이터 테이블 생성
result_table = selected_results.to_html(index=False, header=False).replace('<table', '<table style="margin-left:auto;margin-right:auto;"')
result_table2 = selected_results2.to_html(index=False, header=False).replace('<table', '<table style="margin-left:auto;margin-right:auto;"')
differences_table = selected_differences.to_html(index=False, header=False).replace('<table', '<table style="margin-left:auto;margin-right:auto;"')

# HTML 템플릿에 데이터 삽입
html_output = html_template.format(image_path=image_path, strawberry_type_korean=strawberry_type_korean,
                                   growth_stage_korean=growth_stage_korean, confidence=confidence,
                                   data_rows=now_table, result_rows=result_table,result_rows2=result_table2, result_row3=differences_table)

# 결과 HTML 파일 저장
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_output)