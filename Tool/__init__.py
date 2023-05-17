import Tool.Mek_master as Mm


def get_workorder_code():
    """
    获取一个工单号
    :return:
    """
    return Mm.get_numbertime() + Mm.get_random_hax(6)


def get_ImComponent_code():
    """
    获得一个入库单号
    :return:
    """
    return Mm.get_numbertime() + '-' + Mm.get_random_hax(3)


def passwd_md5(passwd):
    """获取密码的MD5码"""
    return Mm.get_string_MD5(passwd)


def set_token():
    """生成一个随机的TOKEN"""
    return Mm.get_random_hax(32)


def get_name_md5(name):
    """生成一个名字的MD5码 并返回后几位"""
    """用于模板自定义过滤器使用"""
    return Mm.get_string_MD5(name)[-5:]


def get_random_hax():
    return Mm.get_random_hax(16)


if __name__ == '__main__':
    print(get_workorder_code())
