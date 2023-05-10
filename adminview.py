from flask import Blueprint, render_template, request, g

import Model.apiengine as mapi
import Tool as tools

bp = Blueprint('A', __name__)


@bp.route('/user')
def user():
    """管理用户的页面"""
    if g.user is not None and g.user.username == 'admin':
        user_list = mapi.get_user_list()
        return render_template('Admin_User.html', user_list=user_list)


@bp.route('/adduser', methods=['POST'])
def adduser():
    """用于处理添加用户操作"""
    if g.user is not None and g.user.username == 'admin':
        username = request.form.get('username')
        password = request.form.get('password')

        if mapi.get_user_by(username) is None:
            if mapi.add_user(username, password):
                user_list = mapi.get_user_list()
                return render_template('Admin_User.html', hint=f'{username} 注册成功', user_list=user_list)
            else:
                user_list = mapi.get_user_list()
                return render_template('Admin_User.html', hint=f'{username} 注册失败', user_list=user_list)
        else:
            user_list = mapi.get_user_list()
            return render_template('Admin_User.html', hint=f'{username} 用户已存在', user_list=user_list)


@bp.route('/reviseuser', methods=['POST'])
def reviseuser():
    """用于处理编辑用户操作"""
    if g.user is not None and g.user.username == 'admin':
        new_passwd = request.form.get('new_passwd')
        disable = request.form.get('disable')
        username = request.form.get('username')
        user = mapi.get_user_ontpasswd(username)
        if user is not None:
            if disable == 'YES':
                user.available = False
            else:
                user.available = True

            if len(new_passwd) >= 4:
                user.password = tools.passwd_md5(new_passwd)

            user.save()
            user_list = mapi.get_user_list()
            return render_template('Admin_User.html', hint=f'{username} 设置成功', user_list=user_list)
        else:
            user_list = mapi.get_user_list()
            return render_template('Admin_User.html', hint=f'{username} 设置失败', user_list=user_list)
