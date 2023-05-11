# 数据库API接口
from Model import *


def get_user(username, passwd):
    '''
    获取用户的信息
    :param passwd:  密码
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
    print('-----------------------', car)
    return car


def add_car(code, car_code, model, master, phone):
    Car.create(code=code, car_code=car_code, model=model, master=master, phone=phone)


def get_all_project_list():
    return [project for project in Project.select().order_by(Project.code)]


def get_key_project_list(key):
    p_name_list = [project for project in Project.select().where(Project.name.contains(f'{key}'))]

    p_code_list = [project for project in Project.select().where(Project.code.contains(f'{key}'))]

    # 列表去重操作
    return list(set(p_name_list + p_code_list))


def add_project(code, name, price):
    """
    添加工时
    查询该工时代码是否有对应工时
    是: 返回 False
    否: 添加新工时并返回 True
    """
    project = Project.get_or_none(Project.code == code)
    if project is None:
        Project.create(code=code, name=name, price=price)
        return True
    else:
        return False


def update_add_project(code, name, price):
    """
    修改工时信息
    :param code:
    :param name:
    :param price:
    :return: bl
    """
    p = Project.get_or_none(Project.code == code)
    try:
        p.name = name
        p.price = price
        p.save()
        return True
    except:
        return False


def get_all_wg_list():
    return [wg for wg in WorkingGroup.select().order_by(WorkingGroup.code)]


def get_key_wg_list(key):
    wg_name_list = [wg for wg in WorkingGroup.select().where(WorkingGroup.name.contains(f'{key}'))]

    wg_code_list = [wg for wg in WorkingGroup.select().where(WorkingGroup.code.contains(f'{key}'))]

    # 列表去重操作
    return list(set(wg_name_list + wg_code_list))


def add_wg(code, name):
    """
    添加班组
    """
    wg = WorkingGroup.get_or_none(WorkingGroup.code == code)
    if wg is None:
        WorkingGroup.create(code=code, name=name)
        return True
    else:
        return False


def update_wg(code, name):
    wg = WorkingGroup.get_or_none(WorkingGroup.code == code)
    try:
        wg.name = name
        wg.save()
        return True
    except:
        return False


def get_all_component_list():
    return [component for component in Component.select().order_by(Component.name)]


def get_key_component_list(key):
    component_name_list = [component for component in
                           Component.select().where(Component.name.contains(f'{key}')).order_by(Component.name)]
    component_code_list = [component for component in
                           Component.select().where(Component.code.contains(f'{key}')).order_by(Component.name)]
    # 列表去重操作
    return list(set(component_name_list + component_code_list))


def add_component(code, name, price, position):
    """
    添加组件信息
    """
    cp = Component.get_or_none(Component.code == code)
    if cp is None:
        Component.create(code=code, name=name, to_price=price, position=position)
        return True
    else:
        return False


def get_all_ImComponent():
    # 列表去重
    return list(set([a for a in Inbound.select().where(Inbound.status == False).order_by(Inbound.create_time)]))


def createImComponent(uid):
    """

    :param uid:     创建人id
    :return: coe
    """
    user = User.get(id=uid)
    code = tools.get_ImComponent_code()
    Inbound.create(code=code, master=user)
    return code


def get_ImComponent(code):
    return [a for a in Inbound.select().where(Inbound.code == code)]


def delImComponent(code):
    # 删除
    Inbound.delete().where(Inbound.code == code).execute()


def addImComponent(ids, code, number, im_price, info):
    icp = Inbound.get_or_none(Inbound.code == ids)
    cp = Component.get_or_none(Component.code == code)

    Inbound.create(code=ids, component=cp, price=im_price, number=number, master=icp.master, info=info)


if __name__ == '__main__':
    c = get_car_carcode('DK965231')
    print(c)
