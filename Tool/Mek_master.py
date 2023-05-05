import json
import csv
import shutil
import time
import datetime
import os
import uuid
import string
import random
import pickle
import hashlib

compile_time = 20230317


def logo_Slabt(str=''):  # 打印Logo
    text = f'''
    __  ___       __  
   /  |/  /___   / /__
  / /|_/ // _ \ / //_/
 / /  / //  __// ,<       v{compile_time}
/_/  /_/ \___//_/|_|  {str}

        '''
    print(text)


def logo_pray():
    srt1111 = r'''
	                   _ooOoo_
	                  o8888888o
	                  88" . "88
	                  (| -_- |)
	                  O\  =  /O
	               ____/`---'\____
	             .'  \\|     |//  `.
	            /  \\|||  :  |||//  \
	           /  _||||| -:- |||||-  \
	           |   | \\\  -  /// |   |
	           | \_|  ''\-/''  |   |
	           \  .-\__  `-`  ___/-. /
	         ___`. .'  /-.-\  `. . __
	      ."" '<  `.___\_<|>_/___.'  >'"".
	     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
	     \  \ `-.   \_ __\ /__ _/   .-` /  /
	======`-.____`-.___\_____/___.-`____.-'======
	                   `=-='
	                 南无阿弥陀佛
    
    '''
    print(srt1111)


def print_class(object):  # 打印对象类型
    print(type(object))


'''数据持久化操作'''


def read_file(file):  # 读取文件
    with open(file, 'r', encoding='utf-8') as file:
        Data = file.read()
        return Data


def write_file(file, Data):  # 写入文件
    with open(file, 'w', encoding='utf-8') as file:
        file.write(str(Data))


def read_file_byte(file):  # 二进制读取
    '''二进制读取模式不接受encoding编码参数'''
    with open(file, 'rb') as file:
        Data = file.read()
        return Data


def write_file_byte(file, Data):  # 二进制写入文件，Data为二进制数据
    '''二进制写入模式不接受encoding编码参数'''
    with open(file, 'wb') as file:
        file.write(Data)


def addition_write_file(file, Data):  # 追加写入文件
    with open(file, 'a+', encoding='utf-8') as file:
        file.write(str(Data))


def read_json(file):  # 读取json文件
    with open(file, 'r', encoding='utf-8') as file:
        Data = json.load(file)
        return Data


def write_json(file, Data):  # 写入json文件
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(Data, file)


def addition_write_json(file, Data):  # 追加写入json文件
    with open(file, 'a+', encoding='utf-8') as file:
        json.dump(Data, file)


def read_csv(file):  # 读取csv文件返回列表
    with open(file, 'r', newline='') as file:
        Data = csv.reader(file)
        lis = []
        for i in Data:
            lis.append(i)
        return lis


def write_csv(file, lis):  # 将嵌套列表写入csv文件
    with open(file, 'w', newline='') as file:
        w = csv.writer(file)
        for Data in lis:
            w.writerow(Data)


'''时间操作'''


def get_localtime():  # 获取本地时间 2022-03-10 14:01:30
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_numbertime():  # 获得数字序列日期 20220310140628
    """获得数字序列日期 20220310140628"""
    localtime = time.localtime()

    def JL(I):  # 判断是否大于10，不大于则加0
        int(I)
        if I < 10:
            I = '0' + str(I)
        return str(I)

    Y = localtime.tm_year
    M = localtime.tm_mon
    M2 = localtime.tm_mday
    M3 = localtime.tm_hour
    M4 = localtime.tm_min
    M5 = localtime.tm_sec
    time_N = JL(Y) + JL(M) + JL(M2) + JL(M3) + JL(M4) + JL(M5)
    return str(time_N)


def from_unix_time(unix):
    """ unix 时间转换时间对象"""
    t = datetime.datetime.fromtimestamp(unix)
    # (datetime.datetime(2023, 3, 17, 19, 3, 8), '2023-03-17 19:03:08')
    # 字符串时间取[-1],时间对象取0
    return t, t.strftime("%Y-%m-%d %H:%M:%S")


def stringtime_to_unix(s):
    """字符串时间转unix"""
    date_time_start = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    unix_time = time.mktime(date_time_start.timetuple())
    return int(unix_time)


def html_stringtime_to_unix(s):
    # 处理HTML前端字符串时间转unix
    # print(s)
    date_time_start = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M")
    unix_time = time.mktime(date_time_start.timetuple())
    return int(unix_time)


'''文件操作'''


class Create_Dir_tree(object):  # 生成目录树
    def __init__(self):
        self.SPACE = ""
        self.list = []

    def getCount(self, url):
        files = os.listdir(url)
        count = 0
        for file in files:
            myfile = url + "\\" + file
            if os.path.isfile(myfile):
                count = count + 1
        return count

    def getDirList(self, url):
        files = os.listdir(url)
        fileNum = self.getCount(url)
        tmpNum = 0

        for file in files:
            myfile = url + "\\" + file
            size = os.path.getsize(myfile)

            if os.path.isfile(myfile):
                tmpNum = tmpNum + 1
                if (tmpNum != fileNum):
                    self.list.append(str(self.SPACE) + "├─" + file + "\n")
                else:  # www.iplaypy.com
                    self.list.append(str(self.SPACE) + "└─" + file + "\n")

            if os.path.isdir(myfile):
                self.list.append(str(self.SPACE) + "├─" + file + "\n")
                # change into sub directory
                self.SPACE = self.SPACE + "│  "
                self.getDirList(myfile)
                # if iterator of sub directory is finished, reduce "│  "
                self.SPACE = self.SPACE[:-4]
        return self.list


def get_osname():  # 获取系统平台
    return os.name


def get_wokerdir():  # 获取当前工作路径
    return os.getcwd()


def run_exec(cmd):  # 运行系统命令
    return os.popen(cmd).read()  # 后台执行 返回命令行打印结果


def get_file_MD5(file):  # 获取文件MD5
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            bytes = f.read(4096)
            if not bytes:
                break
            m.update(bytes)
        return m.hexdigest()


def get_file_SHA1(file):  # 获取文件SHA1
    m = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            bytes = f.read(4096)
            if not bytes:
                break
            m.update(bytes)
        return m.hexdigest()


def get_file_SHA256(file):  # 获取文件SHA256
    m = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            bytes = f.read(4096)
            if not bytes:
                break
            m.update(bytes)
        return m.hexdigest()


def get_file_SHA512(file):  # 获取文件SHA512
    m = hashlib.sha512()
    with open(file, 'rb') as f:
        while True:
            bytes = f.read(4096)
            if not bytes:
                break
            m.update(bytes)
        return m.hexdigest()


def get_file_size(file, rou=2):  # 获取文件大小 默认为Kb,保留小数点后2位
    return round(os.stat(file).st_size / 1024, rou)


def get_file_class(file):  # 获取文件名和后缀
    return [os.path.splitext(file)[0], os.path.splitext(file)[-1]]


def get_dir_allfile(path):
    """获取目录下全部文件"""
    file_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            file_list.append(file_path)

    return file_list


def dir_notis_make(path):
    """文件夹不存在则创建"""
    if not os.path.exists(path):
        os.makedirs(path)


def cp_file(source_file, destination_file):
    """复制文件"""
    shutil.copy(source_file, destination_file)


def cp_dir(source_dir, destination_dir):
    """复制文件夹"""
    shutil.copytree(source_dir, destination_dir)


def cp(source, destination):
    """通用复制函数"""
    if os.path.isdir:
        cp_dir(source, destination)
    if os.path.isfile:
        cp_file(source, destination)


def create_zip(filename, path):
    """压缩文件为zip格式"""
    shutil.make_archive(filename, "zip", path)


def unzip(file, extract_dir='.'):
    """解压缩  extract_dir解压目录，默认为当前目录"""
    dir_notis_make(extract_dir)  # 路径不存在时自动创建
    shutil.unpack_archive(file, extract_dir)


file_path_link = os.path.join  # 文件名链接

mkdir = os.mkdir  # 创建文件夹

mkdirs = os.makedirs  # 递归创建文件夹

rm = os.remove  # 删除文件

rmd = os.rmdir  # 删除空文件夹

rm_rf = shutil.rmtree  # 递归删除文件夹

file_exist = os.path.exists  # 检测文件或目录是否存在。存在返回 True , 不存在返回 False

isfile = os.path.isfile  # 判断是否为文件。是返回 True， 不是返回 False。也可以用来判断文件是否存在。

isdir = os.path.isdir  # 判断是否为目录。是返回 True， 不是返回 False。也可以用来判断目录是否存在。

'''随机数生成'''


def get_uuid1(clock_seq=None):
    '''根据MAC地址和时间生成UUID'''
    return uuid.uuid1(clock_seq=clock_seq)


def get_uuid4():
    return uuid.uuid4()


def get_uuid4_hex():
    Str = uuid.uuid4()
    return Str.hex


def get_random_letters(N=4):
    s = ''
    for i in range(N):
        s += random.choice(string.ascii_uppercase)
    return s


def get_random_numbe(N=4):
    s = ''
    for i in range(N):
        s += random.choice(string.digits)
    return s


def get_random_hax(N=4):
    s = ''
    for i in range(N):
        s += random.choice(string.hexdigits)
    return s


'''对象持久化'''


def write_obj_file(file, obj):  # 对象写入文件
    with open(file, 'wb') as file:
        pickle.dump(obj, file)


def read_obj_file(file):  # 从文件读取对象
    with open(file, 'rb') as file:
        return pickle.load(file)  # 返回恢复后的对象


'''字符串操作'''


def get_string_MD5(str):  # 获取字符串的MD5
    return hashlib.md5(str.encode('utf-8')).hexdigest()


def get_string_SHA256(str):  # 获取字符串的SHA256
    return hashlib.sha256(str.encode('utf-8')).hexdigest()


def get_string_SHA512(str):  # 获取字符串的SHA512
    return hashlib.sha512(str.encode('utf-8')).hexdigest()


def convert_string_list(str='Mek', cut=' '):  # 字符串转列表 str=字符串,cut=分割符
    return str.split(cut)


def runtime_duration(func, info=None):
    """打印函数运行所需时长"""
    """ lambda: func(**args) """

    start = time.time()
    func()
    end = time.time()
    print(f'func:{func}\n{end - start}\n{info}')
    return end - start


# logo_Slabt(get_localtime())
if __name__ == '__main__':
    logo_Slabt()
