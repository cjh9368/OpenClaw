#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简牍 - 八字排盘与五行分析器
"""

from datetime import datetime, timedelta

# 天干地支表
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 地支藏干
DIZHI_CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

# 天干五行
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 季节五行旺衰（月令）
SEASON_WUXING = {
    # 春季（寅卯辰月）
    "寅": {"旺": "木", "相": "火", "休": "水", "囚": "金", "死": "土"},
    "卯": {"旺": "木", "相": "火", "休": "水", "囚": "金", "死": "土"},
    "辰": {"旺": "土", "相": "金", "休": "火", "囚": "木", "死": "水"},
    # 夏季（巳午未月）
    "巳": {"旺": "火", "相": "土", "休": "木", "囚": "水", "死": "金"},
    "午": {"旺": "火", "相": "土", "休": "木", "囚": "水", "死": "金"},
    "未": {"旺": "土", "相": "金", "休": "火", "囚": "木", "死": "水"},
    # 秋季（申酉戌月）
    "申": {"旺": "金", "相": "水", "休": "土", "囚": "火", "死": "木"},
    "酉": {"旺": "金", "相": "水", "休": "土", "囚": "火", "死": "木"},
    "戌": {"旺": "土", "相": "金", "休": "火", "囚": "木", "死": "水"},
    # 冬季（亥子丑月）
    "亥": {"旺": "水", "相": "木", "休": "金", "囚": "土", "死": "火"},
    "子": {"旺": "水", "相": "木", "休": "金", "囚": "土", "死": "火"},
    "丑": {"旺": "土", "相": "金", "休": "火", "囚": "木", "死": "水"},
}

# 五行生克关系
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}


def get_ganzhi_year(year):
    """获取年柱天干地支"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]


def get_jieqi_year(year):
    """
    获取该年的立春时间（近似值，精确到日）
    立春一般在2月3日-5日之间
    """
    # 简化处理：使用2月4日作为立春
    return datetime(year, 2, 4)


def get_ganzhi_month(year, month, day):
    """
    获取月柱天干地支
    注意：八字月柱以节气为界，不是农历月份
    """
    # 节气分界（近似日期）
    jieqi_dates = [
        (2, 4),   # 立春 - 寅月
        (3, 6),   # 惊蛰 - 卯月
        (4, 5),   # 清明 - 辰月
        (5, 6),   # 立夏 - 巳月
        (6, 6),   # 芒种 - 午月
        (7, 7),   # 小暑 - 未月
        (8, 8),   # 立秋 - 申月
        (9, 8),   # 白露 - 酉月
        (10, 8),  # 寒露 - 戌月
        (11, 7),  # 立冬 - 亥月
        (12, 7),  # 大雪 - 子月
        (1, 6),   # 小寒 - 丑月（次年）
    ]
    
    # 确定当前在哪个月份区间
    current_date = (month, day)
    month_zhi_idx = 0
    
    for i, (jm, jd) in enumerate(jieqi_dates):
        if current_date < (jm, jd):
            month_zhi_idx = i - 1
            break
    else:
        month_zhi_idx = 11  # 丑月
    
    if month_zhi_idx < 0:
        month_zhi_idx = 11
    
    # 年干决定月干起始
    year_gan_idx = (year - 4) % 10
    
    # 年上起月法：甲己之年丙作首，乙庚之岁戊为头...
    month_gan_start = {
        0: 2,  # 甲年 -> 丙寅
        5: 2,  # 己年 -> 丙寅
        1: 4,  # 乙年 -> 戊寅
        6: 4,  # 庚年 -> 戊寅
        2: 6,  # 丙年 -> 庚寅
        7: 6,  # 辛年 -> 庚寅
        3: 8,  # 丁年 -> 壬寅
        8: 8,  # 壬年 -> 壬寅
        4: 0,  # 戊年 -> 甲寅
        9: 0,  # 癸年 -> 甲寅
    }
    
    start_gan = month_gan_start.get(year_gan_idx, 0)
    gan_idx = (start_gan + month_zhi_idx) % 10
    
    return TIANGAN[gan_idx] + DIZHI[month_zhi_idx]


def get_ganzhi_day(year, month, day):
    """获取日柱天干地支"""
    # 使用蔡勒公式或已知基准日推算
    # 1900年1月31日为甲子日
    base_date = datetime(1900, 1, 31)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    gan_idx = days_diff % 10
    zhi_idx = days_diff % 12
    
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]


def get_ganzhi_hour(day_gan, hour):
    """
    获取时柱天干地支
    日上起时法：甲己还加甲，乙庚丙作初...
    """
    # 时辰对应（23-1点子时，1-3点丑时...）
    zhi_idx = ((hour + 1) // 2) % 12
    
    # 日干决定时干起始
    day_gan_idx = TIANGAN.index(day_gan)
    
    hour_gan_start = {
        0: 0,  # 甲日 -> 甲子
        5: 0,  # 己日 -> 甲子
        1: 2,  # 乙日 -> 丙子
        6: 2,  # 庚日 -> 丙子
        2: 4,  # 丙日 -> 戊子
        7: 4,  # 辛日 -> 戊子
        3: 6,  # 丁日 -> 庚子
        8: 6,  # 壬日 -> 庚子
        4: 8,  # 戊日 -> 壬子
        9: 8,  # 癸日 -> 壬子
    }
    
    start_gan = hour_gan_start.get(day_gan_idx, 0)
    gan_idx = (start_gan + zhi_idx) % 10
    
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]


def calculate_bazi(year, month, day, hour, minute=0):
    """计算完整八字"""
    year_gz = get_ganzhi_year(year)
    month_gz = get_ganzhi_month(year, month, day)
    day_gz = get_ganzhi_day(year, month, day)
    hour_gz = get_ganzhi_hour(day_gz[0], hour)
    
    return {
        "年柱": year_gz,
        "月柱": month_gz,
        "日柱": day_gz,
        "时柱": hour_gz
    }


def analyze_wuxing(bazi):
    """分析五行分布"""
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    details = []
    
    for pillar_name, gz in bazi.items():
        tg = gz[0]  # 天干
        dz = gz[1]  # 地支
        
        tg_wx = TIANGAN_WUXING[tg]
        dz_wx = DIZHI_WUXING[dz]
        
        wuxing_count[tg_wx] += 1
        wuxing_count[dz_wx] += 0.5  # 地支本气权重稍低
        
        # 地支藏干
        canggan = DIZHI_CANGGAN[dz]
        for cg in canggan:
            cg_wx = TIANGAN_WUXING[cg]
            wuxing_count[cg_wx] += 0.3  # 藏干权重更低
        
        details.append({
            "柱": pillar_name,
            "干支": gz,
            "天干五行": tg_wx,
            "地支五行": dz_wx,
            "藏干": canggan
        })
    
    return wuxing_count, details


def determine_xiyongshen(bazi, wuxing_count, month_zhi):
    """判定喜用神和忌神"""
    # 获取日主
    day_master = bazi["日柱"][0]
    day_master_wx = TIANGAN_WUXING[day_master]
    
    # 获取月令五行状态
    season_status = SEASON_WUXING.get(month_zhi, {})
    
    # 分析日主强弱
    day_master_strength = wuxing_count[day_master_wx]
    sheng_wo = WUXING_SHENG.get(day_master_wx, "")  # 生我者
    wo_sheng = None
    for k, v in WUXING_SHENG.items():
        if v == day_master_wx:
            wo_sheng = k
            break
    
    # 判断身强身弱
    is_strong = day_master_strength >= 2.5
    
    # 根据身强身弱定喜用神
    if is_strong:
        # 身强：喜克泄耗（官杀、食伤、财星）
        xiyong = [
            WUXING_KE.get(day_master_wx, ""),  # 官杀（克我者）
            wo_sheng  # 食伤（我生者）
        ]
        jishen = [sheng_wo]  # 印星（生我者）
    else:
        # 身弱：喜生扶（印星、比劫）
        xiyong = [sheng_wo, day_master_wx]  # 印星、比劫
        jishen = [WUXING_KE.get(day_master_wx, "")]  # 官杀
    
    return {
        "日主": day_master,
        "日主五行": day_master_wx,
        "身强身弱": "身强" if is_strong else "身弱",
        "喜用神": [x for x in xiyong if x],
        "忌神": [x for x in jishen if x]
    }


def get_yongzi_shuxing(xiyongshen_result):
    """根据喜用神生成宜用字属性"""
    xiyong = xiyongshen_result["喜用神"]
    jishen = xiyongshen_result["忌神"]
    
    # 五行对应的偏旁/字根提示
    wuxing_pianpang = {
        "金": "钅、金、刀、戈、玉、石、贝、西、白、辛等偏旁，或五行属金的字",
        "木": "木、艹、竹、禾、米、糸、纟、衣、巾等偏旁，或五行属木的字",
        "水": "氵、水、冫、雨、子、亥、黑、玄等偏旁，或五行属水的字",
        "火": "火、灬、日、光、赤、心、忄、丙、丁等偏旁，或五行属火的字",
        "土": "土、山、田、石、阜、阝、辰、戌、丑、未等偏旁，或五行属土的字"
    }
    
    yiyong_list = []
    for wx in xiyong:
        yiyong_list.append(f"【{wx}】{wuxing_pianpang.get(wx, '')}")
    
    jinji_list = []
    for wx in jishen:
        jinji_list.append(f"【{wx}】{wuxing_pianpang.get(wx, '')}")
    
    return {
        "宜用五行": xiyong,
        "宜用字特征": yiyong_list,
        "禁忌五行": jishen,
        "禁忌字特征": jinji_list
    }


def generate_report(year, month, day, hour, minute=0, location=""):
    """生成完整的命理分析报告"""
    # 计算八字
    bazi = calculate_bazi(year, month, day, hour, minute)
    
    # 分析五行
    wuxing_count, details = analyze_wuxing(bazi)
    
    # 获取月令
    month_zhi = bazi["月柱"][1]
    
    # 判定喜用神
    xiyongshen = determine_xiyongshen(bazi, wuxing_count, month_zhi)
    
    # 生成用字建议
    yongzi = get_yongzi_shuxing(xiyongshen)
    
    # 构建报告
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 简牍 · 八字命理分析报告                  ║
╚══════════════════════════════════════════════════════════════╝

【基本信息】
出生时间：{year}年{month}月{day}日 {hour}:{minute:02d}
出生地点：{location}

【八字排盘】
┌─────────┬─────────┬─────────┬─────────┐
│   年柱   │   月柱   │   日柱   │   时柱   │
├─────────┼─────────┼─────────┼─────────┤
│  {bazi['年柱']}      │  {bazi['月柱']}      │  {bazi['日柱']}      │  {bazi['时柱']}      │
│ ({TIANGAN_WUXING[bazi['年柱'][0]]}{DIZHI_WUXING[bazi['年柱'][1]]})    │ ({TIANGAN_WUXING[bazi['月柱'][0]]}{DIZHI_WUXING[bazi['月柱'][1]]})    │ ({TIANGAN_WUXING[bazi['日柱'][0]]}{DIZHI_WUXING[bazi['日柱'][1]]})    │ ({TIANGAN_WUXING[bazi['时柱'][0]]}{DIZHI_WUXING[bazi['时柱'][1]]})    │
└─────────┴─────────┴─────────┴─────────┘

【五行盈缺分析】
"""
    
    # 五行统计
    total = sum(wuxing_count.values())
    for wx in ["金", "木", "水", "火", "土"]:
        count = wuxing_count[wx]
        percentage = (count / total * 100) if total > 0 else 0
        bar = "█" * int(percentage / 5)
        status = ""
        if percentage > 25:
            status = "【旺】"
        elif percentage < 10:
            status = "【缺】"
        report += f"  {wx}: {bar:<20} {count:.1f}分 {percentage:.1f}% {status}\n"
    
    # 找出最旺和最缺的
    max_wx = max(wuxing_count, key=wuxing_count.get)
    min_wx = min(wuxing_count, key=wuxing_count.get)
    
    report += f"\n  五行总评：{max_wx}旺"
    if wuxing_count[min_wx] < 1:
        report += f"缺{min_wx}"
    report += "\n"
    
    report += f"""
【日主分析】
日主：{xiyongshen['日主']}（{xiyongshen['日主五行']}命）
状态：{xiyongshen['身强身弱']}

【喜用神 & 忌神】
✨ 喜用神（补益命局）：{'、'.join(xiyongshen['喜用神'])}
⚠️  忌神（应当避免）：{'、'.join(xiyongshen['忌神'])}

【宜用字属性】
"""
    
    for item in yongzi['宜用字特征']:
        report += f"  ✅ {item}\n"
    
    report += "\n【禁忌清单 - 供下游Agent过滤】\n"
    report += f"  ❌ 禁用五行：{'、'.join(yongzi['禁忌五行'])}\n"
    for item in yongzi['禁忌字特征']:
        report += f"     - {item}\n"
    
    report += """
╔══════════════════════════════════════════════════════════════╗
║  注：以上分析基于传统命理学理论，仅供参考。                    ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    return report


if __name__ == "__main__":
    # 测试：2026年3月2日9:31 杭州钱塘区
    report = generate_report(2026, 3, 2, 9, 31, "杭州市钱塘区")
    print(report)
