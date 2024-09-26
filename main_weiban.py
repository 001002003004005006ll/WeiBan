#!/usr/bin/python 
# -- coding: utf-8 --
# author:未央

import WeiBan


# 输入登录账号
account = '你的账号'
# 输入登录密码
passwd = '你的密码'
# 输入学校名称
school_name = '你的学校'
if __name__ == '__main__':
	WeiBan.login(account, passwd, school_name)
	WeiBan.get_student_info()
	WeiBan.go_to_course()
	WeiBan.get_big_class_list()
	WeiBan.course()

