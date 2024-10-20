import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from matplotlib import patches

# 讀取計算結果的CSV檔案
df = pd.read_csv('./simularity_with_weight.csv')

# 計算Cosine Similarity * weight作為特徵
df['cosine_sim_weighted'] = df['cosine_sim'] * df['weight']

# 只保留 'data a', 'data b', 和 'cosine_sim_weighted' 三個欄位
df_features = df[['data a', 'data b', 'cosine_sim_weighted']]

# 轉換成適合做聚類分析的特徵矩陣，data a 和 data b 作為座標，cosine_sim_weighted 作為特徵
X = pd.pivot_table(df_features, index='data a', columns='data b', values='cosine_sim_weighted').fillna(0)

# 使用DBSCAN進行分群
dbscan = DBSCAN(eps=0.5, min_samples=2)
labels = dbscan.fit_predict(X)

# 將結果加回原資料集
df_result = pd.DataFrame({'Location': range(1, 18), 'Cluster': labels})

# 繪製散佈圖
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df_result['Location'], df_result['Cluster'], c=df_result['Cluster'], cmap='Set1', edgecolor='k')

# 增加虛線圈起群組的功能
clusters = np.unique(labels)
for cluster in clusters:
    if cluster == -1:
        continue  # 忽略噪聲點
    # 選取該群的點
    cluster_points = df_result[df_result['Cluster'] == cluster]
    
    # 用虛線圈起該群的範圍
    cluster_min = cluster_points['Location'].min() - 0.5
    cluster_max = cluster_points['Location'].max() + 0.5
    rect = patches.Rectangle((cluster_min, cluster-0.5), cluster_max-cluster_min, 1, linewidth=1, edgecolor='r', facecolor='none', linestyle='--')
    plt.gca().add_patch(rect)

# 標示軸標題和圖標
plt.title('DBSCAN Clustering of Locations Based on Cosine Similarity * Weight')
plt.xlabel('Location')
plt.ylabel('Cluster')

# 顯示圖例
plt.legend(*scatter.legend_elements(), title='Clusters')
plt.savefig('./fig/clustering result/DBSCAN clustering result.png')
