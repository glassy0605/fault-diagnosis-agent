import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get('DEEPSEEK_API_KEY')
if not api_key:                          #没读到 key 就报错
    raise SystemExit("❌ 没读到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

def diagnose(fault_text:str) -> str:
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": "你是制造业设备故障诊断专家"},
            {"role": "user", "content": fault_text},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    return response.choices[0].message.content