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
    },
    {
    "id": "liu_qiangdong",
    "name": "劉強東",
    "image_path": "images/liu_qiangdong.jpg",
    "category": "企業家",
    "hints": [
        "特徵：臉型偏圓、眼神專注、常以簡潔西裝亮相。",
        "經歷：出身農村，靠自學與家教賺錢，於 SARS 災情中轉型電商。",
        "成就：創立京東集團，打造中國最大自營電商物流系統。",
        "現況：淡出日常管理，主要在海外生活。"
        ]
    },
    {
    "id": "morris_chang",
    "name": "張忠謀",
    "image_path": "images/morris_chang.jpg",
    "category": "企業家",
    "hints": [
        "特徵：白髮、眼神慈和但穩重，經常帶微笑。",
        "經歷：曾任德州儀器副總裁，後受邀回台創立半導體新模式。",
        "成就：建立全球最成功的晶圓代工公司，推動台灣成為半導體中心。",
        "現況：已退休但仍參與國家科技政策與演講。"
        ]
    },
    {
    "id": "stephen_chow",
    "name": "周星馳",
    "image_path": "images/stephen_chow.jpg",
    "category": "演藝名人",
    "hints": [
        "特徵：眼神靈動，表情常帶反諷感，略顯疲倦的眼袋。",
        "經歷：從跑龍套演員逐步成長為香港最成功的影星。",
        "成就：《功夫》《少林足球》突破港片票房紀錄，奠定無厘頭風格。",
        "現況：鮮少露面，持續從事影視投資與劇本開發。"
        ]
    },
    {
        "id": "terry_gou",
        "name": "郭台銘",
        "image_path": "images/terry_gou.jpg",
        "category": "企業家",
        "hints": [
            "特徵：下顎方正、表情嚴肅，穿著偏正式。",
            "經歷：白手起家，早期接下大量 OEM 訂單，打造製造帝國。",
            "成就：創立全球最大電子代工廠（鴻海／富士康）。",
            "現況：持續投資科技與醫療，曾投入政治選舉。"
        ]
    },
    {
        "id": "lin_chiling",
        "name": "林志玲",
        "image_path": "images/lin_chiling.jpg",
        "category": "演藝名人",
        "hints": [
            "特徵：身材高挑、聲音溫柔、笑容親和。",
            "經歷：從模特兒轉為主持與演員，迅速受到亞洲觀眾喜愛。",
            "成就：長年被譽為台灣第一名模，跨足電影與公益活動。",
            "現況：結婚後定居日本，仍偶爾參與公開活動。"
        ]
    },
    {
        "id": "chan_tong_kai",
        "name": "陳同佳",
        "image_path": "images/chan_tong_kai.jpg",
        "category": "罪犯",
        "hints": [
            "特徵：年輕、臉型瘦長、神情常帶不安。",
            "經歷：涉入台北旅館命案後回港，引起兩地法律爭議。",
            "成就：無。",
            "現況：案件與引渡問題持續成為社會討論焦點。"
        ]
    },
    {
        "id": "wang_xin",
        "name": "王欣",
        "image_path": "images/wang_xin.jpg",
        "category": "罪犯",
        "hints": [
            "特徵：髮際線略高、表情沉靜、戴眼鏡。",
            "經歷：快播創辦人，曾在中國科技圈極具影響力。",
            "成就：推出高速影音技術，曾擁數億用戶。",
            "現況：因著作權侵害被判刑後出獄，保持低調。"
        ]
    },
    {
        "id": "cheung_tsz_keung",
        "name": "張子強",
        "image_path": "images/cheung_tsz_keung.jpg",
        "category": "罪犯",
        "hints": [
            "特徵：五官深邃、常帶嚴肅表情、身材壯碩。",
            "經歷：香港著名綁匪，犯下多起高額綁架案。",
            "成就：無。",
            "現況：已被依法判決並處決。"
        ]
    },
    {
        "id": "hsieh_lien_bin",
        "name": "謝連斌",
        "image_path": "images/hsieh_lien_bin.jpg",
        "category": "罪犯",
        "hints": [
            "特徵：中年男子、外型樸實、表情略顯嚴肅。",
            "經歷：涉入食品安全不法案件，在台灣社會引起巨大震動。",
            "成就：無。",
            "現況：案件已判決，相關責任仍受公眾檢視。"
        ]
    },
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