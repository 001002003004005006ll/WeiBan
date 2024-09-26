#!/usr/bin/python 
# -- coding: utf-8 --
# author:未央

import WeiBan


# 输入登录账号
account = '411525200607192124'
# 输入登录密码
passwd = '192124'
# 输入学校名称
school_name = '厦门城市职业学院'
if __name__ == '__main__':
	WeiBan.login(account, passwd, school_name)
	WeiBan.get_student_info()
	WeiBan.go_to_course()
	WeiBan.get_big_class_list()
	WeiBan.course()

