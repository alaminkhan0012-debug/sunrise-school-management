import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস ফাংশন
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        for col in columns:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide")

# --- সেশন স্টেট (লগইন ও স্লাইড কন্ট্রোল) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_comment' not in st.session_state:
    st.session_state.show_comment = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

def toggle_comment():
    st.session_state.show_comment = not st.session_state.show_comment
    st.session_state.show_login = False

def toggle_login():
    st.session_state.show_login = not st.session_state.show_login
    st.session_state.show_comment = False

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .school-title-bn { color: #ff3b30; font-size: 35px; font-weight: bold; line-height: 1.1; }
    .school-title-en { color: #2e7d32; font-size: 20px; font-weight: bold; }
    /* ডান পাশে ছোট স্লাইড বক্স */
    .slide-panel {
        background-color: #000;
        padding: 15px;
        color: white;
        border-radius: 0 0 0 10px;
        border-left: 3px solid #ff3b30;
        margin-bottom: 10px;
    }
    .stButton>button { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. ডান পাশের স্লাইড বাটন ও প্যানেল ---
col_main_top, col_side_top = st.columns([7, 3])

with col_side_top:
    b1, b2 = st.columns(2)
    b1.button("মন্তব্য ▼", on_click=toggle_comment, use_container_width=True)
    b2.button("লগ ইন ▼", on_click=toggle_login, use_container_width=True)

    # মন্তব্য স্লাইড প্যানেল
    if st.session_state.show_comment:
        st.markdown('<div class="slide-panel">', unsafe_allow_html=True)
        st.write("💬 মতামত দিন")
        st.text_input("নাম :", key="u_name")
        st.text_input("ফোন :", key="u_phone")
        st.text_area("মন্তব্য :", key="u_msg")
        st.button("পাঠান", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    # লগইন স্লাইড প্যানেল
    if st.session_state.show_login:
        st.markdown('<div class="slide-panel">', unsafe_allow_html=True)
        st.write("🔐 অ্যাডমিন লগইন")
        user = st.text_input("ইউজার :")
        pw = st.text_input("পাসওয়ার্ড :", type="password")
        if st.button("লগইন করুন"):
            if user == "admin" and pw == "12345":
                st.session_state.logged_in = True
                st.success("লগইন সফল!")
                st.rerun()
            else:
                st.error("ভুল তথ্য!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ২. হেডার (লোগো ও নাম) ---
h_l, h_r = st.columns([1, 6])
with h_l:
    st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=100)
with h_r:
    st.markdown("""
        <div style='margin-top: 10px;'>
            <div class="school-title-bn">সানরাইজ কিন্ডারগার্টেন</div>
            <div class="school-title-en">SUN RISE KINDER GARTEN</div>
        </div>
        """, unsafe_allow_html=True)

# --- ৩. মেনু এবং অ্যাডমিন ম্যানেজমেন্ট ---
menu = ["হোম পেজ", "স্কুল প্রশাসন", "প্রাতিষ্ঠানিক কার্যক্রম", "অনলাইন ভর্তি", "রেজাল্ট"]
if st.session_state.logged_in:
    menu.append("⚙️ ম্যানেজমেন্ট প্যানেল")

tabs = st.tabs(menu)

# --- ৪. হোম পেজ ---
with tabs[0]:
    c_left, c_right = st.columns([2.5, 1])
    with c_left:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        st.markdown("### স্বাগতম!")
        st.write("শিক্ষাই শক্তি, জ্ঞানই আলো।")
    with c_right:
        st.info("📢 নোটিশ: ২০২৬ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=150)

# --- ৫. ম্যানেজমেন্ট প্যানেল (লগইন করলেই অপশন ম্যানেজ করা যাবে) ---
if st.session_state.logged_in:
    with tabs[-1]:
        st.header("⚙️ স্কুল ম্যানেজমেন্ট সিস্টেম")
        option = st.selectbox("কি ম্যানেজ করতে চান?", ["ভর্তি তালিকা", "শিক্ষক তথ্য", "নোটিশ আপডেট"])
        
        if option == "ভর্তি তালিকা":
            st.write("এখানে সকল শিক্ষার্থীর তথ্য দেখা যাবে।")
            # ডাটাবেস থেকে তথ্য লোড করার কোড এখানে হবে
        
        if st.button("লগ আউট"):
            st.session_state.logged_in = False
            st.rerun()

# --- ৬. ফুটার ---
st.markdown('<div style="text-align:center; padding:20px; color:#666;">© ২০২৬ সানরাইজ কিন্ডারগার্টেন | বাজিতপুর, কিশোরগঞ্জ।</div>', unsafe_allow_html=True)
