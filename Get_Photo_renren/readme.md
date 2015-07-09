获取人人网公开相册照片
===
=========
#步骤
* 登陆人人网 在console中输入 document.cookie
* 复制引号内的cookie,替换config.ini中cookie=XXX内的XXX
* start_dir = 你文件的保存路径
* [person]中为你要获取的照片的人的ID = 姓名
* 程序会以姓名新建文件夹并保存图片
* 进入程序文件夹 执行python myrenrenphoto.py

#环境
* osx 10.10
* python 2.7

#第三方库
* lxml
* requests

#问题
Mac下安装lxml会出现一点小问题,可google解决