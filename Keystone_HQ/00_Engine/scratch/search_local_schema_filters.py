local_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\WordPress_Theme_Scaffold\astra-child-keystone\functions.php"
with open(local_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("rank_math/json_ld")
if idx != -1:
    start = max(0, idx - 100)
    end = min(len(text), idx + 2500)
    print(text[start:end])
else:
    print("Filter not found")
