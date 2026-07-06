import re
import os
from pathlib import Path

from llm_client import OpenAICompatibleClient
from prompts import AGENT_SYSTEM_PROMPT
from tools.weather import get_weather
from tools.search_attraction import get_attraction


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file(Path(__file__).resolve().parents[1] / ".env")

# --- 0. 配置工具函数 ---
# 将所有工具函数放入一个字典，方便后续调用
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

# --- 1. 配置LLM客户端 ---
# 请根据您使用的服务，将这里替换成对应的凭证和地址
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
MODEL_ID = "claude-sonnet-4-6"
TAVILY_API_KEY= os.environ.get("TAVILY_API_KEY")
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

# --- 2. 初始化 ---
user_prompt = "你好，请帮我查询一下今天南京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)

# --- 3. 运行主循环 ---
for i in range(5): # 设置最大循环次数
    print(f"--- 循环 {i+1} ---\n")
    
    # 3.1. 构建Prompt
    full_prompt = "\n".join(prompt_history)
    
    # 3.2. 调用LLM进行思考
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    # 模型可能会在 Action 后附加“伪执行结果”文本：
    # - 工具调用时只保留 Action 当行
    # - Finish[...] 时允许跨行，直到匹配到结束的 ]
    match = re.search(r'(Thought:[\s\S]*?Action:\s*(?:Finish\[[\s\S]*?\]|[^\r\n]*))', llm_output)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    # 3.3. 解析并执行行动
    action_match = re.search(r"Action:\s*(.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        finish_match = re.search(r"Finish\[(.*)\]\s*$", action_str, re.DOTALL)
        if not finish_match:
            observation = "错误: Finish 格式不正确。请使用 Finish[最终答案]。"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue
        final_answer = finish_match.group(1).strip()
        print(f"任务完成，最终答案: {final_answer}")
        break

    call_match = re.search(r"(\w+)\s*\((.*?)\)", action_str, re.DOTALL)
    if not call_match:
        observation = "错误: 工具调用格式不正确。请使用 function_name(arg_name=\"arg_value\")。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue

    tool_name = call_match.group(1)
    args_str = call_match.group(2)
    kwargs = dict(re.findall(r"(\w+)\s*=\s*['\"]([^'\"]*)['\"]", args_str))

    print(f"正在调用工具: {tool_name}，参数: {kwargs}")

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
