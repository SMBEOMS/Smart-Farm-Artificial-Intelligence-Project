import pandas as pd
import matplotlib.pyplot as plt
import chardet

with open("sul_train_ver2.csv", "rb") as file:
    result = chardet.detect(file.read())

data = pd.read_csv("sul_train_ver2.csv", encoding=result["encoding"])

# 단계별 산점도 그리기 및 실효값 찾기
mean_per_stage = {}
stages = ["sul_1", "sul_2", "sul_3", "sul_4", "sul_5"]  # 각 단계의 이름을 리스트로 지정

for stage in stages:
    # 해당 단계에 해당하는 데이터 필터링
    subset = data[data["label_name"] == stage]
    
    # 실효값 계산을 위해 평균과 표준편차 계산
    mean = subset["ti_value"].mean()
    std = subset["ti_value"].std()
    
    # 실효값 조건 설정
    threshold = 3  # 표준편차의 3배 이상 떨어진 값을 실효값으로 선택
    
    # 실효값 필터링
    filtered_data = subset[(subset["ti_value"] >= mean - threshold * std) & (subset["ti_value"] <= mean + threshold * std)]
    
    # 실효값을 가진 데이터에 대한 평균 계산
    mean_filtered = filtered_data["ti_value"].mean()
    mean_per_stage[stage] = mean_filtered
    
    # 산점도 그리기
    plt.scatter(filtered_data["label_name"], filtered_data["ti_value"], label=stage)
    plt.xlabel("label_name")
    plt.ylabel("ti_value")

plt.legend()
plt.show()

print(mean_per_stage)