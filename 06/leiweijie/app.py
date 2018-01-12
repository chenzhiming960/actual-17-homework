# encoding: utf-8
from flask import Flask, request,render_template,redirect, session, flash
from  Log_Analysis import GetTopN
from functools import wraps
import userdb as user
from dbutils import execute_sql

app = Flask(__name__)
app.secret_key = '13123dfasdf'

# 登陆验证装饰器
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session:
            return redirect('/login/')
        ret = func(*args, **kwargs)
        return ret
    return inner


@app.route('/')
@login_required
def hello_world():
    title = '51Reboot'
    content = ['hello Nick','hello Reboot']
    return render_template('index.html',contents=content)


@app.route('/logs/')
@login_required
def logs():
    topn = request.args.get('topn')
    # 三目表达式
    topn = int(topn) if str(topn).isdigit() else 10
    title = 'Reboot'
    sql = 'select * from accesslog order by count desc limit %s'
    args = (topn,)
    count,log_list =  execute_sql(sql, args, fetch=True)
    return render_template('logs.html',title=title,logall_list=log_list )


@app.route('/login/',methods=['POST','GET'])
def Login():
    username = request.form.get('username')
    password =  request.form.get('password')
    if request.method == 'GET':
        return render_template('login.html')
    if user.vilidate_login(username,password):
        session['user'] = {'username':username}
        # 跳转到首页
        return redirect('/user/list/')
    else:
        return render_template('login.html',username=username,error=u'用户名或密码错误!')

@app.route('/user/list/')
@login_required
def UserList():
    all_user = user.get_user()
    return render_template('user_list.html',user_list=all_user)

@app.route('/user/add/',methods=['POST','GET'])
@login_required
def UserAdd():
    name = request.form.get('name')
    age = request.form.get('age','')
    passwd = request.form.get('passwd','')
    job = request.form.get('job','')
    if request.method == 'GET':
        return render_template('user_add.html')
    elif request.method == 'POST':
        _is_ok, error = user.vilidate_find(name,passwd,age,job)
        if _is_ok:
            flash(error)
            return render_template('user_add.html')
        else:
            if user.add_user(name,passwd,age,job):
                flash(u'添加: %s成功'%name)
                return redirect('/user/list/')
            else:
                return render_template('user_add.html', error=u'用户写入失败.')


@app.route('/user/delete/',methods=['GET'])
@login_required
def user_delete():
    perams = request.args if request.method == 'GET' else request.form
    uid = perams.get('uid','')
    _user = user.get_user_by_id(uid=uid)[0]
    if user.user_delete(_user['id']):
        flash(u'删除: %s成功' % _user['username'])
        return redirect('/user/list/')
    else:
        return '用户删除失败.'


@app.route('/user/update/',methods=['POST','GET'])
@login_required
def user_update():
    perams = request.args if request.method == 'GET' else request.form
    uid = perams.get('uid','')
    age = perams.get('age','')
    job = perams.get('job','')
    _user = user.get_user_by_id(uid=uid)[0]
    if request.method=='GET':
        return render_template("user_update.html",_user=_user)
    if user.user_update(uid=uid, age=age, job=job):
        flash(u'更新：%s成功' % _user['username'])
        return redirect('/user/list/')
    if str(job) ==_user['job'] and int(age) ==_user['age']:
        flash(u'更新：%s成功' % _user['username'])
        return redirect('/user/list/')        
    else:
        print uid,age,job,_user['job'],_user['age']
        return '用户更新失败'

# 用户登出
@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

