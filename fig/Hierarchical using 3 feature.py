import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# 讀取計算結果的CSV檔案
df = pd.read_csv('./simularity_with_weight.csv')

# 只保留 'data a', 'data b', 'cosine_sim_weighted', 'rmse', 'data_len'這幾個欄位
df_features = df[['data a', 'data b', 'cosine_sim', 'rmse', 'data_len']]

# 轉換成適合做聚類分析的特徵矩陣，data a 和 data b 作為座標
pivot_cosine = pd.pivot_table(df_features, index='data a', columns='data b', values='cosine_sim').fillna(0)
pivot_rmse = pd.pivot_table(df_features, index='data a', columns='data b', values='rmse').fillna(0)
pivot_len = pd.pivot_table(df_features, index='data a', columns='data b', values='data_len').fillna(0)

# 合併 特徵
X = np.hstack([pivot_cosine.values, pivot_rmse.values, pivot_len.values])

# 標準化數據（因為數據範圍不同，標準化可以確保其相對權重均衡）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用linkage函數進行層次式聚類（可以選擇不同的方法：'ward', 'complete', 'average', 'single'）
Z = linkage(X_scaled, method='ward')

# 繪製樹狀圖
plt.figure(figsize=(10, 7))
dendrogram(Z, labels=range(1, 18), leaf_rotation=0, leaf_font_size=10, color_threshold=0.0)
plt.title('Hierarchical Clustering Dendrogram (Cosine Similarity, RMSE and data_len)')
plt.xlabel('Location')
plt.ylabel('Distance')
plt.savefig('./fig/clustering result/Hierarchical 3 features-2.png')
