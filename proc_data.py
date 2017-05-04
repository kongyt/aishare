#coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 原始数据集
# date：交易日期
# oepn：开盘价
# high：最高价
# close: 收盘价
# low：最低价
# volume：成交量
# amount：成交金额

# 处理后添加字段
# avg5：五日均线
# avg10：十日均线
# avg15：十五日均线
# avg20：二十日均线

# 加载数据集
def load_data(filename):
    data = pd.read_csv(filename)
    return data

    
# 计算均值
def calc_avg(column_data, num=5):
    avg_data = []
    for i in range(len(column_data)):
        sum = 0.
        if i - num >= 0:
            sum = np.sum(column_data[i-num+1:i+1])
            avg_data.append(sum/num)
        else:
            sum = np.sum(column_data[0:i+1])
            avg_data.append(sum/(i+1))
        
    return avg_data
    
def get_profit(code, data):
    data['roe'] = 0
    data['net_profit_ratio'] = 0
    data['gross_profit_rate'] = 0 
    data['net_profits'] = 0 
    data['esp'] = 0
    data['business_income'] = 0
    data['bips'] = 0
    
    # 净资产收益率
    roe_data = []
    # 净利率
    net_profit_ratio_data = []
    # 毛利率
    gross_profit_rate_data = []
    # 净利润
    net_profits_data = []
    # 每股收益
    esp_data = []
    # 营业收入
    business_income_data = []
    # 每股主营业务收入
    bips_data = []
    indexs = data.index
    for i in range(len(indexs)):
        try:
            date = data.loc[indexs[i], 'date']
            filename = "profit_data/profit_"+str(date.year)+"_"+str(int(date.month/3+1))+".csv"
            #print(filename)
            profit_data = pd.read_csv(filename)
            row = profit_data[profit_data["code"]==int(code)]
            #print(row.loc[row.index[0],'roe'])
            data['roe'][i] = row.loc[row.index[0],'roe']
        except Exception as e:
            pass
            #print(e)
    print(data['roe'])

# 处理数据
def proc_data(data, show = False):
    data["date"] = pd.to_datetime(data["date"], format='%Y-%m-%d')
    raw_data = data['close']
    avg5_data = calc_avg(raw_data, num=5)
    avg10_data = calc_avg(raw_data, num=10)
    avg15_data = calc_avg(raw_data, num=15)
    avg20_data = calc_avg(raw_data, num=20)
    data.insert(7,'avg5', avg5_data)
    data.insert(8,'avg10', avg10_data)
    data.insert(9,'avg15', avg15_data)
    data.insert(10,'avg20', avg20_data)
    #print(data['date'])
    get_profit('002226', data)
    if show is True:
        data.plot(x='date',y=['open', 'avg5', 'avg10', 'avg15', 'avg20'])
        plt.show()
 
 # 保存数据
def save_data(filename, data): 
    data.to_csv(filename, encoding='utf-8')
 
if __name__ == "__main__":
    filename = "002226.csv"
    data = load_data(filename)
    data = data.tail(200)
    proc_data(data)
    #save_data("p"+filename, data)