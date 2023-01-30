# 健身房系統模擬與營業效益之優化 #Gym system simulation and optimization of business efficiency

✒問題定義：
------------------------------------------------------------------------------
每位顧客在有限數量之健身器材前所需花費的等待時間（waiting time），會因為使用者的需求數增加而使每位客戶的等待時間相對拉長，因此身為健身房經理在預算有限下，如何採購與配置健身器材使每位顧客所花費的等待時間最小為一重要問題

假設狀態：

顧客的抵達人數服從卜瓦松分配

每項器材的使用時間服從常態分配

顧客有無訓練菜單為隨機事件

有菜單的顧客訓練哪個部位為隨機事件

✒模型建構步驟：
------------------------------------------------------------------------------

<img width="671" alt="image" src="https://user-images.githubusercontent.com/68886395/215425179-47a612fe-1689-4e67-931c-0f56d4678de6.png">

✒python模型建構(含健身房系統模擬與以localized random search演算法最佳化顧客等待時間比率
---
<img width="692" alt="image" src="https://user-images.githubusercontent.com/68886395/215426467-6b66dc98-b0a5-4685-9ac9-0212ad8c82f6.png">

健身房模擬結果：
![image](https://user-images.githubusercontent.com/68886395/215426930-65713481-f2ad-4a8c-b37b-acedb19b7bca.jpeg)

final表示為總共的等待時間比率佔據總時間比率（使用時間＋等待時間）佔比

arrivals表示為該健身系統營業時間內所到達的總顧客數

total_wait表示所有顧客的等待時間加總

total_use表示所有顧客的使用時間加總
<img width="583" alt="image" src="https://user-images.githubusercontent.com/68886395/215426741-dfa855db-fcdc-44c2-bcf6-7440a40c2dcd.png">
