import asyncio
import time
import aiohttp
async def say_hello():
    print("Hello")
    await asyncio.sleep(5)
    print("World")
    
async def fetch_url(session,url):
    print(f"开始获取{url}")
    async with session.get(url) as response:
        await asyncio.sleep(2)
        context=await response.text()
    print(f"获取{url}完成，内容长度：{len(context)}")

async def main():
    urls = ['https://httpbin.org/get', 'https://httpbin.org/delay/1', 'https://httpbin.org/headers']
    async with aiohttp.ClientSession() as session:
        tasks=[]
        for url in urls:
            task=asyncio.create_task(fetch_url(session,url))
            tasks.append(task)
        print("所有任务已创建，开始并发执行...")
        result=await asyncio.gather(*tasks)
        return result

if __name__ == "__main__":
    start_time=time.time()
    final_results=asyncio.run(main())
    end_time=time.time()

    print(f"总耗时: {end_time - start_time:.2f} 秒")
    for res in final_results:
        print(res)