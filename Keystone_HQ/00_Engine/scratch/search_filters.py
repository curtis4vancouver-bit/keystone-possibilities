remote_path = "scratch/remote_functions.php"
with open(remote_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("update_page_sovereign")
if idx != -1:
    print(content[idx-100:idx+1500])
else:
    print("update_page_sovereign not found in remote_functions.php")
