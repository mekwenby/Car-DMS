from flask import Blueprint, render_template, request, g, redirect, url_for, make_response
import Tool as tools
import Model.apiengine as mapi
from Model import Car

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
        key = request.args.get('key')
        print(key)
        if key is None:
            return render_template('Car.html', car_list=mapi.get_car_list())
        else:

            code_list = [car_ for car_ in Car.select().where(Car.code.contains(f'{key}'))]
            print(code_list)
            car_code_list = [car_ for car_ in Car.select().where(Car.car_code.contains(f'{key}'))]
            print(car_code_list)
            car_list = list(set(code_list + car_code_list))
            return render_template('Car.html', car_list=car_list)
    else:
        return redirect(url_for('login'))


# 添加车辆信息
@bp.route('/addcar/<code>', methods=['POST', 'GET'])
def addCar(code):
    if g.user is not None:
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


@bp.route('/updatecar', methods=['POST'])
def updateCar():
    return redirect(url_for('page_not_found'))


# 删除车辆信息
@bp.route('/delcar')
def delCar():
    return redirect(url_for('page_not_found'))


# 工时项目管理页面
@bp.route('/Project')
def Project():
    return redirect(url_for('page_not_found'))


#  添加工时项目
@bp.route('/addProject')
def addProject():
    return redirect(url_for('page_not_found'))


# 更新工时项目
@bp.route('/updateProject')
def updateProject():
    return redirect(url_for('page_not_found'))


# 工单管理页面
@bp.route('/WorkOrder')
def WorkOrder():
    return redirect(url_for('page_not_found'))


# 维修班组管理
@bp.route('/WorkingGroup')
def WorkingGroup():
    return redirect(url_for('page_not_found'))


# 添加维修班组
@bp.route('/addWorkingGroup')
def addWorkingGroup():
    return redirect(url_for('page_not_found'))


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
