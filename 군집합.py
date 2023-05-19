import pandas as pd
import matplotlib.pyplot as plt
import chardet
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

with open("sul_train_ver2.csv", "rb") as file:
    result = chardet.detect(file.read())

data = pd.read_csv("sul_train_ver2.csv", encoding=result["encoding"])

# 결측값 처리
imputer = SimpleImputer(strategy="most_frequent")
data_imputed = imputer.fit_transform(data)

# 데이터 준비
selected_features = ["ti_value"]  # 군집화에 사용할 특성 선택

# 군집화 알고리즘 설정
n_clusters = 3  # 군집 개수 설정
kmeans = KMeans(n_clusters=n_clusters)

# 데이터 군집화
clusters = kmeans.fit_predict(data_imputed[:, data.columns.get_loc(selected_features[0])].reshape(-1, 1))

# 군집화 결과 시각화
plt.scatter(data["label_name"], data["ti_value"], c=clusters, s=1.5)
plt.xlabel("label_name")
plt.ylabel("ti_value")
plt.show()
print(clusters)
