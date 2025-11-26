import streamlit as st
import os

# --- 設定頁面 ---
st.set_page_config(page_title="面相訓練器", layout="centered")

# --- CSS樣式優化 (針對深色模式 + 白色按鈕框) ---
st.markdown("""
    <style>
    /* 1. 設定全域文字為白色 (針對深色背景) */
    h1, h2, h3, p, span, div, label {
        color: #ffffff;
    }

    /* 2. 特別指定按鈕樣式 (白色邊框 + 白色文字) */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 20px;
        
        /* 關鍵修改：白色邊框與文字 */
        border: 2px solid #ffffff !important; 
        color: #ffffff !important;
        background-color: transparent !important; /* 背景透明 */
    }

    /* 3. 按鈕滑鼠懸停效果 (變成白底黑字，增加互動感) */
    .stButton > button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
    }
    
    /* 4. 資訊框樣式 (因為是淺灰底，所以字要強制改回黑色) */
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #4e8cff;
    }
    
    /* 強制資訊框內的文字變回黑色，不然會被全域設定蓋過去 */
    .info-box, .info-box p, .info-box span, .info-box div {
        color: #000000 !important;
    }

    .reveal-text {
        font-size: 1.2em;
        font-weight: bold;
        color: #2c3e50 !important; /* 深藍色強調 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 資料設定 (請將照片放在 images 資料夾內) ---
people_data = [
    {
        "id": "ma_yun",
        "name": "馬雲",
        "image_path": "images/jack_ma.jpg",  # 確保檔名與 images 資料夾內一致
        "category": "企業家",
        "hints": [
            "特徵：額頭寬廣但臉型特殊，下巴略縮，眼神銳利。",
            "經歷：高考數學曾考 1 分，英文極佳，早期創業屢次失敗。",
            "成就：創立了世界上最大的電子商務帝國之一。",
            "現況：曾為亞洲首富，後轉趨低調。"
        ]
    },
    {
        "id": "toyz",
        "name": "劉偉健 (Toyz)",
        "image_path": "images/toyz.jpg",
        "category": "網路名人 / 罪犯",
        "hints": [
            "特徵：臥蠶明顯，鼻樑挺直，嘴角微揚（帶桃花/口才）。",
            "經歷：電競選手出身，曾獲得世界冠軍。",
            "轉型：退役後轉型為實況主，以言詞犀利聞名。",
            "爭議：因涉嫌販賣二級毒品被判刑入獄。"
        ]
    }
    # 在此繼續複製貼上格式，加入更多人...
]

# --- 狀態管理 ---
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'step' not in st.session_state: st.session_state.step = 0

def change_person(delta):
    st.session_state.idx = (st.session_state.idx + delta) % len(people_data)
    st.session_state.step = 0

def reveal(): st.session_state.step += 1

# --- 主畫面 ---
person = people_data[st.session_state.idx]

st.title("🧐 面相觀察訓練器")

# 顯示圖片 (自動處理 GitHub 路徑問題)
img_path = person["image_path"]
if os.path.exists(img_path):
    # 如果你想要圖片自動填滿寬度
    st.image(img_path, width="stretch")
else:
    st.error(f"找不到圖片：{img_path}，請檢查檔名是否正確。")

st.markdown("---")

# 按鈕區
c1, c2, c3 = st.columns(3)
if c1.button("⬅️ 上一位"): change_person(-1); st.rerun()
    
total_hints = len(person["hints"])
btn_txt = "🔍 揭露線索" if st.session_state.step <= total_hints else "已顯示全部"
if c2.button(btn_txt, disabled=(st.session_state.step > total_hints)): reveal(); st.rerun()

if c3.button("下一位 ➡️"): change_person(1); st.rerun()

# 資訊區
st.markdown("### 📝 人物資訊")
for i in range(len(person["hints"])):
    if st.session_state.step > i:
        st.markdown(f"<div class='info-box'><span class='reveal-text'>線索 {i+1}：</span>{person['hints'][i]}</div>", unsafe_allow_html=True)

if st.session_state.step > len(person["hints"]):
    st.success(f"🎯 答案：{person['name']}")
    st.info(f"🏷️ 分類：{person['category']}")

st.progress((st.session_state.idx + 1) / len(people_data))
st.caption(f"進度：{st.session_state.idx + 1} / {len(people_data)}")