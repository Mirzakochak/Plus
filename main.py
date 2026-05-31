import urllib.request
import urllib.parse
import random
import base64
import json

# بهترین سورس‌های تست‌شده (مخلوطی از خام و Base64)
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub2.txt",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/mix",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity"
]

def clean_name(link, index):
    new_name = f"⚡ Mirzakochak ⚡ | {index}"
    
    if link.startswith('vless://'):
        base_link = link.split('#')[0]
        safe_name = urllib.parse.quote(new_name)
        return f"{base_link}#{safe_name}"
        
    elif link.startswith('vmess://'):
        try:
            base64_str = link[8:]
            base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
            decoded_data = base64.b64decode(base64_str).decode('utf-8')
            config_json = json.loads(decoded_data)
            
            config_json['ps'] = new_name
            
            new_json_str = json.dumps(config_json, ensure_ascii=False).encode('utf-8')
            new_base64 = base64.b64encode(new_json_str).decode('utf-8')
            return f"vmess://{new_base64}"
        except Exception:
            return link
            
    return link

def decode_content(text):
    """تشخیص هوشمند و باز کردن فایل‌های Base64"""
    if "vless://" in text or "vmess://" in text:
        return text.splitlines()
    try:
        # اگر متن Base64 باشد آن را دیکود می‌کند
        padded = text.strip() + "=" * ((4 - len(text.strip()) % 4) % 4)
        decoded = base64.b64decode(padded).decode('utf-8')
        return decoded.splitlines()
    except:
        return text.splitlines()

def fetch_configs():
    all_links = set()
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8')
                lines = decode_content(content)
                
                for line in lines:
                    line = line.strip()
                    if line.startswith(('vless://', 'vmess://')):
                        all_links.add(line)
            print(f"Success: Fetched from {url}")
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    links_list = list(all_links)
    random.shuffle(links_list)
    
    final_links_raw = links_list[:250]
    
    cleaned_links = []
    for i, link in enumerate(final_links_raw, start=1):
        cleaned = clean_name(link, i)
        cleaned_links.append(cleaned)
        
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_links))
        
    print(f"✅ Successfully saved {len(cleaned_links)} configs to sub.txt")

if __name__ == "__main__":
    fetch_configs()
