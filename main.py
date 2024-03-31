import flask
import json
import time

app = flask.Flask(__name__)
app.secret_key = 'xf438q2ipnc42yr32iwf2eq6dr321r431'  # Needed for flash messages to work


def update_json(member_name: str, words: int):  # 写入数据
    """

    :param words:
    :type member_name: str
    """
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    print(data)
    for item in data:
        if item.value()["name"] == member_name:
            item.value()["words"] += words
            item.value()["last_update"] = time.strftime("%Y-%m-%d")
            break
    with open('static/data.json', 'w') as file:
        json.dump(data, file)


# test
@app.route("/test")
def test():
    return "Hello, World!!!"


# index
@app.route("/")
def index():
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    print(data)  # Debug
    members = list(data.values())  # 转列表
    members = sorted(members, key=lambda x: -x["words"])  # 排序
    for member in members:  # 隐藏更新日期，保护部分隐私
        del member["last_update"]
        del member["password"]
    print(members)  # Debug
    return flask.render_template('index.html', members=members, logged_in=('username' in flask.session))


# upload
@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if flask.request.method == 'POST':  # 上传ing
        file = flask.request.files["upload"]
        file.save("static/uploads/" + file.filename)
        # 异步处理OCR
        return "Upload Successfully."
    else:  # 上传前
        # 渲染模板并返回
        return flask.render_template('upload.html')
    # file = flask.request.files["upload"]
    # file.save("static/uploads/" + file.filename)
    # return "Upload Successfully."


def valid_login(username: str, password: str):
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    members = list(data.values())  # 转列表
    for member in members:
        if member["name"] == username and member["password"] == password:
            # 别忘了.value()
            return True
    return False


@app.route("/login", methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':
        if valid_login(flask.request.form['username'], flask.request.form['password']):
            return "Login Successfully"
        else:
            # return "Error"
            # 这样子就能够在错误的时候重新返回登录页面，但是还不能显示错误提示。
            flask.flash("Wrong Username/Password")
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template('login.html')


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True, port=5001)
