# w11scan 安装
w11scan使用的技术有celery、Django、redis、mongodb，
下面的安装步骤大都是配置这些软件 = -  
因为所使用的软件在linux/windows/osx都可以找到，理论上w11scan可以在三系统任一运行,但开发环境是在ubuntu。
 
## linux下安装

### 1. 下载redis并配置（可使用阿里/腾讯云上redis服务）
### 2. 下载mongodb并配置（可使用阿里/腾讯云上mongodb服务）
1. 导入数据库
```
mongorestore -h 127.0.0.1 --port 65521 -d w11scan backup/w11scan
```
2. 进入mongo shell,,建立全局索引 
```
use w11scan_config
db.result.createIndex({"$**":"text"})
```
### 3. 下载python3
### 4. 安装python相关库 
```
pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```
### 5. 配置w11scan相关
 1. 修改config.py 相关数据库参数
 2. 生成Django session
 ```
 python manage.py makemigrtations
 python manage.py migrate
```
## 运行WEB端
```python manage.py runserver```
默认账号密码: admin w11scan
## 运行节点
```celery -A whatcms worker -l info```
