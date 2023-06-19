import sys
from server import app, recover

"""
debug=True      打开调试模式
recover         初始化数据库

docker init db
docker exec dms_web_1 python main.py recover

"""

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'recover':
        recover()
    app.run(host='0.0.0.0', debug=True)
