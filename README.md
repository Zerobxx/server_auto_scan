**程序入口：**

`python3  auto_server_scan.py	#自动从运维数据库提取扫描`

`python3 manual_server_scan.py	#将从前端url界面上显示ip按钮获得的ip输入ips文件后执行`



**环境依赖：**

python 3.5+

ubuntu 16.04

pip:

```shell
    sudo apt-get install python3-pip
    pip3 install --upgrade pip
    pip -V
```

virtualenv:

```shell
    pip install virtualenv
    virtualenv --no-site-packages venv
    source venv/bin/activate
```

```shell
pip install requests
pip install psycopg2
pip install pycrypto
```



使用requirements.txt解决依赖：

```shell
pip freeze > requirements.txt
pip install -r requirements.txt
```



**keys.py中主要存储数据库连接、接口API等敏感信息（所以不同步到git库）：**

```python
server_database_demo = {
    'database': 'DATABASE',
    'user': 'USERNAME',
    'password': 'PASSWORD',
    'host': 'DB_HOST',
    'port': '5432'
}
```

AES_key：加密key

AES_iv：偏移量

authority：授权header

diables_url：API接口