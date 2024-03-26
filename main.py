import flask
import json
import time

app = flask.Flask(__name__)


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
    print(members)  # Debug
    return flask.render_template('index.html', members=members)


# upload
@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if flask.request.method == 'POST': # 上传ing
        file = flask.request.files["upload"]
        file.save("static/uploads/" + file.filename)
        return "Upload Successfully."
    else: # 上传前
        # 渲染模板并返回
        return flask.render_template('upload.html')
    # file = flask.request.files["upload"]
    # file.save("static/uploads/" + file.filename)
    # return "Upload Successfully."


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True, port=5001)
