from ds_client import diagnose

fault_text = input("请输入设备故障描述：")
print("\n===== 诊断结果 =====\n")
print(diagnose(fault_text))