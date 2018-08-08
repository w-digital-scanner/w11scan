# Docker 安装w11scan

## 注意
docker安装方式仅为测试w11scan的单机安装方案（主控和节点在一个docker里），不是节点安装方式。如果想使用docker部署分布式节点需要自行修改`Dockerfile`文件，或联系作者提供帮助。

## 安装
1. 到项目根目录，输入命令
```
docker build -t w11scan:1.0 .
```
这样docker便打包完毕
2. 因为在启动docker的时候会向mongodb添加指纹信息，所以速度会比较慢。用下面的命令查看进度。
```docker run -it -p 666:8000 w11scan:1.0```
当然，你也可以放到后台执行
```docker run -d -p 666:8000 w11scan:1.0```
3. 打开http://127.0.0.1:666  账号密码为 admin w11scan
4. Enjoy it!
