# 数据库API接口
from Model import *
import Tool as tools


def get_user(username, passwd):
    '''
    获取用户的信息
    :param username: 用户名
    :return: 用户的信息
    '''
    user = User.get_or_none(User.username == username,
                            User.password == passwd)

    """
    如果用户名或密码错误则返回空
    """
    if user is not None:
        user.token = tools.set_token()
        user.last_login_time = datetime.datetime.now()
        user.save()
        return user
    else:
        return None


def get_user_by_token(username, token):
    """
    :param username:
    :param token:
    :return:
    """
    user = User.get_or_none(User.username == username,
                            User.token == token)
    return user


def get_user_ontpasswd(name):
    user = User.get_or_none(User.username == name)
    return user


def get_user_by(name):
    """
    查询用户是否存在
    不存在返回None
    """
    user = User.get_or_none(User.username == name)
    if user is not None:
        return True
    elif user is None:
        return None
    else:
        return False


def add_user(username, passwd):
    '''
    创建用户
    :param username:
    :param passwd:
    '''
    try:
        user = User(username=username, password=tools.passwd_md5(passwd))
        user.save()
        return True
    except:
        return False


def get_user_list():
    """获取用户列表"""
    return [user for user in User.select()]


def get_car_list():
    return [car for car in Car.select()]


def get_car_carcode(code):
    car = Car.get_or_none(Car.car_code == code)
    print('-----------------------',car)
    return car


def add_car(code, car_code, model, master, phone):
    Car.create(code=code, car_code=car_code, model=model, master=master, phone=phone)

if __name__ == '__main__':
    c = get_car_carcode('DK965231')
    print(c)