# -

使用前先看word文档

确保chromedriver.exe 与两个py文件在同一文件下、

使用： python main_weiban.py   (python3环境哦)

微伴自动刷课
需要安装selenium 、ddddocr
pip install selenium   //有问题就百度吧
pip install ddddocr

在main_weiban.py 里面配置好自己的信息

![image](https://github.com/user-attachments/assets/69aead24-9583-45fa-9bf6-f83590426b21)


注意有的学校可能输入 信息后会弹出一个对话框这是需要你自己去点击的
例如（如果不弹出就不用管）


![image](https://github.com/user-attachments/assets/3ad189e9-6416-464f-8b0c-bc3ec0f0a59e)


	
还有的学校再点击课程的时候会弹出公众号是否关注（弹出--》取消注释|不弹--》不用取消）

![image](https://github.com/user-attachments/assets/1c6963ef-0dfe-44b7-8545-38fc3850c948)


这部分对应代码

![image](https://github.com/user-attachments/assets/2487ae90-39ba-493a-bbd6-c56269e9983d)

默认是注释掉的

代码是使用的selenium模块外加强制等待，不会自动答题想要答题自己去油猴找一个就可以了，速度肯定没有网络请求那么快，不过是自己没事写着玩的，bug也会有很多，希望大家多提提意见，毕竟这是自己的第一个项目。

使用前先看word文档 如果有其他课程修改下按钮属性就可以刷了
