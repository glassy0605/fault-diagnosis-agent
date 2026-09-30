import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get('DEEPSEEK_API_KEY')  #走环境变量，防止泄露
if not api_key:                          #没读到 key 就报错
    raise SystemExit("❌ 没读到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

fault_schema = {
    "type": "object",
    "properties": {
        "causes": {                       # 故障原因候选
            "type": "array",
            "items": {"type": "string"},
        },
        "steps": {                        # 排查步骤
            "type": "array",
            "items": {"type": "string"},
        },
        "risks": {                        # 风险提示
            "type": "array",
            "items": {"type": "string"},
        },
        "spare_parts": {                  # 推荐备件
            "type": "array",
            "items": {"type": "string"},
        },
        "sources": {                      # 证据来源
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["causes", "steps", "risks", "spare_parts", "sources"],
}

def diagnose(fault_text:str) -> dict:
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": "你是制造业设备故障诊断专家。请严格只输出一个 JSON 对象，不要写解释文字，格式：{\"causes\":[...], \"steps\":[...], \"risks\":[...], \"spare_parts\":[...], \"sources\":[...]}，五个字段都是字符串数组，缺一不可。"
},
            {"role": "user", "content": fault_text},
        ],
        response_format={"type": "json_object"},
        stream=False,
        # reasoning_effort="high",
        # extra_body={"thinking": {"type": "enabled"}}  #思考模式
    )
    return json.loads(response.choices[0].message.content)