import streamlit as st
from datetime import date

from database import (
    init_db,
    add_dream,
    get_all_dreams,
    update_dream,
    delete_dream
)

from rag_analysis import generate_jungian_reflection
def apply_custom_theme():

    st.markdown("""
    <style>

    /* =====================================================
       1. 整體背景：白色 → 淡紫色 → 淡藍色漸層
    ===================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #FFFFFF 0%,
                #DDD6FE 50%,
                #BAE6FD 100%
            );

        background-attachment: fixed;
        color: #1F2937;
    }


    /* =====================================================
       2. 移除 Streamlit 上方突兀白色 Header
    ===================================================== */

    header[data-testid="stHeader"] {
        background: rgba(196, 181, 253, 0.38);!important;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);

        border-bottom: 1px solid rgba(255,255,255,0.06);
    }


    /* =====================================================
       3. 主內容寬度
    ===================================================== */

    .block-container {
        # max-width: 1250px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       4. Hero
    ===================================================== */

    .hero-box {

        padding: 2.3rem 0rem;

        margin-bottom: 1.8rem;


        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }


    .hero-title {

        font-size: 2.8rem;

        font-weight: 800;

        letter-spacing: 0.3px;

        margin-bottom: 1rem;
        margin-top: 3rem;

        background:
            linear-gradient(
                30deg,
                #7f809e,
                #DDD6FE,
                #bde8ff
            );
        color: #1F2937;

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {

        color: #7f809e;

        font-size: 1.05rem;

        line-height: 1.8;
    }



    /* =====================================================
       5. Tabs：柔和玻璃底座與圓角膠囊
    ===================================================== */

    .stTabs [role="tablist"] {
        display: flex;
        gap: 10px;
        padding: 10px;
        margin: 12px 0 24px;
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 30px;
        box-shadow: 0 8px 24px rgba(83, 67, 140, 0.08);
        backdrop-filter: blur(14px);
        overflow-x: auto;
    }

    .stTabs [role="tab"] {
        flex: 1 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 52px;
        height: auto;
        padding: 14px 28px !important;
        border: 1px solid transparent !important;
        border-radius: 999px !important;
        background: transparent !important;
        color: #514768 !important;
        font-weight: 600;
        white-space: nowrap;
        transition: background 180ms ease, color 180ms ease,
                    box-shadow 180ms ease;
    }

    .stTabs [role="tab"]:hover,
    .stTabs [role="tab"][data-hovered] {
        background: #7863B5 !important;
        color: #FFFFFF !important;
    }

    .stTabs [role="tab"][aria-selected="true"],
    .stTabs [role="tab"][data-selected] {
        background: linear-gradient(120deg, #7355B5, #516BAC) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(99, 76, 161, 0.22);
    }

    .stTabs [role="tab"] p,
    .stTabs [role="tab"] span {
        color: inherit !important;
    }

    .stTabs [role="tab"]:focus-visible {
        outline: 2px solid #6350A0 !important;
        outline-offset: 2px;
    }

    /* 隱藏新舊版 Streamlit 的選取底線 */
    .stTabs .react-aria-SelectionIndicator,
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    .stTabs [role="tab"]::before,
    .stTabs [role="tab"]::after {
        display: none !important;
    }

    @media (max-width: 640px) {
        .stTabs [role="tablist"] {
            gap: 6px;
            padding: 8px;
        }

        .stTabs [role="tab"] {
            padding: 12px 20px !important;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .stTabs [role="tab"] {
            transition: none;
        }
    }

    /* =====================================================
       8. Expander - 夢境卡片
    ===================================================== */

    [data-testid="stExpander"] {

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.045),
                rgba(139,92,246,0.025)
            );

        border:
            1px solid rgba(167,139,250,0.14);

        border-radius: 20px;

        overflow: hidden;

        margin-bottom: 14px;

        box-shadow:
            0 10px 35px rgba(0,0,0,0.18);

        transition: all 0.2s ease;
    }


    [data-testid="stExpander"]:hover {

        border-color:
            rgba(167,139,250,0.30);

        box-shadow:
            0 12px 40px rgba(99,102,241,0.10);
    }



    /* =====================================================
       9. Form
    ===================================================== */

    [data-testid="stForm"] {

        background:
            rgba(255,255,255,0.025);

        border:
            1px solid rgba(167,139,250,0.12);

        border-radius: 20px;

        padding: 1.2rem;
    }



    /* =====================================================
       10. Metric cards
    ===================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.09),
                rgba(168,85,247,0.055)
            );

        border:
            1px solid rgba(167,139,250,0.14);

        border-radius: 20px;

        padding: 1.2rem 1.4rem;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.15);
    }



    /* =====================================================
       11. Input
    ===================================================== */

    .stTextArea textarea,
    .stTextInput input {

        background:
            rgba(255,255,255,0.045) !important;

        color:
            #F7F7FF !important;

        border:
            1px solid rgba(167,139,250,0.16) !important;

        border-radius:
            14px !important;
    }


    .stTextArea textarea:focus,
    .stTextInput input:focus {

        border-color:
            rgba(167,139,250,0.55) !important;

        box-shadow:
            0 0 0 2px rgba(139,92,246,0.08) !important;
    }



    /* =====================================================
       12. Button
    ===================================================== */

    .stButton button,
    .stFormSubmitButton button {

        background:
            linear-gradient(
                135deg,
                #6366F1,
                #8B5CF6,
                #A855F7
            );

        color:
            #FFFFFF !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        border-radius:
            24px !important;

        padding: 0.75rem 1.75rem !important;
        min-height: 3rem;

        font-weight:
            650 !important;

        box-shadow:
            0 8px 24px rgba(99,102,241,0.22);

        transition:
            all 0.22s ease;
    }


    .stButton button:hover,
    .stFormSubmitButton button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 12px 28px rgba(139,92,246,0.30);

        filter:
            brightness(1.08);
    }



    /* =====================================================
       13. Divider
    ===================================================== */

    hr {

        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(167,139,250,0.20),
                transparent
            );

        margin:
            1.5rem 0;
    }



    /* =====================================================
       14. Caption
    ===================================================== */

    .stCaption {

        color:
            #9198C4 !important;
    }



    /* =====================================================
       15. Scrollbar
    ===================================================== */

    ::-webkit-scrollbar {

        width: 8px;
    }


    ::-webkit-scrollbar-track {

        background:
            #070B18;
    }


    ::-webkit-scrollbar-thumb {

        background:
            linear-gradient(
                #6366F1,
                #A855F7
            );

        border-radius:
            20px;
    }

    </style>
    """, unsafe_allow_html=True)

# -------------------------
# 頁面設定
# -------------------------
st.set_page_config(
    page_title="DreamMap",
    page_icon="🌙",
    layout="wide"
)


# -------------------------
# 初始化資料庫
# -------------------------
init_db()


# -------------------------
# Header
# -------------------------
apply_custom_theme()

st.markdown("""
<div class="hero-box">
    <div class="hero-title">🌙 DreamMap</div>
    <div class="hero-subtitle">
        記錄夢境，探索潛意識的宇宙。<br>
        在星夜與神秘感之中，保存夢、閱讀夢、理解夢。
    </div>
</div>
""", unsafe_allow_html=True)



# -------------------------
# 建立分頁
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "✏️ 記錄夢境",
        "📖 夢境日記",
        "🔍 AI 搜尋",
        "✨ 夢境地圖"
    ]
)


# ==================================================
# Tab 1：記錄夢境
# ==================================================
with tab1:

    st.subheader("✨ 記錄一個夢")

    with st.form("dream_form"):

        dream_date = st.date_input(
            "夢境日期",
            value=date.today()
        )

        dream = st.text_area(
            "今晚想記下什麼夢？",
            placeholder="例如：我夢到自己回到學校，走廊沒有盡頭，怎麼樣都找不到教室……",
            height=220
        )

        mood = st.selectbox(
            "這個夢帶給你的感受",
            [
                "😄 開心",
                "🙂 平靜",
                "😐 普通",
                "😟 焦慮",
                "😢 難過",
                "😨 害怕",
                "😠 憤怒"
            ]
        )

        submitted = st.form_submit_button(
            "🌙 儲存夢境",
            use_container_width=True
        )

        if submitted:

            if dream.strip():

                add_dream(
                    str(dream_date),
                    dream.strip(),
                    mood
                )

                st.success("🌙 夢境已經保存到 DreamMap！")

            else:

                st.warning("請先寫下一點夢境內容。")


# ==================================================
# Tab 2：夢境日記
# ==================================================
with tab2:

    st.subheader("📖 我的夢境日記")

    dreams = get_all_dreams()

    if len(dreams) == 0:

        st.info("目前還沒有夢境紀錄。")

    else:

        # -------------------------
        # 統計資訊
        # -------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🌙 已記錄夢境",
                len(dreams)
            )

        with col2:
            latest_date = dreams[0][1]

            st.metric(
                "✨ 最近一次夢境",
                latest_date
            )

        st.divider()

        # -------------------------
        # 每一筆夢境
        # -------------------------
        for dream_item in dreams:

            dream_id = dream_item[0]
            dream_date_value = dream_item[1]
            content = dream_item[2]
            mood = dream_item[3]

            with st.expander(
                f"🌙 {dream_date_value}｜{mood}"
            ):

                # =========================
                # 顯示夢境內容
                # =========================
                st.markdown("#### 夢境內容")
                st.write(content)

                st.caption(
                    f"Dream ID：{dream_id}"
                )

                st.divider()

                # =========================
                # AI 榮格式分析
                # =========================
                if st.button(
                    "🔮 AI 榮格式分析",
                    key=f"rag_analyze_{dream_id}"
                ):

                    with st.spinner(
                        "正在分析夢境..."
                    ):

                        try:

                            result = generate_jungian_reflection(
                                content
                            )

                            st.session_state[
                                f"rag_result_{dream_id}"
                            ] = result

                        except Exception as e:

                            st.error(
                                f"分析失敗：{e}"
                            )

                rag_key = f"rag_result_{dream_id}"

                if rag_key in st.session_state:

                    result = st.session_state[
                        rag_key
                    ]

                    st.markdown(
                        "### ✨ AI Jungian Reflection"
                    )

                    st.caption(
                        "以下內容為 AI 輔助的榮格式自我反思，"
                        "並非心理診斷，也不存在唯一正確的夢境解讀。"
                    )

                    # AI 生成內容
                    st.markdown(
                        result["reflection"]
                    )

                    # Retrieval 資訊
                    with st.expander(
                        "🔎 查看 AI 使用的榮格概念"
                    ):

                        st.caption(
                            "DreamMap 會先利用 Embedding "
                            "找出與夢境語意最相關的榮格概念，"
                            "再把這些資料提供給 LLM。"
                        )

                        for concept in result["concepts"]:

                            score = max(
                                0,
                                min(
                                    1,
                                    concept["score"]
                                )
                            )

                            st.markdown(
                                f"#### {concept['name']}"
                            )

                            st.write(
                                f"語意相關度：{score:.0%}"
                            )

                            st.progress(score)

                            st.write(
                                concept["description"]
                            )

                            st.markdown(
                                f"💭 **反思方向：** "
                                f"{concept['question']}"
                            )

                            st.divider()

                st.divider()

                # =========================
                # 狀態 key
                # =========================
                edit_key = f"show_edit_{dream_id}"
                delete_key = f"confirm_delete_{dream_id}"

                if edit_key not in st.session_state:
                    st.session_state[edit_key] = False

                if delete_key not in st.session_state:
                    st.session_state[delete_key] = False

                # =========================
                # 編輯 / 刪除按鈕
                # =========================
                col_action1, col_action2 = st.columns(2)

                with col_action1:

                    if st.button(
                        "✏️ 編輯夢境",
                        key=f"edit_btn_{dream_id}",
                        use_container_width=True
                    ):
                        st.session_state[
                            edit_key
                        ] = not st.session_state[
                            edit_key
                        ]

                with col_action2:

                    if st.button(
                        "🗑️ 刪除夢境",
                        key=f"delete_btn_{dream_id}",
                        use_container_width=True
                    ):
                        st.session_state[
                            delete_key
                        ] = True

                # =========================
                # 編輯表單
                # =========================
                if st.session_state[edit_key]:

                    st.markdown("### ✏️ 編輯夢境")

                    with st.form(
                        f"edit_form_{dream_id}"
                    ):

                        edited_date = st.date_input(
                            "日期",
                            value=date.fromisoformat(
                                dream_date_value
                            ),
                            key=f"date_{dream_id}"
                        )

                        edited_content = st.text_area(
                            "夢境內容",
                            value=content,
                            height=180,
                            key=f"content_{dream_id}"
                        )

                        mood_options = [
                            "😄 開心",
                            "🙂 平靜",
                            "😐 普通",
                            "😟 焦慮",
                            "😢 難過",
                            "😨 害怕",
                            "😠 憤怒"
                        ]

                        edited_mood = st.selectbox(
                            "夢裡主要的感受",
                            mood_options,
                            index=(
                                mood_options.index(mood)
                                if mood in mood_options
                                else 2
                            ),
                            key=f"mood_{dream_id}"
                        )

                        save_edit = st.form_submit_button(
                            "💾 儲存修改",
                            use_container_width=True
                        )

                        if save_edit:

                            if edited_content.strip():

                                update_dream(
                                    dream_id,
                                    str(edited_date),
                                    edited_content.strip(),
                                    edited_mood
                                )

                                st.session_state[
                                    edit_key
                                ] = False

                                st.success(
                                    "修改成功！"
                                )

                                st.rerun()

                            else:

                                st.warning(
                                    "夢境內容不能是空白。"
                                )

                # =========================
                # 刪除確認
                # =========================
                if st.session_state[delete_key]:

                    st.warning(
                        "確定要刪除這筆夢境嗎？此操作無法復原。"
                    )

                    confirm_col1, confirm_col2 = st.columns(2)

                    with confirm_col1:

                        if st.button(
                            "✅ 確定刪除",
                            key=f"confirm_delete_btn_{dream_id}",
                            use_container_width=True
                        ):

                            delete_dream(
                                dream_id
                            )

                            st.session_state.pop(
                                delete_key,
                                None
                            )

                            st.session_state.pop(
                                edit_key,
                                None
                            )

                            st.session_state.pop(
                                f"rag_result_{dream_id}",
                                None
                            )

                            st.success(
                                "夢境已刪除。"
                            )

                            st.rerun()

                    with confirm_col2:

                        if st.button(
                            "取消",
                            key=f"cancel_delete_btn_{dream_id}",
                            use_container_width=True
                        ):

                            st.session_state[
                                delete_key
                            ] = False

                            st.rerun()

# ==================================================
# Tab 3：AI 搜尋
# ==================================================
with tab3:

    st.subheader("🔍 AI 夢境搜尋")

    st.info(
        "下一步我們會讓 AI 理解夢境的語意，"
        "讓你可以搜尋「迷路」、「朋友」、「學校」等相關夢境。"
    )

    search_text = st.text_input(
        "你想找什麼樣的夢？",
        placeholder="例如：我以前有沒有夢過迷路？",
        disabled=True
    )

    st.button(
        "🔍 搜尋夢境",
        disabled=True
    )


# ==================================================
# Tab 4：夢境地圖
# ==================================================
with tab4:

    st.subheader("✨ Dream Galaxy")

    st.info(
        "之後所有夢境都會變成地圖上的點，"
        "內容越相似的夢，會彼此靠得越近。"
    )

    st.write("🌌 Dream Galaxy 即將加入")

def delete_dream(dream_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM dreams WHERE id = ?",
        (dream_id,)
    )

    conn.commit()
    conn.close()