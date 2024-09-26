#!/usr/bin/python 
# -- coding: utf-8 --
# author:未央


from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # 修正为Chrome的Service
import time
from selenium.webdriver.common.by import By
import ddddocr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



ser = Service(r'./chromedriver.exe')  # 直接在初始化时指定路径
driver = webdriver.Chrome(service=ser)
# driver.implicitly_wait(10)
driver.get('https://weiban.mycourse.cn/#/login')
# time.sleep(20)


def login(account, passwd,school_name):
	ocr = ddddocr.DdddOcr(show_ad=False)
	school = driver.find_element(By.XPATH, '//*[@id="app"]/div/section/section[2]/section[1]/label[1]/input').click()
	time.sleep(0.3)
	school_input = driver.find_element(By.XPATH,'//*[@id="app"]/div/section/div[1]/div[1]/div/div[2]/div/input').send_keys(school_name)
	time.sleep(0.3)
	school_click = driver.find_element(By.XPATH, '//*[@id="app"]/div/section/div[2]/div[3]/div').click()

	# 输入用户名和密码
	time.sleep(1)
	# 输入用户名 这里是绝对路径 相对路径达不到
	username = driver.find_element(By.XPATH, '/html/body/div/div/section/section[2]/section[1]/label[2]/input')
	username.send_keys(account)
	# 输入密码 相对路径
	password = driver.find_element(By.XPATH, '//*[@id="app"]/div/section/section[2]/section[1]/label[3]/input')
	password.send_keys(passwd)
	# 验证码输入框
	code = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入右图验证码"]')

	# 找到验证码图片
	img_code = driver.find_element(By.CSS_SELECTOR, 'img[class="loginp-label-verify"]')

	result = ocr.classification(img_code.screenshot_as_png)
	# print(result)
	code.send_keys(result)
	# 点击登录按钮
	login_button = driver.find_element(By.CSS_SELECTOR, 'a[class="loginp-submit"]').click()
	time.sleep(2)
	html = driver.page_source
	while '调查问卷' in html:
		print('登录成功')
		time.sleep(3)
		break

	else:
		print('登录失败')
		# time.sleep(1)
		# 验证码输入框
		code2 = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入右图验证码"]')
		time.sleep(0.2)
		code2.clear()
		print('正在重新输入验证码')
		time.sleep(1)
		# 找到验证码图片
		img_code2 = driver.find_element(By.CSS_SELECTOR, 'img[class="loginp-label-verify"]')
		result_refresh = ocr.classification(img_code2.screenshot_as_png)
		print(result_refresh)
		# 输入验证码
		code2.send_keys(result_refresh)
		# driver.execute_script("arguments[0].value = '{}';".format(result_refresh), code2)
		print("输入新的验证码")
		# 点击登录按钮
		login_button = driver.find_element(By.CSS_SELECTOR, 'a[class="loginp-submit"]').click()
		time.sleep(2)
		# 在这里重新获取页面源
		html = driver.page_source
		time.sleep(1)

def get_student_info():
	# 点击我的获取学生信息
	image_element1 = driver.find_element("xpath", "//img[@src='./static/img/icon-tarbar-mine.3fab209.png']")
	image_element1.click()
	time.sleep(2)
	# 点击学生信息
	student_info_element = driver.find_element("xpath", "//div[@class='homep-material-content']")
	student_info_element.click()  # 点击学生信息
	time.sleep(1)
	# 定位学生姓名和学号等信息 元素并打印
	student_front = driver.find_elements("xpath", "//span[@class='info-container-item-left']")
	student_after = driver.find_elements("xpath", "//span[@data-v-45d83be4 and not(@class)]")
	for front, after in zip(student_front, student_after):
		print(front.text, after.text)
	#点击主页 返回主页进行刷课操作
	image_element1 = driver.find_element("xpath", "//img[@src='./static/img/icon-tarbar-home.597e000.png']")
	image_element1.click()
	time.sleep(2)


#先看这里需要修改不？第106行的关注
def go_to_course():

	time.sleep(2)
	# 定位图片元素
	image_element2 = driver.find_element(By.CSS_SELECTOR, 'img[class="task-block-img"]')
	# 点击图片
	image_element2.click()
	time.sleep(2)
	# 定位关注按钮元素并点击
	# 注意这里如果在点击新生教育课程图片后没有出现关注按钮，那就把下面一行代码注销
	#follow_link = driver.find_element("xpath", "//a[text()='已关注']").click()
	time.sleep(2)
	# 找到目标span标签
	span_element = driver.find_element("xpath", "//span[@class='van-tab__text']")
	# 提取文本并分割
	span_text = span_element.get_attribute('innerHTML')  # 获取HTML内容
	texts = span_text.split('<br')  # 按照<br>进行分割
	# 提取并清理结果
	title = texts[0].strip()  # 课程学习
	number = texts[1].replace('data-v-3d121d09="">', '').strip()  # 120/120
	# 打印结果
	print("课程名称:", title)
	print("数量:", number)
def get_big_class_list():
	look_big_course_name = []
	# 定位大课程名称元素并打印 找到包含特定数据属性和类名的div元素
	big_course_name = driver.find_elements("xpath", "//div[@data-v-3d121d09='' and @class='text']")
	for look_big_course_name2 in big_course_name:
		look_big_course_name.append(look_big_course_name2.text)
	# 打印结果
	print("大课程名称:", look_big_course_name)


	course(big_course_name,look_big_course_name)


def finish_course(html_content):
	if 'class="page-WH page-video"' in html_content:
		print("该小课程动画页面为视频，采用page-WH-evideo方法")
		time.sleep(0.5)
		# 再次查找<section>元素并设置onclick属性
		section_element = driver.find_element(By.CSS_SELECTOR, 'section[class="page-WH page-video"]')
		# 设置 onclick 属性
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')",
							  section_element)
		# print("成功设置canvas的onclick属性")
		time.sleep(1)
		section_element_click = driver.find_element(By.CSS_SELECTOR,
													'section[class="page-WH page-video"]').click()
		# print("点击section")
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		img_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.mai-capta-pattern > img[src]')))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", img_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

	elif '点击播放' and '<html class="page-WH"' in html_content:
		print("页面包含动画视频直接使用page-WH方法")
		section_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
			(By.CSS_SELECTOR, "section.page-WH.page-item.page-start.page-active")))
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')",
							  section_element)
		# print("设置onclick属性")
		time.sleep(1)
		# 查找并点击<div class="page-slide">
		slide_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable(
				(By.CSS_SELECTOR, "section.page-WH.page-item.page-start.page-active")))
		# slide_element.click()
		driver.execute_script("arguments[0].click();", slide_element)
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		canvas_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern > img[src]")))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", canvas_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)
		driver.switch_to.default_content()
		# print("切换回主文档")
	# time.sleep(1)


	elif '点击播放' in html_content:
		print("该小课程页面只包含视频，采用视频方法")
		time.sleep(1)
		page_div = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.page")))
		# 修改 onclick 属性
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')", page_div)
		# print("设置onclick属性")
		time.sleep(1)
		# 等待 <h2> 标签可见后再查找
		h2_element = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.XPATH, "//h2[@class='h2']")))
		# 点击 <h2> 标签
		h2_element.click()
		# print("点击h2")
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		canvas_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern > img[src]")))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", canvas_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)



	elif ("page-WH" in html_content):
		time.sleep(1)
		print("该小课程页面只包含page-WH使用常规方法")
		time.sleep(1)
		# 再次查找<section>元素并设置onclick属性
		section_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
			(By.CSS_SELECTOR, "section.page-WH.page-item.page-start.page-active")))
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')",
							  section_element)
		# print("设置onclick属性")
		time.sleep(1)
		# 查找并点击<div class="page-slide">
		slide_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.page-slide")))
		slide_element.click()
		# print("点击slide")
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		canvas_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern > img[src]")))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", canvas_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)
		driver.switch_to.default_content()
		print("切换回主文档")
	# time.sleep(1)


	elif "page-none page-item page-start page-active" in html_content:

		print("该小课程页面包含page-none page-item page-start page-active")
		time.sleep(1)
		# 再次查找<section>元素并设置onclick属性
		print("该小课程页面包含page-none采用第三种方法")
		time.sleep(1)
		section_element = driver.find_element(By.CSS_SELECTOR,
											  'section[class="page-none page-item page-start page-active"]')
		# 设置 onclick 属性
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')",
							  section_element)
		# print("成功设置canvas的onclick属性")
		time.sleep(1)
		section_element_click = driver.find_element(By.CSS_SELECTOR,
													'section[class="page-none page-item page-start page-active"]').click()
		# print("点击canvas")
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		img_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.mai-capta-pattern > img[src]')))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", img_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)


	else:
		# 找到canvas元素

		print("尝试最后一种方法")

		small_canvas = driver.find_element(By.CSS_SELECTOR, "canvas#canvas")
		# print("找到canvas")

		# 设置 onclick 属性
		driver.execute_script("arguments[0].setAttribute('onclick', 'finishWxCourse();')", small_canvas)
		# print(driver.page_source)
		# print("成功设置canvas的onclick属性")
		time.sleep(1)
		# 点击canvas
		small_canvas_onclick = driver.find_element(By.CSS_SELECTOR, "canvas#canvas").click()
		# print("点击canvas")
		time.sleep(3)
		# 第一次点击
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		mai_capta_container.click()
		# print("课后问答1")
		time.sleep(3)

		# 使用 WebDriverWait 等待 <div> 标签可点击
		mai_capta_pattern = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mai-capta-pattern")))
		# 点击该元素
		mai_capta_pattern.click()
		# print("课后问答2")
		time.sleep(3)

		# 第三次点击
		# 切换到 iframe 中
		# print("尝试第三次点击")
		# 使用 WebDriverWait 等待 <canvas> 标签可点击
		img_element = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.mai-capta-pattern > img[src]')))
		# 尝试使用JS点击canvas元素
		driver.execute_script("arguments[0].click();", img_element)
		# print("课后问答3")
		time.sleep(1)

		# 规定范围内找到要点击的元素  点击 '继续学习' 按钮
		mai_capta_container = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mai-capta-container")))
		continue_learning_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.LINK_TEXT, "继续学习")))
		continue_learning_button.click()
		# print("点击 '继续学习' 按钮")

		# 切换回主文档 (确保不在 iframe 中)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)

		# print("尝试返回列表")

		# 查找并点击返回列表按钮
		return_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, "//button[@class='comment-footer-button']")))
		return_button.click()
		# print("点击 返回列表 按钮")
		time.sleep(3)
		driver.switch_to.default_content()
		# print("切换回主文档")
		time.sleep(1)


def course(big_course_name,look_big_course_name):
	for index, name in enumerate(big_course_name):
		# 第一个大课程默认展开显示
		if index == 0:
			print(index + 1, "大课程名称:", name.text)
			small_course_list = []
			small_course_name = driver.find_elements("xpath", "//h5[@class='title van-multi-ellipsis--l2']")
			# 打印小课程名称

			for smale_name in small_course_name:
				small_course_list.append(smale_name.text)
			# print(small_course_list)

			small_course_list = list(filter(None, small_course_list))
			print("小课程列表:", small_course_list)
			# 遍历小课程列表

			for look_course_name in small_course_list:

				small_course_name_element = driver.find_element("xpath", "//*[text()=\"{}\"]".format(look_course_name))

				small_course_name_element2 = driver.find_element("xpath","//*[text()=\"{}\"]/..".format(look_course_name))
				small_course_name_element2_txt = small_course_name_element2.get_attribute("outerHTML")
				# print(small_course_name_element2_txt)
				if "passed" in small_course_name_element2_txt:
					print(look_course_name, "该课程已完成")
				else:
					# print(look_course_name, "该课程未完成")
					print("正在学习小课程:", look_course_name)

					# 滚动到当前元素
					driver.execute_script("arguments[0].scrollIntoView();", small_course_name_element)
					# 显式等待，直到元素可点击
					# print(current_element.text)
					time.sleep(1)
					# WebDriverWait(driver, 10).until(EC.element_to_be_clickable(small_course_name_element))
					# 点击小课程名称
					# small_course_name_element.click()
					driver.execute_script("arguments[0].click();", small_course_name_element)
					time.sleep(3)
					# print("切换到iframe")
					WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe")))
					driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))

					# html_content = driver.page_source

					time.sleep(2)
					html_content = driver.page_source
					# print(type(html_content))
					# print(html_content)
					# 检查是否找到了该元素
					finish_course(html_content)

		if len(big_course_name) > index >= 1:  # 0 是第一个课程，1 是第二个课程
			for index in range(1, len(big_course_name)):
				name = big_course_name[index]
			continue_big_look_course = look_big_course_name[1:]

			for look_big_name in continue_big_look_course:
				driver.switch_to.default_content()
				# time.sleep(1)
				print("当前大课程名称:", look_big_name)
				#     # 打印课程名称
				#     # 确保元素在视口中可见 滚动到元素位置
				continue_big_look_course_name_element = driver.find_element("xpath",
																			"//*[text()=\"{}\"]".format(look_big_name))
				driver.execute_script("arguments[0].scrollIntoView();", continue_big_look_course_name_element)
				#     # 显式等待，直到元素可点击
				#     print("继续学习的大课程名称:", look_big_name)

				# 显式等待，直到元素可点击
				WebDriverWait(driver, 15).until(EC.element_to_be_clickable(continue_big_look_course_name_element))
				# 点击大课程名称
				continue_big_look_course_name_element.click()
				time.sleep(3)

				small_course_list = []
				small_course_name = driver.find_elements("xpath", "//h5[@class='title van-multi-ellipsis--l2']")
				# 打印小课程名称

				for smale_name in small_course_name:
					small_course_list.append(smale_name.text)
				# print(small_course_list)

				small_course_list = list(filter(None, small_course_list))
				print("小课程列表:", small_course_list)
				# 遍历小课程列表

				for look_course_name in small_course_list:

					small_course_name_element = driver.find_element("xpath","//*[text()=\"{}\"]".format(look_course_name))

					small_course_name_element2 = driver.find_element("xpath","//*[text()=\"{}\"]/..".format(look_course_name))
					small_course_name_element2_txt = small_course_name_element2.get_attribute("outerHTML")
					# print(small_course_name_element2_txt)
					if "passed" in small_course_name_element2_txt:
						print(look_course_name, "该课程已完成")
					else:
						# print(look_course_name, "该课程未完成")
						print("正在学习小课程:", look_course_name)
						# 滚动到当前元素
						driver.execute_script("arguments[0].scrollIntoView();", small_course_name_element)
						# 显式等待，直到元素可点击
						# print(current_element.text)
						time.sleep(1)
						# WebDriverWait(driver, 10).until(EC.element_to_be_clickable(small_course_name_element))
						# 点击小课程名称
						# small_course_name_element.click()
						driver.execute_script("arguments[0].click();", small_course_name_element)
						time.sleep(3)
						# print("切换到iframe")
						WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe")))
						driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))

						# html_content = driver.page_source

						time.sleep(2)
						html_content = driver.page_source
						finish_course(html_content)

		else:
			print("没有找到课程")

