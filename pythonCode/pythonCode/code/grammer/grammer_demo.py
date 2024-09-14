# grammer=utf-8
import pandas
from _collections_abc import Iterable

import pandas as pd
import  numpy as np


# ======== generator 生成器，迭代一次 返回一个值 ========
def generator_demo():
    yield 1
    yield 2
    yield 3


print('generator Iterable? ', isinstance(generator_demo(), Iterable))
for g in generator_demo():
    print(g)
# pandas ======= series
num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num_series = pd.Series(num_list, index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
print(num_series['a'])
print(num_series.iloc[0])
print(num_series[0])
for j in num_series:
    print(j)
for i in num_series.items():
    print(i)
for k, v in num_series.items():
    print(k, v)

# 删除num_series中的第一个元素
del num_series['a']
print(num_series)
# 返回一个新的series 删除第一个元素 即index=b
drop_num_series = num_series.drop(['b'])
# 包含b
print(num_series)
# 新的series不包含b
print(drop_num_series)

print('========' * 10)
# int乘2 字符串3->33
result = num_series * 2
print(result)
print('========' * 10)
filtered = result[result > 4]
print(filtered)

print('========' * 10)
print(np.sqrt(filtered))
print('========' * 10)
print(num_series.sum())
#avg
print(num_series.mean())
print(num_series.max())
print(num_series.min())
#标准差
print(num_series.std())

print('========' * 10)
print(num_series.index)
print(num_series.index.values)
print(num_series.values)
print(num_series.describe())
print(num_series.idxmax())
print(num_series.idxmin())
print('========' * 10)
print(num_series.dtype)
#rows columns
print(num_series.shape)
# head 5 ele
print(num_series.head())
#tail 5 ele
print(num_series.tail())
print('========' * 10)
r=num_series.astype('string')
print(r)




