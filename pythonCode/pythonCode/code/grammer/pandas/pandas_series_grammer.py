import pandas as pd
import numpy as np

# series ======= 获取
num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num_series = pd.Series(num_list, index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])

# series ======= 获取指定索引的元素
print(num_series['a'])
print(num_series.iloc[0])
print(num_series[0])

print('========' * 30)
# series ======= 遍历 默认 遍历value
for j in num_series:
    print(j)
# series ======= 遍历 索引 value  ('a', 1)
for i in num_series.items():
    print(i)
# series ======= 遍历 索引 value  a 1
for k, v in num_series.items():
    print(k, v)

print('========' * 30)
# 删除num_series中的第一个元素 , a 1 被删除
del num_series['a']
print(num_series)

print('========' * 30)
# 返回一个新的series,该series的删除第一个元素 即 b 2被删除, num_series 不变
drop_num_series = num_series.drop(['b'])
# 包含b
print(num_series)
# 新的series不包含b
print(drop_num_series)

print('========' * 30)
# int乘2 字符串3->33
result = num_series * 2
print(result)

print('========' * 30)
filtered = result[result > 4]
print(filtered)

print('========' * 30)
print(np.sqrt(filtered))

print('========' * 30)
print(num_series.sum())
# avg
print(num_series.mean())
print(num_series.max())
print(num_series.min())
# 标准差
print(num_series.std())

print('========' * 30)
print(num_series.index)
print(num_series.index.values)
print(num_series.values)
print(num_series.describe())
print(num_series.idxmax())
print(num_series.idxmin())

print('========' * 30)
print(num_series.dtype)
# rows columns
print(num_series.shape)
# head 5 ele
print(num_series.head())
# tail 5 ele
print(num_series.tail())
print('========' * 30)
r = num_series.astype('string')
print(r)
