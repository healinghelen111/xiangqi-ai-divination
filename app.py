import streamlit as st
import pandas as pd
import random
from collections import Counter

st.set_page_config(page_title="象棋卜卦 AI 解盤", page_icon="♟️")
st.title("♟️ 象棋卜卦 AI 占卜系統（隨機抽卦）")

# 建立32顆象棋資料（紅黑各16）
chess_pool = ["紅帥"] + ["紅士"]*2 + ["紅相"]*2 + ["紅車"]*2 + ["紅馬"]*2 + ["紅炮"]*2 + ["紅兵"]*5 + \
             ["黑將"] + ["黑士"]*2 + ["黑象"]*2 + ["黑俥"]*2 + ["黑傌"]*2 + ["黑包"]*2 + ["黑卒"]*5

# 棋子五行與情緒對應
chess_db = {
    "帥": {"五行": "金", "性格": "領導、掌控", "情緒": "控制慾、壓力大", "身體": "腦、神經系統"},
    "將": {"五行": "金", "性格": "領導、掌控", "情緒": "控制慾、壓力大", "身體": "腦、神經系統"},
    "士": {"五行": "金", "性格": "文靜、守護", "情緒": "壓抑、憂鬱", "身體": "肺、大腸"},
    "仕": {"五行": "金", "性格": "文靜、守護", "情緒": "壓抑、憂鬱", "身體": "肺、大腸"},
    "相": {"五行": "水", "性格": "穩重、慢熱", "情緒": "疑慮、退縮", "身體": "腎、小腸"},
    "象": {"五行": "水", "性格": "穩重、慢熱", "情緒": "疑慮、退縮", "身體": "腎、小腸"},
    "車": {"五行": "木", "性格": "執行力強", "情緒": "憤怒、行動衝動", "身體": "肝、筋"},
    "俥": {"五行": "木", "性格": "執行力強", "情緒": "憤怒、行動衝動", "身體": "肝、筋"},
    "馬": {"五行": "木", "性格": "奔放、機動", "情緒": "焦躁、不穩定", "身體": "四肢、肌肉"},
    "傌": {"五行": "木", "性格": "奔放、機動", "情緒": "焦躁、不穩定", "身體": "四肢、肌肉"},
    "炮": {"五行": "火", "性格": "聰明、變化快", "情緒": "恐懼、波動", "身體": "腎上腺、泌尿"},
    "包": {"五行": "火", "性格": "聰明、變化快", "情緒": "恐懼、波動", "身體": "腎上腺、泌尿"},
    "兵": {"五行": "土", "性格": "踏實、努力", "情緒": "過度思慮", "身體": "脾胃"},
    "卒": {"五行": "土", "性格": "踏實、努力", "情緒": "過度思慮", "身體": "脾胃"},
}

positions = ["中（1）", "左（2）", "右（3）", "上（4）", "下（5）"]

# 格局條件分析
def detect_patterns(pieces):
    names = [p[1:] for p in pieces]
    patterns = []
    if names.count("馬") + names.count("傌") >= 2:
        patterns.append("好友格：雙馬，朋友助力或衝突")
    if "馬" in names and ("炮" in names or "包" in names):
        patterns.append("桃花格：馬＋炮，感情變化多")
    if names[1] == names[2] == names[3]:
        patterns.append("雨傘格：中層同色保護力但壓力大")
    if len(set(names).intersection(["車", "馬", "炮", "俥", "傌", "包"])) >= 3:
        patterns.append("事業格：行動棋多，壓力與挑戰並存")
    return patterns

# 花精推薦
def flower_essence_recommendation(elements, patterns):
    recs = []
    if elements.get("金", 0) >= 2:
        recs.append("Vervain / Vine：控制與壓力型情緒")
    if elements.get("火", 0) >= 1:
        recs.append("Cherry Plum / Impatiens：穩定焦躁與情緒")
    if elements.get("土", 0) >= 2:
        recs.append("White Chestnut：清除思緒與睡眠壓力")
    if any("焦慮" in p or "雨傘格" in p for p in patterns):
        recs.append("Mimulus：釋放焦慮與內在壓力")
    if any("桃花" in p for p in patterns):
        recs.append("Holly / Chicory：釐清感情糾結與佔有")
    return recs

# 抽卦按鈕
if st.button("🔮 抽卦（從32顆象棋隨機抽5顆）"):
    draw = random.sample(chess_pool, 5)
    elements = []
    rows = []
    for i, piece in enumerate(draw):
        color = piece[0]
        name = piece[1:]
        pos = positions[i]
        data = chess_db.get(name, {})
        elements.append(data.get("五行", ""))
        rows.append({
            "位置": pos,
            "棋子": piece,
            "五行": data.get("五行"),
            "性格": data.get("性格"),
            "情緒": data.get("情緒"),
            "身體": data.get("身體")
        })

    df_result = pd.DataFrame(rows)
    st.subheader("🧩 占卜結果：")
    st.dataframe(df_result, use_container_width=True)

    # 五行分析
    counts = pd.Series(elements).value_counts().to_dict()
    st.write("### 五行分佈：")
    st.json(counts)

    # 格局分析
    patterns = detect_patterns(draw)
    st.write("### 格局分析：")
    st.success("\\n".join(patterns) if patterns else "未觸發明顯格局")

    # 花精建議
    flowers = flower_essence_recommendation(counts, patterns)
    st.write("### 🌸 花精建議：")
    st.warning("、".join(flowers) if flowers else "目前無特別花精建議，可持續觀察情緒變化")
