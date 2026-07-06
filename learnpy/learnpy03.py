#函数与类
#装饰器
from functools import wraps
##在函数中定义函数
def hi(name="yasoob"):
    print("now you are inside the hi() function")
 
    def greet():
        return "now you are in the greet() function"
 
    def welcome():
        return "now you are in the welcome() function"
 
    print(greet())
    print(welcome())
    print("now you are back in the hi() function")
 
hi()
 
# 无论何时你调用hi(), greet()和welcome()将会同时被调用。
# 然后greet()和welcome()函数在hi()函数之外是不能访问的，比如：
 
#手动实现一个装饰器
##装饰器封装一个函数，并且用这样或者那样的方式来修改它的行为！
def a_new_decorator(a_func):
 
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
 
        a_func()
 
        print("I am doing some boring work after executing a_func()")
 
    return wrapTheFunction
 
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")
 
a_function_requiring_decoration()

##装饰器返回修改/增强后的新函数——重新赋值给原函数名——覆盖原函数
##不改原函数的代码，为原函数增添额外的功能
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

a_function_requiring_decoration()
print(a_function_requiring_decoration.__name__)
#output：wrapTheFunction ，不是我们想要的输出，Ouput输出应该是"a_function_requiring_decoration"
# 这里的函数被warpTheFunction替代了，它重写了我们函数的名字和注释文档(docstring)
# Python提供给我们一个简单的函数来解决这个问题，那就是functools.wraps

print("——————————————————————————————————————————————————————————————")

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("drop dead is good")
        a_func()
        print("stupid song is great")
    return wrapTheFunction

@a_new_decorator
def a_func_require_dec():
    print("the cure is yaya's best song")
    
print(a_func_require_dec.__name__)
a_func_require_dec()
print("——————————————————————————————————————————————————————————————")

#带条件拦截的装饰器
def decorator_name(f):                     #接收目标函数
    @wraps(f)                              #保护原函数f的函数名和注释文档
    def decorated(*args, **kwargs):        #定义代理/包装函数，args与kwargs是参数的魔法打包与解包机制
                                           # *args（元组打包）：把所有位置参数（比如 1, 2, 3）打包成一个元组（Tuple）
                                           # **kwargs（字典打包）：把所有关键字参数（比如 a=1, b=2, c=3）打包成一个字典（Dict）
                                           #它们俩组合起来，就等于无论你原函数长什么样、传多少个参数，我这个代理方法都能一网打尽、全盘接收
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)          #核心执行：放行并返回结果，原函数 f 执行完之后，可能会有返回值
    return decorated
 
@decorator_name
def func():
    return("Function is running")

can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run
print("——————————————————————————————————————————————————————————————")

#带参数的装饰器
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrap_forward(*args,**kwargs):
            log_string=func.__name__ + "\t was used"
            print(log_string)
            with open(logfile,'a') as open_file:
                open_file.write(log_string + '\n')
                #wrapped_function 里的 return func(...) 是把原函数的执行结果透传出去，这样调用者感知不到函数被包装过
            return func(*args,**kwargs)
        return wrap_forward
    return logging_decorator

@logit(logfile='func2.log')
def myfunc2():
    print("this is myfunc2")
    
myfunc2()