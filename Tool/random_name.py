# !python3
# coding:utf8

'''
随机姓名
姓用的是百家姓
名用的是汉语常见3500字
这两个都放在不同的txt文件里，可以自己更换，格式照着改就行了，最后别有空格
由于编码的原因，所以最好在命令行下使用
'''

import random
import platform

xings = open("Tool/xing.txt", 'r', encoding='utf8').read().split(" ")
mings = open("Tool/ming.txt", 'r', encoding='utf8').read().split(" ")


# print(xings)
# print(mings)

def get_name(n=2):
    if n == 2:
        xing = random.choice(xings)
        ming = random.choice(mings)
        return f'{xing}{ming}'
    else:
        xing = random.choice(xings)
        ming = random.choice(mings)
        ming2 = random.choice(mings)
    return f'{xing}{ming}{ming2}'


if __name__ == '__main__':
	print(get_name(4))
