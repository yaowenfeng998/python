import pandas as pd
import glob


def parse_csv(files, columns_to_read=None):
    try:
        all_data = pd.DataFrame()
        if columns_to_read is not None:
            for file in files:
                df = pd.read_csv(file, usecols=columns_to_read, low_memory=False)
                all_data = pd.concat([all_data, df], ignore_index=True)
        return all_data
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def parse_xlsx(file_path, columns_to_read=None):
    try:
        if columns_to_read is not None:
            df = pd.read_excel(file_path, usecols=columns_to_read)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


csv_dir = '/Users/yaowenfeng/Desktop/csv_dir/*.csv'
asset_all_file = '/Users/yaowenfeng/Desktop/csv_dir/数据资产全量_列表.xlsx'

csv_files = glob.glob(csv_dir)

csv_columns = ['部门', 'IP', '端口', '库名', '表名', '字段', '变更前分级', '变更后分级', '操作时间']
asset_columns = ['业务网IP地址', '业务网端口', '数据库名/文件目录', '数据资产编号']

asset_ip_port_db_columns = ['业务网IP地址', '业务网端口', '数据库名/文件目录']
csv_ip_port_db_colums = ['IP', '端口', '库名']

csv_asset_level_group_key_no_code = ['部门', 'IP', '端口']
csv_asset_level_group_key_with_code = csv_asset_level_group_key_no_code.copy()
csv_asset_level_group_key_with_code.append('数据资产编号')

csv_db_level_group_key = ['部门', 'IP', '端口', '库名']
csv_table_level_group_key = csv_db_level_group_key.copy()
csv_table_level_group_key.append('表名')
csv_column_level_group_key = csv_table_level_group_key.copy()
csv_column_level_group_key.append('字段')

asset_all_data_frame = parse_xlsx(asset_all_file, asset_columns)
csv_all_data_frame = parse_csv(csv_files, csv_columns)

filtered_down_grade = csv_all_data_frame[(csv_all_data_frame['变更前分级'].isin(['第3级', '第4级'])) & (
    ~csv_all_data_frame['变更后分级'].isin(['第3级', '第4级']))]
# 对过滤结果去重 统计涉及到的部门 资产 库 表 字段 数量
unique_filtered_down_grade = filtered_down_grade.drop_duplicates(subset=csv_column_level_group_key)

print('=====================    降级统计信息    =====================')

merged = pd.merge(unique_filtered_down_grade, asset_all_data_frame, left_on=csv_ip_port_db_colums,
                  right_on=asset_ip_port_db_columns, how='left')
has_match = merged['业务网IP地址'].notna()
matched = merged[has_match]
down_grade_asset_sub_one = matched.groupby(csv_asset_level_group_key_with_code).size().groupby(
    level=0).size().reset_index(name='降级涉及资产数量')
unmatched = merged[~has_match]
down_grade_asset_sub_two = unmatched.groupby(csv_asset_level_group_key_no_code).size().groupby(
    level=0).size().reset_index(name='降级涉及资产数量')

down_grade_asset_sub = pd.concat([down_grade_asset_sub_one, down_grade_asset_sub_two], ignore_index=True)
down_grade_asset = down_grade_asset_sub.groupby('部门')['降级涉及资产数量'].sum().reset_index()
print(down_grade_asset)

down_grade_dept = unique_filtered_down_grade.groupby(csv_db_level_group_key).size().groupby(
    level=0).size().reset_index(name='降级涉及库数量')
print(down_grade_dept)

down_grade_table = unique_filtered_down_grade.groupby(csv_table_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='降级涉及表数量')
print(down_grade_table)

down_grade_column = unique_filtered_down_grade.groupby(csv_column_level_group_key).size().groupby(
    level=0).size().reset_index(name='降级涉及字段数量')
print(down_grade_column)

filtered_up_grade = csv_all_data_frame[
    ~(csv_all_data_frame['变更前分级'].isin(['第3级', '第4级'])) & (
        csv_all_data_frame['变更后分级'].isin(['第3级', '第4级']))]
unique_filtered_up_grade = filtered_up_grade.drop_duplicates(subset=csv_column_level_group_key)
print('=====================    升级统计信息    =====================')

up_merged = pd.merge(unique_filtered_up_grade, asset_all_data_frame, left_on=csv_ip_port_db_colums,
                     right_on=asset_ip_port_db_columns, how='left')
up_has_match = up_merged['业务网IP地址'].notna()
up_matched = up_merged[up_has_match]
up_grade_asset_sub_one = up_matched.groupby(csv_asset_level_group_key_with_code).size().groupby(
    level=0).size().reset_index(name='升级涉及资产数量')
up_unmatched = up_merged[~up_has_match]
up_grade_asset_sub_two = up_unmatched.groupby(csv_asset_level_group_key_no_code).size().groupby(
    level=0).size().reset_index(name='升级涉及资产数量')

up_grade_asset_sub = pd.concat([up_grade_asset_sub_one, up_grade_asset_sub_two], ignore_index=True)
up_grade_asset = up_grade_asset_sub.groupby('部门')['升级涉及资产数量'].sum().reset_index()
print(up_grade_asset)

up_grade_dept = unique_filtered_up_grade.groupby(csv_db_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='升级涉及库数量')
print(up_grade_dept)

up_grade_table = unique_filtered_up_grade.groupby(csv_table_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='升级涉及表数量')
print(up_grade_table)

up_grade_column = unique_filtered_up_grade.groupby(csv_column_level_group_key).size().groupby(
    level=0).size().reset_index(name='升级涉及字段数量')
print(up_grade_column)
