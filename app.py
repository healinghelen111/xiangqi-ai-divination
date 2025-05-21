import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="象棋卜卦 AI 解盤", page_icon="♟️")
st.title("♟️ 象棋卜卦 AI 解盤系統")

# 棋子資料庫
chess_db = {
    "帥": {"五行": "金", "性格": "領導、掌控", "情緒": "控制慾、壓力大", "身體": "腦、神經系統"},
    "士": {"五行": "金", "性格": "文靜、守護", "情緒": "壓抑、憂鬱", "身體": "肺、大腸"},
    "相": {"五行": "水", "性格": "穩重、慢熱", "情緒": "疑慮、退縮", "身體": "腎、小腸"},
    "車": {"五行": "木", "性格": "執行力強", "情緒": "憤怒、行動衝動", "身體": "肝、筋"},
    "馬": {"五行": "木", "性格": "奔放、機動", "情緒": "焦躁、不穩定", "身體": "四肢、肌肉"},
    "炮": {"五行": "火", "性格": "聰明、變化快", "情緒": "恐懼、波動", "身體": "腎上腺、泌尿"},
    "兵": {"五行": "土", "性格": "踏實、努力", "情緒": "過度思慮", "身體": "脾胃"},
}
# 格局條件分析邏輯
def detect_patterns(pieces):
    c = Counter(pieces)
    patterns = []
    if pieces.count("馬") >= 2:
        if len(set(pieces)) < 5:
            patterns.append("好友格：同色馬馬，朋友助力")
        else:
            patterns.append("破壞格：馬馬異色，爭執與耗損")
    if "馬" in pieces and "炮" in pieces:
        patterns.append("桃花格：馬＋炮偏桃花，有感情糾葛")
    if pieces[1] == pieces[2] == pieces[3]:
        patterns.append("雨傘格：中層三子同色，受保護但易焦慮")
    if set(["車", "馬", "炮"]).issubset(set(pieces)):
        patterns.append("事業格：車馬炮齊聚，事業壓力與變動多")
    if set(["帥", "士", "相"]).issubset(set(pieces)):
        patterns.append("通吃格：三主棋齊聚，控制慾強，需放手")
    return patterns

# 花精推薦邏輯
def flower_essence_recommendation(elements, patterns):
    recs = []
    if elements.get("金", 0) >= 2:
        recs.append("Vine（支配型）／Vervain（理想主控）")
    if elements.get("火", 0) >= 1:
        recs.append("Cherry Plum／Impatiens：平穩情緒與反應")
    if elements.get("土", 0) >= 2:
        recs.append("White Chestnut：清除思緒、助眠")
    if any("焦慮" in p or "雨傘格" in p for p in patterns):
        recs.append("Mimulus：釋放焦慮與不安")
    if any("桃花" in p for p in patterns):
        recs.append("Holly / Chicory：穩定情感、去除佔有")
    return recs
# 問題類型選擇
question_type = st.selectbox("請選擇你的占卜主題：", ["感情", "健康", "事業"])

# 使用者輸入五顆棋子
st.subheader("請選擇五顆棋子（可重複）")
selected_pieces = []
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        piece = st.selectbox(f"第{i+1}顆棋子", list(chess_db.keys()), key=f"piece_{i}")
        selected_pieces.append(piece)

# 按鈕觸發
if st.button("🔍 解卦分析"):
    five_elements = [chess_db[p]["五行"] for p in selected_pieces]
    df_result = pd.DataFrame([{
        "棋子": p,
        "五行": chess_db[p]["五行"],
        "性格": chess_db[p]["性格"],
        "情緒": chess_db[p]["情緒"],
        "身體": chess_db[p]["身體"]
    } for p in selected_pieces])

    st.subheader("🔎 解卦分析報告：")
    st.dataframe(df_result, use_container_width=True)

    # 五行統計
    counts = pd.Series(five_elements).value_counts().to_dict()
    st.write("### 五行分佈：")
    st.json(counts)

    # 解釋建議
    suggestion = ""
    if question_type == "健康":
        if counts.get("木", 0) >= 2:
            suggestion += "木過旺，注意肝氣鬱結與壓力性行動；\\n"
        if counts.get("土", 0) >= 2:
            suggestion += "土重，易思慮過多，脾胃功能需保養；\\n"
    elif question_type == "感情":
        if "水" not in counts:
            suggestion += "缺水，情感交流與信任易出現問題；\\n"
        if counts.get("木", 0) >= 2:
            suggestion += "木旺，情感積極但變化快速，需穩定心性；\\n"
    elif question_type == "事業":
        if counts.get("金", 0) >= 2:
            suggestion += "金旺，適合規劃、領導型職業；\\n"
        if counts.get("火", 0) >= 1:
            suggestion += "火出現，適合創業與主動發展。\\n"

    st.write("### 🌱 建議解析：")
    st.info(suggestion if suggestion else "五行均衡，目前無明顯偏重。")

    # 格局分析
    patterns = detect_patterns(selected_pieces)
    st.write("### 🧩 格局分析：")
    st.success("\\n".join(patterns) if patterns else "未觸發明顯格局")

    # 花精建議
    flowers = flower_essence_recommendation(counts, patterns)
    st.write("### 🌸 花精建議：")
    st.warning("、".join(flowers) if flowers else "目前無特別推薦花精，建議維持情緒穩定。")
