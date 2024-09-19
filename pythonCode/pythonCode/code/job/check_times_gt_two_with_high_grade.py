import pandas as pd
import glob


def parse_csv(csv_files, columns_to_read=None):
    try:
        all_data = pd.DataFrame()
        if columns_to_read is not None:
            for file in csv_files:
                df = pd.read_csv(file, usecols=columns_to_read, low_memory=False)
                all_data = pd.concat([all_data, df], ignore_index=True)
        return all_data
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


csv_dir = '/Users/yaowenfeng/Desktop/csvs/*.csv'

csv_files = glob.glob(csv_dir)

columns_to_read = ['部门', 'IP', '端口', '库名', '表名', '字段', '变更前分级', '变更后分级', '操作时间']
group_key = ['部门', 'IP', '端口', '库名', '表名', '字段']

all_data_frame = parse_csv(csv_files, columns_to_read=columns_to_read)
print('共读取文件:{}个,读取数据:{}行'.format(len(csv_files), len(all_data_frame)))

# DataFrameGroupBy -> Series (index: group_key, value: 操作时间最大的记录所在行行号)
max_time_indices = all_data_frame.groupby(group_key)['操作时间'].idxmax()
filtered_max_time_only = all_data_frame.loc[max_time_indices]
print('分组,获取每组时间最新的行号,过滤后获取:{}行'.format(len(filtered_max_time_only)))

filtered_max_time_only_high_grade = filtered_max_time_only[
    filtered_max_time_only['变更后分级'].isin(['第3级', '第4级'])]
print('最终等级为三/四级的字段数量:{}'.format(len(filtered_max_time_only_high_grade)))

# all_data_frame.groupby(group_key).size() 获取到Series k group_key value size()的值，.reset_index(name='count')将Series转成DataFrame 重置索引的同时,将size()结果列 命名为count
filtered_count_only = all_data_frame.groupby(group_key).size().reset_index(name='count')

# 布尔表达式 过滤 count值>1的记录
filtered_count_gt_two = filtered_count_only[filtered_count_only['count'] >= 3]
print('核查3次及以上的字段共{}'.format(len(filtered_count_gt_two)))

if not filtered_count_gt_two.empty:
    ## 横向merge  根据group_key 取交集
    r = pd.merge(filtered_max_time_only_high_grade, filtered_count_gt_two,
                 on=group_key, how='inner')
    print('核查3次及以上，并且满足最终是三四级的字段共有{}'.format(len(r)))
    a = r.groupby(['部门', '变更后分级']).size().reset_index(name='数量')
    print(a)
