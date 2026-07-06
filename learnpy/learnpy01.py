#四种推导式
#迭代器与生成器

import sys
#列表推导式
name=['John', 'Jane', 'Doe', 'Smith', 'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
new_name=[name.upper() for name in name]
print(new_name)

#字典推导式
new2_name={name.upper():len(name)for name in name}
print(new2_name)

dic={x : x**2 for x in (2,4,6)}
print(dic)

#集合推导式
new_set={x**2 for x in(1,2,3,4,5)}
print(new_set)

new2_set={x for x in'abracabredabra' if x not in'abc'}
print(new2_set)
print(type(new2_set))

#元组推导式（生成器表达式），元组推导式可以利用 range 区间、元组、列表、字典和集合等数据类型，快速生成一个满足指定需求的元组
a=(x for x in range(1,10))
print(a)       #返回生成器对象——特殊的迭代器，要一个数，他才会给你一个数，不会直接输出所有数、生成器是一次性的（不可逆）
tuple_b=next(a)   
tuple_c=next(a)   
print(tuple_c)    
print(tuple_b)    
tuple_a=tuple(a)   #将生成器对象转换为元组
print(tuple_a)     #输出元组

#迭代器与生成器
#访问集合元素的一种方式，是一个可以记住遍历的位置的对象，迭代器只能往前不会后退，迭代器是一个对象，生成器是一个函数
#迭代器有两个基本方法：iter() 和 next()
list=[1,2,3,4,5,6]
it=iter(list)  #创建一个迭代器对象
while True:
    try:
        print(next(it))  #输出迭代器的下一个元素
    except StopIteration:
        break
        
# print(next(it))  #输出迭代器的下一个元素
# print(next(it))
# print(next(it))
# for x in it:
#     print (x, end=" ")

#把一个类作为一个迭代器使用需要在类中实现两个方法 __iter__() 与 __next__()
#__iter__() 方法返回一个特殊的迭代器对象， 这个迭代器对象实现了 __next__() 方法并通过 StopIteration 异常标识迭代的完成
#__next__() 方法（Python 2 里是 next()）会返回下一个迭代器对象
#在 Python 中，任何一个类只要实现了 __iter__() 和 __next__() 这两个魔法方法（Magic Methods），它就变成了一个迭代器类
class Xws:
    def __iter__(self):
        self.a=1     #初始化计数器
        return self     #必须返回迭代器对象本身
    
    def __next__(self):
        if self.a>5:
            raise StopIteration
        x=self.a
        self.a+=1
        return x
    
x=Xws()
for i in x:
    print(i)
x_iter=iter(x)
print(next(x_iter))
print(next(x_iter))
print(next(x_iter))
print(next(x_iter))
print(next(x_iter))

#生成器
#使用了 yield 的函数被称为生成器（generator），yield 是一个关键字，用于定义生成器函数
#当在生成器函数中使用 yield 语句时，函数的执行将会暂停，并将 yield 后面的表达式作为当前迭代的值返回
#每次调用生成器的 next() 方法或使用 for 循环进行迭代时，函数会从上次暂停的地方继续执行，直到再次遇到 yield 语句
#调用一个生成器函数，返回的是一个迭代器对象
#生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器
def count(n):
    while n> 0:
        try:
            yield n
            n-=1
        except StopIteration:
            break
        
xu= count(5)
print(next(xu))
print(next(xu))
print(next(xu))
print(next(xu))
print(next(xu))

for value in count(5):
    print(value)
    

def fibonacci(n): # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n): 
            return
        yield a
        a, b = b, a + b
        counter += 1
f = fibonacci(10) # f 是一个迭代器，由生成器返回生成
 
print(next(f)) # 输出斐波那契数列的下一个值
print(next(f))
print(next(f))  
print(next(f))
print(next(f))

# while True:
#     try:
#         print (next(f), end=" ")
#     except StopIteration:
#         sys.exit()








