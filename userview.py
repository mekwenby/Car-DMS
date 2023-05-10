from flask import Blueprint, render_template, request, g, redirect, url_for

import Model.apiengine as mapi
import Tool as tools
from Model import Car, Project

bp = Blueprint('User', __name__)


# 修改密码
@bp.route('/changePassword', methods=['POST'])
def changePassword():
    if request.method == 'POST' and g.user is not None:
        user = g.user
        old_passwd = request.form.get('oldpassword')
        new_passwd = request.form.get('newpassword')
        confirm_passwd = request.form.get('confirm_passwd')

        if tools.passwd_md5(old_passwd) == user.password and new_passwd == confirm_passwd:
            """验证表单信息是否正确"""
            user.password = tools.passwd_md5(new_passwd)
            user.save()
            hint = '密码修改成功!'
            return render_template('UserSettings.html', hint=hint)
        else:
            hint = '密码修改失败! 请检查表单信息是否正确'
            return render_template('UserSettings.html', hint=hint)


# 管理车辆档案
@bp.route('/car')
def car():
    if g.user is not None:
        # key   搜索用，不搜索时为None
        key = request.args.get('key')

        if key is None:
            """
            key 为 空返回所有  数据量过大建议分页或者只显示前N条
            """
            return render_template('Car.html', car_list=mapi.get_car_list())
        else:
            """key 不为空 查找车牌号和车架号相关的数据 合并去重"""
            code_list = [car_ for car_ in Car.select().where(Car.code.contains(f'{key}'))]

            car_code_list = [car_ for car_ in Car.select().where(Car.car_code.contains(f'{key}'))]

            # 列表去重操作
            car_list = list(set(code_list + car_code_list))
            return render_template('Car.html', car_list=car_list)
    else:
        return redirect(url_for('login'))


# 添加车辆信息
@bp.route('/addcar/<code>', methods=['POST', 'GET'])
def addCar(code):
    if g.user is not None:
        """新增时<code>为new"""
        if request.method == 'GET':
            if code == 'new':
                return render_template('AddCar.html')
            else:
                _car = mapi.get_car_carcode(code)
                return render_template('AddCar.html', car=_car)

        elif request.method == 'POST':
            code_ = request.form.get('code')
            car_code = request.form.get('car_code')
            model = request.form.get('model')
            master = request.form.get('master')
            phone = request.form.get('phone')

            if code == 'new':  # 新增流程
                try:
                    mapi.add_car(code_, car_code, model, master, phone)
                    return redirect(url_for('User.car'))
                except:
                    return render_template('Car.html', car_list=mapi.get_car_list(), msg=f'{car_code} 已存在')
            else:  # 修改流程
                car_ = Car.get_or_none(Car.car_code == car_code)
                car_.code = code_
                car_.master = master
                car_.model = model
                car_.phone = phone
                car_.save()
                return redirect(url_for('User.car'))
    else:
        return redirect(url_for('login'))

    # 更新车辆信息


''' 已弃用
---------------------------------------------------
@bp.route('/updatecar', methods=['POST'])
def updateCar():
    return redirect(url_for('page_not_found'))


# 删除车辆信息
@bp.route('/delcar')
def delCar():
    return redirect(url_for('page_not_found'))
--------------------------------------------------
'''


# 工时项目管理页面
@bp.route('/Project')
def Project():
    if g.user is not None:
        key = request.args.get('key')
        if key is None:
            return render_template('Project.html', Project_list=mapi.get_all_project_list())
        else:
            return render_template('Project.html', Project_list=mapi.get_key_project_list(key))
    else:
        return redirect(url_for('login'))


#  添加工时项目
@bp.route('/addProject', methods=['POST'])
def addProject():
    if g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        price = request.form.get('price')
        if mapi.add_project(code=code, name=name, price=price):
            return redirect(url_for('User.Project'))
        else:
            return render_template('Project.html', Project_list=mapi.get_all_project_list(), msg=f'工时代码 {code} 已存在')

    else:
        return redirect(url_for('login'))


# 更新工时项目
@bp.route('/updateProject', methods=['POST'])
def updateProject():
    if g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        price = request.form.get('price')
        if mapi.update_add_project(code=code, name=name, price=price):
            return render_template('Project.html', Project_list=mapi.get_all_project_list(), msg=f'{code} {name} 修改成功')
        else:
            return render_template('Project.html', Project_list=mapi.get_all_project_list(), msg=f'{code} {name} 修改失败')
    else:
        return redirect(url_for('login'))


# 工单管理页面
@bp.route('/WorkOrder')
def WorkOrder():
    return redirect(url_for('page_not_found'))


# 维修班组管理
@bp.route('/WorkingGroup')
def WorkingGroup():
    if g.user is not None:
        key = request.args.get('key')
        if key is None:
            return render_template('WorkingGroup.html', wg_list=mapi.get_all_wg_list())
        else:
            return render_template('WorkingGroup.html', wg_list=mapi.get_key_wg_list(key))
    else:
        return redirect(url_for('login'))


# 添加维修班组
@bp.route('/addWorkingGroup', methods=['POST'])
def addWorkingGroup():
    if g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        if mapi.add_wg(code=code, name=name):
            return redirect(url_for('User.WorkingGroup'))
        else:
            return render_template('WorkingGroup.html', wg_list=mapi.get_all_wg_list(), msg=f'班组代码 {code} 已存在')

    else:
        return redirect(url_for('login'))


@bp.route('/updateWorkingGroup', methods=['POST'])
def updateWorkingGroup():
    if g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        if mapi.update_wg(code=code, name=name):
            return render_template('WorkingGroup.html', wg_list=mapi.get_all_wg_list(), msg=f'{code} {name} 编辑成功')
        else:
            return render_template('WorkingGroup.html', wg_list=mapi.get_all_wg_list(), msg=f'{code} {name} 编辑失败')
    else:
        return redirect(url_for('login'))


# 派工管理页面
@bp.route('/Dispatch')
def Dispatch():
    return redirect(url_for('page_not_found'))


# 结算管理页面
@bp.route('/Checkout')
def Checkout():
    return render_template('Checkout.html')


# 零部件管理页面
@bp.route('/Component')
def Component():
    return render_template('Component.html')


# 零部件出库管理
@bp.route('/ToComponent', methods=['POST', 'GET'])
def ToComponent():
    return render_template('ToComponent.html')


# 零部件入口管理页面
@bp.route('/ImComponent')
def ImComponent():
    return render_template('ImComponent.html')
