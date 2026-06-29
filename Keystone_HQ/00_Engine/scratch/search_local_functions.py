local_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\WordPress_Theme_Scaffold\astra-child-keystone\functions.php"
with open(local_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"File size: {len(text)} characters")
print("Contains update_page_sovereign:", "update_page_sovereign" in text)
print("Contains rank_math:", "rank_math" in text)
print("Contains Organization:", "Organization" in text)
