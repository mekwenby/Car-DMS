from flask import Flask, render_template, url_for, request, g, make_response, redirect, abort
from flask_bootstrap import Bootstrap4

import Model.apiengine as mapi
import Tool as tools
from adminview import bp as adminview
from userview import bp as userview

app = Flask(__name__)
bootstrap = Bootstrap4(app=app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# 挂载蓝图 --------------------------
app.register_blueprint(userview, url_prefix='/User')
app.register_blueprint(adminview, url_prefix='/A')


# 自定义过滤器 -----------------------
@app.template_filter('time_ftm')
def time_ftm(value):
    """将数据库读取的时间格式化为Web页面显示格式"""
    if value is not None:
        print(value)
        x = '{:%Y-%m-%d %H:%M:%S}'.format(value)
        print(x)
        return x
    else:
        return None


@app.template_filter('md5')
def get_username_md5(value):
    """获取字符串的md5,用于前端模态框绑定"""
    return f'Lab{tools.get_name_md5(value)}'


# 请求前钩子函数
@app.before_request
def examine_cookie():
    """验证Cookie"""
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    user = mapi.get_user_by_token(username, token)
    g.user = user


# 404 处理
@app.errorhandler(404)
def page_not_found(e):
    """
    处理404页面问题
    这个 ‘e’ 我也不知道是什么
    """
    return render_template('404.html'), 404


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        check = request.form.get('check')
        # 获取用户
        user = mapi.get_user(username, tools.passwd_md5(passwd))

        if user is not None and user.username != 'admin' and user.available == True:  # 普通用户登录
            print(user.username)
            if check == 'on':  # 今日自动登录
                resp = make_response(redirect(url_for('hello_world')))
                """
                cookie有效期等于 60秒*60分钟*16小时
                """
                resp.set_cookie('username', user.username, max_age=int(60 * 60 * 16))
                resp.set_cookie('token', user.token, max_age=int(60 * 60 * 16))
                return resp
            else:  # 今日不自动登录
                resp = make_response(redirect(url_for('hello_world')))
                resp.set_cookie('username', user.username)
                resp.set_cookie('token', user.token)
                return resp
        elif user is not None and user.username == 'admin':  # 管理员登录
            print(user.username, 'admin')
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('username', user.username)
            resp.set_cookie('token', user.token)
            return resp
        elif user is not None and not user.available:
            hint = '''
                        <hr>
                        <div class="alert alert-danger" role="alert">该用户已被停用</div>
                        '''
            return render_template('Login.html', hint=hint)
        else:  # 用户名或密码错误
            hint = '''
            <hr>
            <div class="alert alert-danger" role="alert">用户名或密码错误</div>
            '''
            return render_template('Login.html', hint=hint)


# 注销页面
@app.route('/logout')
def logout():
    if g.user is not None:
        resp = make_response(redirect(url_for('login')))
        resp.delete_cookie('username')
        resp.delete_cookie('token')
        return resp
    else:
        return redirect(url_for('login'))


# 用户设置 用于用户自己修改密码
@app.route('/UserSettings')
def user_settings():
    if g.user is not None:
        return render_template('UserSettings.html')
    else:
        return redirect(url_for('login'))


# 首页
@app.route('/')
def hello_world():
    if g.user is not None:
        user = g.user
        return render_template('Index.html', user=user)
    else:
        return redirect(url_for('login'))


# 管理员界面
@app.route('/admin')
def admin():
    if g.user is not None and g.user.username == 'admin':
        return render_template('Admin.html')
    else:
        return redirect(url_for('hello_world'))


@app.route('/404')
def page_not_found():
    """404 not found page"""
    abort(404)


def recover():
    import Model
    Model.recover()
    Model.create_demo_data()


if __name__ == '__main__':
    app.run(debug=True)
