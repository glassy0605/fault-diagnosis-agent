import json
from ds_client import diagnose

phenomenon = input("故障描述：").strip()
# alarm_code = input("报警代码（可留空）：").strip()   # 回车 → "" 空串
result = diagnose(phenomenon)
print("\n===== 诊断结果 =====\n")
print(json.dumps(result, indent=2, ensure_ascii=False)) #indent:调整缩进 ensure_ascii:确保汉字正常显示