from flask import Blueprint, render_template, request, g, redirect, url_for, flash
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
@bp.route('/WorkOrder', methods=['POST', 'GET'])
def WorkOrder():
    if g.user is not None and request.method == 'GET':
        key = request.args.get('key')
        if key is None:
            car_list = []
        else:
            car_list = mapi.get_car_key_list(key)

        wo_list = mapi.get_wo_list()
        print(wo_list)
        return render_template('WorkOrder.html', car_list=car_list, wo_list=wo_list)
    else:
        return redirect(url_for('login'))


# 添加工单
@bp.route('/addWorkOrder/<code>', methods=['POST', 'GET'])
def addWorkOrder(code):
    if g.user is not None and request.method == 'GET':
        # print(code)
        mapi.addWo(code, g.user)
        return redirect(url_for('User.WorkOrder'))
    else:
        return redirect(url_for('login'))


# 编辑工单
@bp.route('/editWO/<code>', methods=['POST', 'GET'])
def editWO(code):
    if g.user is not None and request.method == 'GET':
        lc = request.args.get('lc')
        fand = request.args.get('fand')
        print('lc:',lc)
        # 处理 fand 的空字符
        if fand == '':
            fand = None

        # 处理里程修改
        if lc is not None:
            if not mapi.update_car_distance(code, int(lc)):
                flash('数值输入错误')

        # 处理工时项目查找
        if fand is not None:
            """
            fand_c_list :   零部件列表
            fand_p_list :   工时项目列表
            没有时返回空列表
            """
            fand_c_list = mapi.get_key_component_list(fand)
            fand_p_list = mapi.get_key_project_list(fand)
            print(fand_c_list, fand_p_list)
        else:
            fand_c_list = list()
            fand_p_list = list()

        wo_list = mapi.get_wo_Dispatch_and_Outbound(code)

        return render_template('editWO.html', wo=mapi.get_wo_code(code),
                               fand_c_list=fand_c_list, fand_p_list=fand_p_list,
                               wo_dispatch_list=wo_list[0], wo_onbound_list=wo_list[1])
    else:
        return redirect(url_for('login'))


# 删除工单
@bp.route('/delwo/<code>', methods=['GET'])
def deleteWO(code):
    if g.user is not None and request.method == 'GET':
        mapi.delete_wo(code)
        return redirect('/User/WorkOrder')
    else:
        return redirect(url_for('login'))


# 删除工时或者零部件
@bp.route('/delfand/<code>/<wo_code>', methods=['GET'])
def deleteFand(code, wo_code):
    if g.user is not None and request.method == 'GET':
        mapi.delete_fand(wo_code=wo_code, code=code)
        return redirect(f'/User/editWO/{wo_code}')
    else:
        return redirect(url_for('login'))


# 添加工时项目和零部件
@bp.route('/addTimeProd/<code>/<class_>', methods=['POST'])
def addTimeProd(code, class_):
    if g.user is not None and request.method == 'POST':

        if class_ == 'P':
            p_code = request.form.get('code')
            number = request.form.get('number')
            price = request.form.get('price')
            mapi.wo_add_p(wo_code=code, p_code=p_code, number=number, price=price)
        elif class_ == 'C':
            c_code = request.form.get('code')
            number = request.form.get('number')
            price = request.form.get('price')
            mapi.wo_add_c(wo_code=code, c_code=c_code, number=number, price=price)

        return redirect(f'/User/editWO/{code}')


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


# 更新维修班组
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
    if g.user is not None and request.method == 'GET':
        key = request.args.get('key')
        if key is None:
            car_list = []
        else:
            car_list = mapi.get_car_key_list(key)

        wo_list = mapi.get_wo_list()
        print(wo_list)
        return render_template('Dispatch.html', car_list=car_list, wo_list=wo_list)
    else:
        return redirect(url_for('login'))


# 开始派工
@bp.route('/Startdispatch/<wo_code>', methods=['POST', 'GET'])
def Startdispatch(wo_code):
    if g.user is not None and request.method == 'GET':
        wo = mapi.get_wo_code(wo_code)
        dispatch_list = mapi.get_wo_Dispatch(wo)
        return render_template('Startdispatch.html', wo=wo, dispatch_list=dispatch_list, wg_list=mapi.get_all_wg_list())

    if g.user is not None and request.method == 'POST':
        pid = request.form.get('pid')
        wg = request.form.get('wg')
        mapi.start_dispatch(pid, wg)

        return redirect(f'/User/Startdispatch/{wo_code}')

    else:
        return redirect(url_for('login'))


@bp.route('/StartTC/<wo_code>', methods=['POST', 'GET'])
def StartTC(wo_code):
    if g.user is not None and request.method == 'GET':
        wo = mapi.get_wo_code(wo_code)
        outbound_list = mapi.get_wo_Outbound(wo)
        print(outbound_list)
        return render_template('StartTC.html', wo=wo, outbound_list=outbound_list)
    else:
        return redirect(url_for('login'))


# 确认出库
@bp.route('/StartTCOK/<wo_code>/<tcid>')
def StartTCOK(wo_code, tcid):
    if g.user is not None and request.method == 'GET':
        wo = mapi.get_wo_code(wo_code)
        mapi.start_tc_ok(wo=wo, tcid=tcid, user=g.user)
        return redirect(f'/User/StartTC/{wo_code}')
    else:
        return redirect(url_for('login'))


# 退库
@bp.route('/StartTCON/<wo_code>/<tcid>')
def StartTCON(wo_code, tcid):
    if g.user is not None and request.method == 'GET':
        wo = mapi.get_wo_code(wo_code)
        mapi.start_tc_on(wo=wo, tcid=tcid, user=g.user)
        return redirect(f'/User/StartTC/{wo_code}')
    else:
        return redirect(url_for('login'))


# 结算管理页面
@bp.route('/Checkout', methods=['GET', 'POST'])
def Checkout():
    if g.user is not None and request.method == 'GET':
        wo_list = mapi.get_wo_list()
        print(wo_list)
        return render_template('Checkout.html', wo_list=wo_list)
    elif g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        price = request.form.get('price')
        real_price = request.form.get('real_price')
        mapi.checkout(wo_code=code, price=price, real_price=real_price)
        return redirect(url_for('User.Checkout'))


    else:
        return redirect(url_for('login'))


# 零部件管理页面
@bp.route('/Component')
def Component():
    if g.user is not None:
        key = request.args.get('key')
        if key is None:
            return render_template('Component.html', component_list=mapi.get_all_component_list())
        else:
            return render_template('Component.html', component_list=mapi.get_key_component_list(key))
    else:
        return redirect(url_for('login'))


@bp.route('/addComponent', methods=['POST'])
def addComponent():
    if g.user is not None and request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        price = request.form.get('price')
        position = request.form.get('position')
        if mapi.add_component(code=code, name=name, price=price, position=position):
            return redirect(url_for('User.Component'))
        else:
            return render_template('Component.html', component_list=mapi.get_all_component_list(), msg=f'{code} 已存在')

    else:
        return redirect(url_for('login'))


# 零部件出库管理
@bp.route('/ToComponent', methods=['POST', 'GET'])
def ToComponent():
    if g.user is not None and request.method == 'GET':
        wo_list = mapi.get_wo_list()
        print(wo_list)
        return render_template('ToComponent.html', wo_list=wo_list)
    else:
        return redirect(url_for('login'))


# 零部件入口管理页面
@bp.route('/ImComponent')
def ImComponent():
    if g.user is not None:
        return render_template('ImComponent.html', documents_list=mapi.get_all_ImComponent())
    else:
        return redirect(url_for('login'))


# 创建入库单
@bp.route('/createImComponent/<id>')
def createImComponent(id):
    """
    入库单管理
    id:         入库单号
    创建时为new
    """
    if g.user is not None:
        if id == 'new':
            mapi.createImComponent(g.user.id)
            flash('新建入库单成功！')
            return redirect(url_for('User.ImComponent'))
    else:
        return redirect(url_for('login'))


# 编辑入库单
@bp.route('/editImComponent/<ids>', methods=['POST', 'GET'])
def editImComponent(ids):
    if g.user is not None and request.method == 'GET':
        imcomponent_list = mapi.get_ImComponent(ids)
        key = request.args.get('key')
        if key == '':
            component_list = []
        else:
            component_list = mapi.get_key_component_list(key)
        return render_template('editImComponent.html', imcomponent_list=imcomponent_list, ids=ids,
                               component_list=component_list)
    elif g.user is not None and request.method == 'POST':
        ids = ids
        code = request.form.get('code')
        number = request.form.get('n')
        im_price = request.form.get('p')
        info = request.form.get('info')
        mapi.addImComponent(ids=ids, code=code, number=number, im_price=im_price, info=info)
        return redirect(f'/User/editImComponent/{ids}')
    else:
        return redirect(url_for('login'))


# 删除入库单
@bp.route('/delImComponent/<id>')
def delImComponent(id):
    if g.user is not None:
        mapi.delImComponent(id)
        return redirect(url_for('User.ImComponent'))
    else:
        return redirect(url_for('login'))


# 删除入库明细
@bp.route('/delImComponentid/<eid>/<ids>')
def delImComponentid(eid, ids):
    if g.user is not None:
        mapi.delImComponentid(eid)
        return redirect(f'/User/editImComponent/{ids}')
    else:
        return redirect(url_for('login'))


# 提交入库单
@bp.route('/postImComponent/<ids>')
def postImComponent(ids):
    if g.user is not None:
        mapi.postImComponent(ids)
        flash(f'{ids} 提交成功！')
        return redirect(url_for('User.ImComponent'))
    else:
        return redirect(url_for('login'))
