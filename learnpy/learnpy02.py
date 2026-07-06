#异常处理、断言


#!/usr/bin/python
# -*- coding: UTF-8 -*-

try:
    fh = open("testfile", "w", encoding="utf-8")
    fh.write("这是一个测试文件，用于测试异常!!")
except IOError:
    print("Error: 没有找到文件或读取文件失败")
else:
    print("内容写入文件成功")
    fh.close()
    
    
#try-finally 语句无论是否发生异常都将执行最后的代码
try:
    fh = open("testfile2", "w", encoding="utf-8")
    fh.write("这是一个测试文件，用于测试异常!!")
finally:
    print("Error: 没有找到文件或读取文件失败")
    
#异常的参数
#变量接收的异常值通常包含在异常的语句中。在元组的表单中变量可以接收一个或者多个值
#元组通常包含错误字符串，错误数字，错误位置
def temp_convert(var):
    try:
        return int(var)
    except ValueError as Argument:  # 如果发生 ValueError，把错误信息塞给 Argument
        print("参数没有包含数字\n", Argument)

a=temp_convert("xyz")  # 传入一个字符串，无法转换成数字
print(a)

#触发异常,raise 语句可以用来触发一个指定的异常
#raise [Exception [, args [, traceback]]]
# 定义函数
def mye( level ):
    if level < 1:
        raise Exception("Invalid level!")
        # 触发异常后，后面的代码就不会再执行
        
try:
    mye(5)            # 触发异常
except Exception as err:
    print(1,err)
else:
    print(2)