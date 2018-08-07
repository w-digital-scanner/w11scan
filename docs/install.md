# w11scan 安装
w11scan使用的技术有celery、Django、redis、mongodb，
下面的安装步骤大都是配置这些软件 = - 
因为所使用的软件在linux/windows/osx都可以找到，理论上w11scan可以在三系统任一运行,但开发环境是在ubuntu。
以下安装方式由作者从一个纯净的ubuntu实验，亲测成功。

## ubuntu下安装

### 1. 安装python3,pip,下载软件,安装依赖
```
sudo apt install python3
sudo apt install python3-pip
sudo apt install python-celery-common
sudo apt install git
git clone https://github.com/boy-hack/w11scan
cd w11scan
pip3 install -r requirement.txt
```

### 2. 安装redis、mongodb、导入指纹数据
```
sudo apt install redis-server (下载完成后默认运行)
sudo apt install mongodb
```
接着导入指纹
`mongorestore -h 127.0.0.1 --port 65521 -d w11scan backup/w11scan`
接着输入`mongo`进入mongodb shell
`use dbs`
查看是否有w11scan数据库创建，有则创建成功。  
接着对结果进行全文索引。
依然在mongodb shell状态下
```
use w11scan_config
db.result.createIndex({"$**":"text"})
```
完成后exit退出。

### 3. 软件config配置
1. 修改config.py，按照提示配置redis、mongodb用户名密码(如果按上面操作进行的，默认即可)
2. 生成django的session
```
python3 manage.py migrate
```

## 运行WEB端
```python manage.py runserver```
默认账号密码: admin w11scan
## 运行节点
```celery -A whatcms worker -l info```

## 注意
上述为单机配置方案，多节点布置需将redis、mongodb服务配置到公网，运行节点即可。若部署有错误可mail:dzhheUBxcS5jb20=
