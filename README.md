环境依赖：

python 3.5+
ubuntu 16.04
pip
    sudo apt-get install python3-pip
    pip3 install --upgrade pip
    pip -V

virtualenv
    pip install virtualenv
    virtualenv --no-site-packages venv
    source venv/bin/activate

pip install requests
pip install psycopg2
pip install pycrypto

pip freeze > requirements.txt

安装requirements.txt依赖
pip install -r requirements.txt

一些敏感不同步git文件说明：

keys.py中主要存储数据库连接、接口API等敏感信息：

server_database_demo = {
    'database': 'DATABASE',
    'user': 'USERNAME',
    'password': 'PASSWORD',
    'host': 'DB_HOST',
    'port': '5432'
}