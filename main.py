import urllib.request
import random

# لیست منابع خام (می‌تونی بعداً لینک‌های بیشتری به این لیست اضافه کنی)
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_links.txt"
]

def fetch_configs():
    all_links = set() # استفاده از set برای اینکه لینک‌های تکراری خودکار حذف بشن

    for url in SOURCES:
        try:
            # ارسال درخواست برای دریافت محتوای لینک‌ها
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                lines = response.read().decode('utf-8').splitlines()
                for line in lines:
                    line = line.strip()
                    # فقط لینک‌های معتبر رو جدا می‌کنیم
                    if line.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                        all_links.add(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    # تبدیل به لیست و بُر زدن (Shuffle) تا کانفیگ‌های منابع مختلف قاطی بشن
    links_list = list(all_links)
    random.shuffle(links_list)

    # محدود کردن تعداد دقیقاً به ۴۰۰ عدد
    final_links = links_list[:400]

    # ذخیره خروجی در فایل sub.txt
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_links))

    print(f"Successfully saved {len(final_links)} configs to sub.txt")

if __name__ == "__main__":
    fetch_configs()
