import os
import random
import datetime
import time

import Tool.Mek_master as Mm
from Model import *
import Tool.random_name

cars = Car.select(Car.id).count()
#cars = 100
print(cars)


# wg_list = [i for i in Model.WorkingGroup.select(Model.WorkingGroup.id)]


def import_project():
    file = os.path.join('demo', 'project.csv')
    for i in Mm.read_csv(file):
        Project.create(code=i[0], name=i[1], price=i[2])


def import_component():
    file = os.path.join('demo', 'component.csv')
    for i in Mm.read_csv(file):
        print(i)
        Component.create(name=i[1], code=i[0], to_price=i[2], number=1000)


def import_wg():
    WorkingGroup.create(name='临港机修组')
    WorkingGroup.create(name='临港钣金组')
    WorkingGroup.create(name='临港洗车组')
    WorkingGroup.create(name='临港自动洗车')

    WorkingGroup.create(name='南岸机修组')
    WorkingGroup.create(name='南岸钣金组')
    WorkingGroup.create(name='南岸洗车组')
    WorkingGroup.create(name='南岸自动洗车')

    WorkingGroup.create(name='南溪自动洗车')


def random_car():
    car_model = [a[0] for a in Mm.read_csv(os.path.join('demo', 'car.csv'))]

    name = Tool.random_name.get_name(3)
    car = random.choice(car_model) + f' {str(random.randint(2010, 2023))}' + '款'
    distance = random.randint(3000, 10000)
    code = f'临A{Mm.get_random_hax(5).upper()}'
    car_code = Mm.get_random_hax(18)

    Car.create(code=code, car_code=car_code, model=car,
               length=distance,
               master=name, phone=f'1{Mm.get_random_numbe(10)}')


def get_ramdom_car_id():
    ids = random.randint(0, cars)
    return ids-1


class Ptxc:
    def __init__(self, id):
        car = Car.get(id=id)
        car.last_im_time = datetime.datetime.now()
        car.length += random.randint(100, 1000)
        car.save()

        user = User.get(id=2)
        wo = WorkOrder(code=tools.get_workorder_code(), car=car, master=user)
        wo.length = car.length
        wo.save()

        pjct = Project.get(code='XCBZ')
        wg_list = WorkingGroup.select().where(WorkingGroup.name.contains('洗车组'))
        dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=random.choice(wg_list), number=1,
                            price=pjct.price)
        dpsl.save()

        # 完成派单
        wo.workers = True
        wo.go_component = True
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


class Fsxc:
    def __init__(self, id):
        car = Car.get(id=id)
        car.last_im_time = datetime.datetime.now()
        car.length += random.randint(100, 1000)
        car.save()

        user = User.get(id=2)
        wo = WorkOrder(code=tools.get_workorder_code(), car=car, master=user)
        wo.length = car.length
        wo.save()

        pjct = Project.get(code='XCFS')
        wg_list = WorkingGroup.select().where(WorkingGroup.name.contains('自动洗车'))
        dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=random.choice(wg_list), number=1,
                            price=pjct.price)
        dpsl.save()

        # 完成派单
        wo.workers = True
        wo.go_component = True
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


class SDxc:
    def __init__(self, id):
        car = Car.get(id=id)
        car.last_im_time = datetime.datetime.now()
        car.length += random.randint(100, 1000)
        car.save()

        user = User.get(id=2)
        wo = WorkOrder(code=tools.get_workorder_code(), car=car, master=user)
        wo.length = car.length
        wo.save()

        wg_list = WorkingGroup.select().where(WorkingGroup.name.contains('洗车组'))
        wg = random.choice(wg_list)

        pjct = Project.get(code='XCSD')
        dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=wg, number=1,
                            price=pjct.price)
        dpsl.save()

        pjct = Project.get(code='XCJC')
        dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=wg, number=1,
                            price=pjct.price)
        dpsl.save()

        # 完成派单
        wo.workers = True
        wo.go_component = True
        wo.save()

        cp1 = Component.get(code=100001)
        Outbound.create(code=wo.code, workorder=wo, component=cp1, master=user, price=cp1.to_price)
        cp2 = Component.get(code=100002)
        Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)

        if wo.go_component == True and wo.workers == True:
            # print(wo.code, wo.car.code, wo.car.car_code, wo.car.model)

            wg_price = 0  # 用于计算工时费
            for dpsl in DispatchList.select().where(DispatchList.code.contains(wo.code)):
                # print(dpsl.project.csv.name, dpsl.project.csv.price, dpsl.wg.name, dpsl.project.csv.price)
                wg_price += dpsl.project.price * dpsl.number

            outbound_price = 0  # 用于计算材料费
            for outbound in Outbound.select().where(Outbound.code.contains(wo.code)):
                outbound.status = True
                outbound.out_time = datetime.datetime.now()
                outbound.save()
                # print(outbound.component.name, outbound.price)
                outbound_price += outbound.price * outbound.number

            wo.checkout = True

            wo.checkout_time = datetime.datetime.now()
            wo.init_price = wg_price + outbound_price
            wo.real_price = wo.init_price
            wo.save()


class By:
    def __init__(self, id):
        car = Car.get(id=id)
        car.last_im_time = datetime.datetime.now()
        car.length += random.randint(5000, 10000)
        car.save()

        user = User.get(id=2)
        wo = WorkOrder(code=tools.get_workorder_code(), car=car, master=user)
        wo.length = car.length
        wo.save()

        wg_list = WorkingGroup.select().where(WorkingGroup.name.contains('机修'))
        wg = random.choice(wg_list)

        pjct = Project.get(code='AGBYQ')
        dpsl = DispatchList(code=wo.code, workorder=wo, project=pjct, wg=wg, number=1,
                            price=pjct.price)

        dpsl.save()

        # 完成派单
        wo.workers = True
        wo.go_component = True
        wo.save()

        cp1s = Component.select().where(Component.name.contains('昆仑'))
        cp1 = random.choice(cp1s)
        Outbound.create(code=wo.code, workorder=wo, component=cp1, master=user, price=cp1.to_price)

        cp2 = Component.get(code='P98323')
        Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)

        cp2 = Component.get(code='P62781')
        Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)

        cp2 = Component.get(code='HYQQXJ')
        Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)

        if random.randint(1, 10) > 5:
            cp2 = Component.get(code='100001')
            Outbound.create(code=wo.code, workorder=wo, component=cp2, master=user, price=cp2.to_price)

        if wo.go_component == True and wo.workers == True:
            # print(wo.code, wo.car.code, wo.car.car_code, wo.car.model)

            wg_price = 0  # 用于计算工时费
            for dpsl in DispatchList.select().where(DispatchList.code.contains(wo.code)):
                # print(dpsl.project.csv.name, dpsl.project.csv.price, dpsl.wg.name, dpsl.project.csv.price)
                wg_price += dpsl.project.price * dpsl.number

            outbound_price = 0  # 用于计算材料费
            for outbound in Outbound.select().where(Outbound.code.contains(wo.code)):
                outbound.status = True
                outbound.out_time = datetime.datetime.now()
                outbound.save()
                # print(outbound.component.name, outbound.price)
                outbound_price += outbound.price * outbound.number

            wo.checkout = True

            wo.checkout_time = datetime.datetime.now()
            wo.init_price = wg_price + outbound_price
            wo.real_price = wo.init_price
            wo.save()


def timing_random():
    p_list = [Ptxc, Fsxc, SDxc, By]
    while True:
        id = get_ramdom_car_id()
        p = random.choice(p_list)
        p(id)
        time.sleep(10)


def weights_are_random():
    id = get_ramdom_car_id() + 1
    weights = random.randint(1, 1000)
    print(id, weights)
    if weights < 800:
        Fsxc(id)

    elif weights < 900:
        Ptxc(id)

    elif weights > 900 < 980:
        SDxc(id)

    else:
        By(id)


if __name__ == '__main__':
    while True:
        weights_are_random()
        print('------------{}'.format(datetime.datetime.now()))
        #time.sleep(0)
