import requests
import re

# --- 从 moban.txt 提取自定义分类 ---
def load_categories_from_moban():
    categories = {}
    current_category = None
    try:
        with open("moban.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 检测分类行 (例如 "央视,#genre#")
                if ",#genre#" in line:
                    current_category = line.split(",")[0]  # 提取分类名称
                    categories[current_category] = []
                elif current_category:
                    # 清理频道名后的逗号，并添加到当前分类
                    channel = line.split(",")[0].strip()
                    if channel:
                        categories[current_category].append(channel)
    except FileNotFoundError:
        print("错误：未找到 moban.txt 文件")
    return categories

# --- 主逻辑 ---
url = "https://fanmingming.com/txt?url=https://live.fanmingming.com/tv/m3u/ipv6.m3u"
try:
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    content = ""

# 加载分类数据
categories = load_categories_from_moban()
if not categories:
    print("分类数据为空，请检查 moban.txt 格式")
    exit()

if content:
    lines = content.splitlines()
    sorted_content = []
    filtered_lines = [line for line in lines if "#genre#" not in line]

    # 按 moban.txt 中的顺序处理分类
    for category in categories:
        sorted_content.append(f"{category},#genre#")
        for channel in categories[category]:
            for line in filtered_lines.copy():  # 使用副本避免迭代修改问题
                # 匹配频道名称（允许频道名后有逗号或其他参数）
                if re.match(f"^{re.escape(channel)},", line):
                    sorted_content.append(line)
                    filtered_lines.remove(line)
        sorted_content.append("")

    # 剩余内容归入"其它"
    sorted_content.append("其它,#genre#")
    sorted_content.extend(filtered_lines)

    # 保存文件
    with open("live.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted_content))
else:
    print("未获取到内容，无法进行排序。")