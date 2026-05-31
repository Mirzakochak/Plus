import urllib.request
import urllib.parse
import random
import base64
import json

# لیست منابع خام
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_links.txt"
]

# 👈 اینجا می‌تونی اسم دلخواهت رو برای کانفیگ‌ها بنویسی
CUSTOM_NAME = "VIP-Config"

def clean_name(link, index):
    """تغییر نام (remark) کانفیگ‌ها به یک نام اختصاصی"""
    new_name = f"{CUSTOM_NAME}-{index}"
    
    # برای vless, trojan, ss که اسمشون بعد از # میاد
    if link.startswith(('vless://', 'trojan://', 'ss://')):
        base_link = link.split('#')[0]
        # انکود کردن اسم جدید برای کارکرد صحیح در URL
        safe_name = urllib.parse.quote(new_name)
        return f"{base_link}#{safe_name}"
        
    # برای vmess که با فرمت base64 و ساختار JSON ذخیره می‌شه
    elif link.startswith('vmess://'):
        try:
            # حذف vmess://
            base64_str = link[8:]
            # اضافه کردن پدینگ برای جلوگیری از خطای دیکود
            base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
            decoded_data = base64.b64decode(base64_str).decode('utf-8')
            config_json = json.loads(decoded_data)
            
            # تغییر کلید ps (که همون اسم/remark کانفیگ هست)
            config_json['ps'] = new_name
            
            # تبدیل مجدد به JSON و بعد Base64
            new_json_str = json.dumps(config_json, ensure_ascii=False).encode('utf-8')
            new_base64 = base64.b64encode(new_json_str).decode('utf-8')
            return f"vmess://{new_base64}"
        except Exception:
            # اگه لینک به هر دلیلی استاندارد نبود، خود لینک اصلی رو برگردون
            return link
            
    return link

def fetch_configs():
    all_links = set()
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                lines = response.read().decode('utf-8').splitlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                        all_links.add(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    links_list = list(all_links)
    random.shuffle(links_list)
    final_links_raw = links_list[:400]
    
    # پردازش و تغییر نام تک‌تک لینک‌ها
    cleaned_links = []
    for i, link in enumerate(final_links_raw, start=1):
        cleaned = clean_name(link, i)
        cleaned_links.append(cleaned)
        
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_links))
        
    print(f"Successfully saved and cleaned {len(cleaned_links)} configs to sub.txt")

if __name__ == "__main__":
    fetch_configs()
