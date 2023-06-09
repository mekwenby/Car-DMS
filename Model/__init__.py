import datetime
import pymysql
from peewee import *
import random
import Tool as tools
import Tool.Mek_master as Mm

# db = SqliteDatabase('sqlite.db')


# 使用 MySQL 数据库
db_mysql = MySQLDatabase(host='db', port=3306, user='root',  # 连接MySQL
                         passwd='passwd', database='DMS')

db = db_mysql


class BaseModel(Model):
    """创建基础模型类,用于指定数据库"""

    class Meta:
        database = db
        # database = db_mysql


class User(BaseModel):
    """
    登录用户表
    username: str       用户名
    password: str       密码,md5加密
    available: bool     是否可用
    funclimit: str      权限管理
    last_login_time     最后登录时间
    token               令牌
    """
    id = AutoField(primary_key=True)
    username = CharField(max_length=30, index=True)
    password = CharField(max_length=128)
    available = BooleanField(default=True)
    funclimit = CharField(default='', null=True)
    token = CharField(max_length=64, null=True)
    last_login_time = DateTimeField(null=True)


class WorkingGroup(BaseModel):
    """
    工作组表
    available: bool     是否可用
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=32, unique=True, default=lambda: Mm.get_random_letters(6))
    name = CharField(max_length=128, index=True)
    available = BooleanField(default=True)


class Component(BaseModel):
    """
    零件表
    code: str        编码
    name: str        名称
    number: int      库存数量
    im_price: float  入库价格
    to_price: float  出库价格
    position: str    货架位置
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=128, index=True)
    name = CharField(max_length=256, index=True)
    number = IntegerField(default=0)
    im_price = FloatField(default=0.0)
    to_price = FloatField(default=0.0)
    position = CharField(null=True)


class Project(BaseModel):
    """
    工时项目
    code: str        编码
    name: str        名称
    price: float     工时价格
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=128, index=True)
    name = CharField(max_length=256, index=True)
    price = FloatField(default=0.0)


class Car(BaseModel):
    """
    车辆
    id_code: str        车牌号
    car_code: str       车架号
    model: str          品牌和车型
    length: int         行驶里程 KM
    master: str         车主
    phone: str          车主电话
    last_im_time:       最后进店时间
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=12, index=True, )
    car_code = CharField(max_length=128, unique=True)
    model = CharField(max_length=128, null=True)
    length = IntegerField(default=0)
    master = CharField(max_length=32, null=True)
    phone = CharField(max_length=16, null=True)
    last_im_time = DateTimeField(null=True)


class WorkOrder(BaseModel):
    """
    维修工单
    code: str           工单号
    create_time         创建时间
    checkout_time       结算时间
    car:                车
    master:             开单人
    workers：            派工状态
    go_component        出库状态
    checkout            结算状态
    init_price          应收金额
    real_price          实收金额
    info                备注信息
    delete_             删除标记
    length              进店里程
    """

    id = AutoField(primary_key=True)
    code = CharField(max_length=128, unique=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    checkout_time = DateTimeField(null=True)
    car = ForeignKeyField(Car, backref='work_order')
    master = ForeignKeyField(User, backref='work_order')
    workers = BooleanField(default=False)
    go_component = BooleanField(default=False)
    init_price = FloatField(default=0.0)
    real_price = FloatField(default=0.0)
    checkout = BooleanField(default=False)
    info = CharField(null=True)
    delete_ = BooleanField(default=False)
    length = IntegerField(default=0)


class Outbound(BaseModel):
    """
    出库记录
    code            与工单一致
    master          出库人
    price           价格
    status          出库状态
    out_time        出库时间
    number          数量
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=128)
    workorder = ForeignKeyField(WorkOrder, backref='outbound')
    component = ForeignKeyField(Component, backref='outbound')
    master = ForeignKeyField(User, backref='Outbound', null=True)
    number = IntegerField(default=1)
    price = FloatField(default=0.0)
    status = BooleanField(default=False)
    out_time = DateTimeField(null=True)


class DispatchList(BaseModel):
    # 派工单
    id = AutoField(primary_key=True)
    code = CharField(max_length=128)
    workorder = ForeignKeyField(WorkOrder, backref='DispatchList')
    project = ForeignKeyField(Project, backref='DispatchList')
    wg = ForeignKeyField(WorkingGroup, backref='DispatchList', null=True)
    price = FloatField(default=0.0)
    number = IntegerField(default=1)


class Inbound(BaseModel):
    """
    入库单记录表
    code            单号
    master          入库人
    price           价格
    number          入库数量
    status          入库状态
    in_time         入库时间
    info            备注信息
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=128)
    component = ForeignKeyField(Component, backref='Inbound', null=True)
    price = FloatField(default=0.0)
    number = IntegerField(default=1)
    create_time = DateTimeField(default=datetime.datetime.now)
    in_time = DateTimeField(null=True)
    status = BooleanField(default=False)
    master = ForeignKeyField(User, backref='Inbound')
    info = TextField(null=True)


def create_table():
    """
    创建表
    """
    db.connect()
    db.create_tables([User, WorkingGroup, Component, Project, Car, WorkOrder, Outbound, DispatchList, Inbound],
                     safe=True)

    init_passwd = Mm.get_random_letters(8)
    User.create(username='admin', password=Mm.get_string_MD5(init_passwd))
    print(f"数据库初始化完成,管理员用户名: admin，密码为: {init_passwd}")

    db.close()


def create_demo_workorder(ids):
    # 业务数据模拟
    # 获取车辆

    car = Car.get(Car.id == ids)
    # print(car.code)
    car.last_im_time = datetime.datetime.now()
    car.save()

    # print(car.code, car.master, car.last_im_time)
    # 获取用户
    user = User.get(id=2)
    # print('开单用户', user.username)
    wo = WorkOrder(code=tools.get_workorder_code(), car=car, master=user)
    wo.save()

    # 创建工时
    pjct = Project.get(id=1)
    wg = WorkingGroup.get(id=1)
    dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=wg, number=180)

    dpsl.save()

    # 创建部件需求单
    cp1 = Component.get(id=1)
    cp2 = Component.get(id=2)
    cp3 = Component.get(id=3)
    # print('开始创建出库单')
    Outbound.create(code=wo.code, workorder=wo, component=cp1, master=user, price=cp1.to_price)
    Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)
    Outbound.create(code=wo.code, workorder=wo, component=cp3, master=user, price=cp3.to_price)
    # print('出库单创建完成')

    # 完成出库
    outbound_list = [o for o in Outbound.select().where(Outbound.code.contains(wo.code))]
    # print(outbound_list)
    for outbound in outbound_list:
        # print(outbound.id)
        outbound.status = True
        outbound.out_time = datetime.datetime.now()
        outbound.save()
        # print(outbound.component.name, "完成出库!")
    wo.go_component = True
    wo.save()

    # 完成派单
    wo.workers = True
    wo.save()

    if wo.go_component == True and wo.workers == True:
        # print(wo.code, wo.car.code, wo.car.car_code, wo.car.model)

        wg_price = 0  # 用于计算工时费
        for dpsl in DispatchList.select().where(DispatchList.code.contains(wo.code)):
            # print(dpsl.project.csv.name, dpsl.project.csv.price, dpsl.wg.name, dpsl.project.csv.price)
            wg_price += dpsl.project.price * dpsl.number

        outbound_price = 0  # 用于计算材料费
        for outbound in Outbound.select().where(Outbound.code.contains(wo.code)):
            # print(outbound.component.name, outbound.price)
            outbound_price += outbound.price * outbound.number

        wo.checkout = True

        wo.checkout_time = datetime.datetime.now()
        wo.init_price = wg_price + outbound_price
        wo.real_price = wo.init_price
        wo.save()

        # print(f'工时费:{wg_price},材料费:{outbound_price},合计:{wg_price + outbound_price}')


def create_demo_data():
    """生成演示数据"""
    # 生成演示用户
    User.create(username='demo', password=Mm.get_string_MD5('123456'))
    # 生成工作组
    WorkingGroup.create(name='机修组')
    WorkingGroup.create(name='钣金组')
    # 生成部件
    Component.create(code=Mm.get_random_hax(6), name='美孚SL 5W30 4L', im_price=265.0, to_price=286, number=7,
                     position='A1-11')
    Component.create(code=Mm.get_random_hax(4), name='火炬450mm通用机油滤清器', im_price=12.0, to_price=15, number=10,
                     position='A1-21')
    Component.create(code='HYQQXJ', name='化油器清洗剂', im_price=8.0, to_price=10, number=36)

    Component.create(code='KL5W30', name='昆仑5W30 4L', im_price=8.0, to_price=185, number=0)
    Component.create(code='KL0W20', name='昆仑0W20 4L', im_price=8.0, to_price=215, number=0)
    Component.create(code='KL5W40', name='昆仑5W40 4L', im_price=8.0, to_price=195, number=0)

    Component.create(code='GHPDK-113', name='高合高性能刹车片-113', im_price=0, to_price=288, number=0)
    Component.create(code='GHPDK-128', name='高合高性能刹车片-128', im_price=0, to_price=388, number=0)
    Component.create(code='GHPDK-417', name='高合高性能刹车片-417', im_price=0, to_price=688, number=0)

    Component.create(code='ADD-P-47', name='ADD卡钳', im_price=0, to_price=1888, number=0)
    Component.create(code='ADD-P-36', name='ADD卡钳', im_price=0, to_price=2888, number=0)
    Component.create(code='ADD-P-28', name='ADD卡钳', im_price=0, to_price=1265, number=0)

    # 生成工时类型
    Project.create(code='0000', name="通用工时", price=1)
    Project.create(code=Mm.get_random_letters(4), name="普通洗车", price=30)
    Project.create(code=Mm.get_random_letters(4), name="深度洗车", price=128)
    Project.create(code=Mm.get_random_letters(4), name="常规保养", price=120)
    Project.create(code=Mm.get_random_letters(4), name="四轮定位", price=80)
    # 生成车辆
    for _ in range(100):
        Car.create(code=f'临A{Mm.get_random_hax(5).upper()}', car_code=Mm.get_random_hax(18), model='大众捷达 2021款 白色',
                   length=34561,
                   master='ACE', phone=f'1{Mm.get_random_numbe(10)}')

        Car.create(code=f'临A{Mm.get_random_hax(5).upper()}', car_code=Mm.get_random_hax(18), model='奥迪A3 2019款 白色',
                   length=int(Mm.get_random_numbe(5)),
                   master='Demos', phone=f'1{Mm.get_random_numbe(10)}')


def recover():
    """还原数据库默认设置"""
    db.drop_tables([User, WorkingGroup, Component, Project, Car, WorkOrder, Outbound, DispatchList, Inbound])
    db.close()
    create_table()


if __name__ == '__main__':
    pass
