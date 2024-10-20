import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# 讀取計算結果的CSV檔案
df = pd.read_csv('./simularity_with_weight.csv')

# 計算Cosine Similarity * weight作為特徵
df['cosine_sim_weighted'] = df['cosine_sim'] * df['weight']

# 只保留 'data a', 'data b', 和 'cosine_sim_weighted' 三個欄位
df_features = df[['data a', 'data b', 'cosine_sim_weighted']]

# 轉換成適合做聚類分析的特徵矩陣，data a 和 data b 作為座標，cosine_sim_weighted 作為特徵
X = pd.pivot_table(df_features, index='data a', columns='data b', values='cosine_sim_weighted').fillna(0)

# 使用linkage函數進行層次式聚類（可以選擇不同的方法：'ward', 'complete', 'average', 'single'）
Z = linkage(X, method='ward')

# 繪製樹狀圖
plt.figure(figsize=(10, 7))
dendrogram(Z, labels=range(1, 18), leaf_rotation=90, leaf_font_size=10, color_threshold=0.0)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Location')
plt.xticks(rotation=0, ha='right')
plt.ylabel('Distance')
plt.savefig('./fig/clustering result/Hierarchical clustering result.png')
