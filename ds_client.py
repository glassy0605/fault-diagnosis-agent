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

def diagnose(phenomenon:str) -> dict:
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": """
【角色】你是制造业设备故障诊断专家。
【任务】用户会用一句口语描述设备故障，请把它翻译成结构化 JSON，
并给出诊断结论。信息不足时不要编造。
【字段】
一、故障信息
- 设备：字符串。用户口中设备本身的称呼，不含部位；未提到填空字符串。
- 故障现象：字符串。把口语描述规范化成完整、可检索的故障描述，保留工况与关键细节，不含时长。
- 故障部位：字符串。发生故障的部件或系统（如主轴、刀库、液压系统）；无法判断填空字符串。
- 持续时长：字符串。故障已持续的时间，原样保留（如"约30分钟""两天"）；未提到填空字符串。

二、诊断结论
- 可能原因：字符串数组。按可能性从高到低列出原因候选，每条为一句完整描述；无法判断时填空数组。
- 诊断结论：字符串。用一句话概括最可能的故障判断，供现场快速阅读。
- 排查步骤：字符串数组。按执行顺序排列的排查动作，每步以动词开头、可独立执行。

三、风险与处置
- 风险提示：字符串数组。维修过程中的安全风险、二次损坏风险、生产损失风险；无明显风险时填空数组。
- 推荐备件：字符串数组。可能需要更换或准备的备件名称；无需备件时填空数组。

四、溯源与缺口
- 证据来源：字符串数组。判断所依据的手册、标准或规程名称；无明确来源时填空数组。
- 推断报警码：字符串数组。根据现象推断可能对应的报警代码；该故障通常无码时填空数组。
- 待补充信息：字符串数组。信息不足以定性时，列出还需采集什么；信息充分时填空数组。
【禁令】
- 只输出 JSON 对象，不要任何解释文字、不要 markdown 代码块标记
- 只输出上述字段，不得增加、改名
"""
},
            {"role": "user", "content": phenomenon},
        ],
        response_format={"type": "json_object"},
        stream=False,
        # reasoning_effort="high",
        # extra_body={"thinking": {"type": "enabled"}}  #思考模式
    )
    return json.loads(response.choices[0].message.content)