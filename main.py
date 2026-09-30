import json
from ds_client import diagnose

fault_text = input("请输入设备故障描述：")
result = diagnose(fault_text)
print("\n===== 诊断结果 =====\n")
print(json.dumps(result, indent=2, ensure_ascii=False))