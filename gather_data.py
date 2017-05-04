#coding: utf-8

import time
import tushare as ts
import sys

# 生成开始日期字符串
def get_start_date():
    date = time.strftime("%Y-%m-%d", time.localtime(0))
    return date

# 生成当前日期字符串
def get_current_date():
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date
    
# 收集历史数据
def gather_hist_data(share_code):
    start_date = get_start_date()
    end_date = get_current_date()
    data = ts.get_h_data(share_code, start=start_date, end=end_date)
    return data
    
    
# 获取基本面数据
def gather_stock_basics():
    data = ts.get_stock_basics()
    return data

# 保存数据
def save_data(filename, data):
    data.to_csv(filename, encoding='utf=8')
 
 
 
# 获取单支数据并保存
def gather_share_data_and_save(share_code):
    data = gather_hist_data(share_code)
    data = data.sort(ascending=True)
    filename = share_code + ".csv"
    save_data(filename, data)
    
# 获取基本面数据并保存
def gather_stock_basics_and_save():
    filename = "basics.csv"
    data = gather_stock_basics()
    save_data(filename, data)
 
# 获取业绩报表数据
def gather_report_data_and_save():
    for i in range(1990,2018):
        for j in range(1, 5):
            try:
                filename = "reports_data/report_"+str(i)+"_"+str(j)+".csv"
                print('\n', filename,'\n')
                data = ts.get_report_data(i,j)
                data.drop_duplicates(['code'])
                save_data(filename, data)
            except:
                pass
                
# 获取盈利能力数据
def gather_profit_data_and_save():
    for i in range(1990,2018):
        for j in range(1, 5):
            try:
                filename = "profit_data/profit_"+str(i)+"_"+str(j)+".csv"
                print('\n', filename,'\n')
                data = ts.get_profit_data(i,j)
                data.drop_duplicates(['code'])
                save_data(filename, data)
            except:
                pass
                

# 帮助
def help():
    print("commands:")
    print("    share <code>     | get share history data by code.")
    print("    report           | get all report since 1990.")
    print("    basics           | get basics data.")
    print("    help             | this is.")
    print("")
 
if __name__ == "__main__":

    if len(sys.argv) == 3:
        if sys.argv[1] == "share" and sys.argv[2].isdigit():
            share_code = sys.argv[2]
            gather_share_data_and_save(share_code)
        else:
            help()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "basics":
            gather_stock_basics_and_save()
        elif sys.argv[1] == "report":
            gather_report_data_and_save()
        elif sys.argv[1] == "profit":
            gather_profit_data_and_save()
        elif sys.argv[1] == "help":
            help()
        else:
            help()        
    else:
        # 获取单支数据
        share_code = "002226"
        data = gather_hist_data(share_code)
        data = data.sort(ascending=True)
        filename = share_code + ".csv"
        save_data(filename, data)
    
        # 获取并保存基本面数据
        filename = "basics.csv"
        data = gather_stock_basics()
        save_data(filename, data)