import pandas as pd
import glob
import xlsxwriter


def parse_csv(files, columns_to_read=None):
    try:
        all_data = pd.DataFrame()
        if columns_to_read is not None:
            for file in files:
                df = pd.read_csv(file, usecols=columns_to_read, low_memory=False)
                all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            for file in files:
                df = pd.read_csv(file, low_memory=False)
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


csv_dir = '/Users/yaowenfeng/Desktop/csv_dir/操作留痕导出/*.csv'
asset_all_file = '/Users/yaowenfeng/Desktop/csv_dir/数据资产全量_列表.xlsx'
field_file_dir = '/Users/yaowenfeng/Desktop/csv_dir/8月份新增字段明细/*.csv'

csv_files = glob.glob(csv_dir)
field_file = glob.glob(field_file_dir)

csv_columns = ['部门', 'IP', '端口', '库名', '表名', '字段', '变更前分级', '变更后分级', '操作时间', '操作员']
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

asset_all_data_frame = parse_xlsx(asset_all_file, columns_to_read=asset_columns)
csv_all_data_frame = parse_csv(csv_files, columns_to_read=csv_columns)

field_data = parse_csv(field_file,
                       columns_to_read=['部门', '业务系统', '资产编号', '库名', '表名', '字段名', '创建时间',
                                        '更新时间'])

max_time_indices = csv_all_data_frame.groupby(csv_column_level_group_key)['操作时间'].idxmax()
filtered_max_time_only = csv_all_data_frame.loc[max_time_indices]

filtered_down_grade = filtered_max_time_only[(filtered_max_time_only['变更前分级'].isin(['第3级', '第4级'])) & (
    ~filtered_max_time_only['变更后分级'].isin(['第3级', '第4级']))]
print('字段最终降级数量:{}'.format(len(filtered_down_grade)))
print('=====================    降级统计信息    =====================')

csv_asset_down_merge = pd.merge(filtered_down_grade, asset_all_data_frame, left_on=csv_ip_port_db_colums,
                                right_on=asset_ip_port_db_columns, how='left')
csv_asset_down_merge_matched = csv_asset_down_merge[csv_asset_down_merge['业务网IP地址'].notna()]

down_grade_asset_sub_one = csv_asset_down_merge_matched.groupby(csv_asset_level_group_key_with_code).size().groupby(
    level=0).size().reset_index(name='降级涉及资产数量')
csv_asset_down_merge_unmatched = csv_asset_down_merge[~(csv_asset_down_merge['业务网IP地址'].notna())]
down_grade_asset_sub_two = csv_asset_down_merge_unmatched.groupby(csv_asset_level_group_key_no_code).size().groupby(
    level=0).size().reset_index(name='降级涉及资产数量')

down_grade_asset_sub = pd.concat([down_grade_asset_sub_one, down_grade_asset_sub_two], ignore_index=True)
down_grade_asset = down_grade_asset_sub.groupby('部门')['降级涉及资产数量'].sum().reset_index()
print(down_grade_asset)

csv_asset_field_left_merge_matched = pd.merge(csv_asset_down_merge_matched, field_data,
                                              left_on=['部门', '库名', '表名', '字段', '数据资产编号'],
                                              right_on=['部门', '库名', '表名', '字段名', '资产编号'], how='left')
print('操作记录、数据资产 关联成功的记录数:{},关联key: ip,port,db'.format(len(csv_asset_down_merge_matched)))
print('操作记录、数据资产、comb 关联成功的记录数:{},关联key: ip,port,db;;; 部门 db table field 资产编号'.format(
    len(csv_asset_field_left_merge_matched[csv_asset_field_left_merge_matched['资产编号'].notna()])))

re_unmatched = csv_asset_down_merge_unmatched[csv_columns]
print('操作记录、数据资产 关联失败数量:{},将以ip port进行关联'.format(len(re_unmatched)))
middle = (pd.merge(re_unmatched, asset_all_data_frame, left_on=['IP', '端口'],
                   right_on=['业务网IP地址', '业务网端口'], how='left'))
print('操作记录、数据资产 关联成功的数量:{},关联key: ip port'.format(len(middle[middle['业务网IP地址'].notna()])))
print(middle[~middle['业务网IP地址'].notna()])

csv_asset_field_left_merge_unmatched = pd.merge(middle, field_data,
                                                left_on=['部门', '库名', '表名', '字段', '数据资产编号'],
                                                right_on=['部门', '库名', '表名', '字段名', '资产编号'], how='left')

print('操作记录、数据资产、comb关联成功数量:{},关联key: ip,port;;; 部门 db table field 资产编号'.format(
    len(csv_asset_field_left_merge_unmatched[csv_asset_field_left_merge_unmatched['资产编号'].notna()])))
result_sub = pd.concat([csv_asset_field_left_merge_matched, csv_asset_field_left_merge_unmatched], ignore_index=True)
print('操作记录、数据资产、comb 关联记录总数:{}'.format(len(result_sub)))
result = result_sub[result_sub['创建时间'].notna()]
print('操作记录、数据资产、comb 关联成功的记录总数:{}'.format(len(result)))

print(
    result.groupby(['部门', '资产编号']).size().groupby(level=0).size().reset_index(name='降级-涉及字段新增的资产数量'))

un_result = result_sub[~(result_sub['创建时间'].notna())]
un_result = un_result[
    ['部门', '操作员', '数据资产编号', '库名', '表名', '字段', '变更前分级', '变更后分级', '操作时间']]
for name, group in un_result.groupby('部门'):
    filename = f"/Users/yaowenfeng/Desktop/csv_dir/res/{name}_2024年8月份核查存量字段降级明细.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        group.to_excel(writer, sheet_name='降级明细', index=False)

down_grade_dept = filtered_down_grade.groupby(csv_db_level_group_key).size().groupby(
    level=0).size().reset_index(name='降级涉及库数量')
print(down_grade_dept)

down_grade_table = filtered_down_grade.groupby(csv_table_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='降级涉及表数量')
print(down_grade_table)

down_grade_column = filtered_down_grade.groupby(csv_column_level_group_key).size().groupby(
    level=0).size().reset_index(name='降级涉及字段数量')
print(down_grade_column)

filtered_up_grade = filtered_max_time_only[
    ~(filtered_max_time_only['变更前分级'].isin(['第3级', '第4级'])) & (
        filtered_max_time_only['变更后分级'].isin(['第3级', '第4级']))]

print('=====================    升级统计信息    =====================')

csv_asset_up_merged = pd.merge(filtered_up_grade, asset_all_data_frame, left_on=csv_ip_port_db_colums,
                               right_on=asset_ip_port_db_columns, how='left')

csv_asset_up_matched = csv_asset_up_merged[csv_asset_up_merged['业务网IP地址'].notna()]
up_grade_asset_sub_one = csv_asset_up_matched.groupby(csv_asset_level_group_key_with_code).size().groupby(
    level=0).size().reset_index(name='升级涉及资产数量')
csv_asset_up_unmatched = csv_asset_up_merged[~(csv_asset_up_merged['业务网IP地址'].notna())]
up_grade_asset_sub_two = csv_asset_up_unmatched.groupby(csv_asset_level_group_key_no_code).size().groupby(
    level=0).size().reset_index(name='升级涉及资产数量')

up_grade_asset_sub = pd.concat([up_grade_asset_sub_one, up_grade_asset_sub_two], ignore_index=True)
up_grade_asset = up_grade_asset_sub.groupby('部门')['升级涉及资产数量'].sum().reset_index()
print(up_grade_asset)

csv_asset_field_left_merge_up_matched = pd.merge(csv_asset_up_matched, field_data,
                                                 left_on=['部门', '库名', '表名', '字段', '数据资产编号'],
                                                 right_on=['部门', '库名', '表名', '字段名', '资产编号'], how='left')
print(len(csv_asset_field_left_merge_up_matched))
print(len(csv_asset_field_left_merge_up_matched[csv_asset_field_left_merge_up_matched['资产编号'].notna()]))

re_up_unmatched = csv_asset_up_unmatched[csv_columns]
print(len(re_up_unmatched))
up_middle = (pd.merge(re_up_unmatched, asset_all_data_frame, left_on=['IP', '端口'],
                      right_on=['业务网IP地址', '业务网端口'], how='inner'))
print(len(up_middle))
csv_asset_field_left_merge_up_unmatched = pd.merge(up_middle, field_data,
                                                   left_on=['部门', '库名', '表名', '字段', '数据资产编号'],
                                                   right_on=['部门', '库名', '表名', '字段名', '资产编号'], how='left')
print(len(csv_asset_field_left_merge_up_unmatched))
print(len(csv_asset_field_left_merge_up_unmatched[csv_asset_field_left_merge_up_unmatched['资产编号'].notna()]))
result_sub_up = pd.concat([csv_asset_field_left_merge_up_matched, csv_asset_field_left_merge_up_unmatched],
                          ignore_index=True)
print(len(result_sub_up))
result_up = result_sub_up[result_sub_up['创建时间'].notna()]
print(len(result_up))
print(result_up.groupby(['部门', '资产编号']).size())
print(result_up.groupby(['部门', '资产编号']).size().groupby(level=0).size().reset_index(
    name='升级-涉及字段新增的资产数量'))

un_result_up = result_sub_up[~(result_sub_up['创建时间'].notna())]
un_result_up = un_result_up[
    ['部门', '操作员', '数据资产编号', '库名', '表名', '字段', '变更前分级', '变更后分级', '操作时间']]
for name, group in un_result_up.groupby('部门'):
    filename = f"/Users/yaowenfeng/Desktop/csv_dir/res/{name}_2024年8月份核查存量字段升级明细.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        group.to_excel(writer, sheet_name='升级明细', index=False)

up_grade_dept = filtered_up_grade.groupby(csv_db_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='升级涉及库数量')
print(up_grade_dept)

up_grade_table = filtered_up_grade.groupby(csv_table_level_group_key).size().groupby(
    level=0).size().reset_index(
    name='升级涉及表数量')
print(up_grade_table)

up_grade_column = filtered_up_grade.groupby(csv_column_level_group_key).size().groupby(
    level=0).size().reset_index(name='升级涉及字段数量')
print(up_grade_column)
