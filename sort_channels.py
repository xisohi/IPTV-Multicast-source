import requests
import re

# 获取原始内容
url = "https://fanmingming.com/txt?url=https://live.fanmingming.com/tv/m3u/ipv6.m3u"
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    content = response.text
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    content = ""

# 定义分类
categories = {
    "央视": [
        "CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV4欧洲", "CCTV4美洲", "CCTV5", "CCTV5+", "CCTV6", "CCTV7",
        "CCTV8", "CCTV9", "CCTV10", "CCTV11", "CCTV12", "CCTV13", "CCTV14", "CCTV15", "CCTV16", "CCTV17",
        "CCTVNews", "CGTN", "CGTN西语", "CGTN法语", "CGTN俄语", "CGTN阿语"
    ],
    "卫视": [
        "安徽卫视", "北京卫视", "重庆卫视", "东方卫视", "东南卫视", "甘肃卫视", "广东卫视", "广西卫视",
        "贵州卫视", "海南卫视", "河北卫视", "河南卫视", "黑龙江卫视", "湖北卫视", "湖南卫视", "吉林卫视",
        "江苏卫视", "江西卫视", "康巴卫视", "辽宁卫视", "内蒙古卫视", "宁夏卫视", "青海卫视", "三沙卫视",
        "厦门卫视", "山东卫视", "山西卫视", "陕西卫视", "深圳卫视", "四川卫视", "天津卫视", "西藏卫视",
        "新疆卫视", "云南卫视", "浙江卫视", "CETV1", "CETV2", "CETV3", "CETV4"
    ],
    "其它": []
}

# 解析内容
if content:
    lines = content.splitlines()
    sorted_content = []

    for category, channels in categories.items():
        sorted_content.append(f"{category},#genre#")
        for channel in channels:
            for line in lines:
                if re.match(f"^{channel},", line):
                    sorted_content.append(line)
                    lines.remove(line)
                    break
        sorted_content.append("")  # 添加空行分隔

    # 将剩余的内容添加到“其它”分类
    sorted_content.append("其它,#genre#")
    sorted_content.extend(lines)

    # 保存到文件
    with open("sorted_channels.m3u", "w") as f:
        f.write("\n".join(sorted_content))
else:
    print("未获取到内容，无法进行排序。")