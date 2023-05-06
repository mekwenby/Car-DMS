from flask import Blueprint, render_template, request, g, redirect, url_for
import Tool as tools

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
    return redirect(url_for('page_not_found'))


# 添加车辆信息
@bp.route('/addcar', methods=['POST'])
def addCar():
    return redirect(url_for('page_not_found'))


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