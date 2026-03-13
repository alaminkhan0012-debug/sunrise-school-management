import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px

# ডাটাবেস হ্যান্ডলিং
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        for col in columns:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

# পেজ কনফিগারেশন
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide", page_icon="🏫")

# --- কাস্টম সিএসএস (ckgghs.edu.bd এর মতো লুক দিতে) ---
st.markdown("""
    <style>
    .header-box { background-color: #002D62; padding: 20px; color: white; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .marquee-text { background: #FFD700; padding: 10px; font-weight: bold; color: #000; border-radius: 5px; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #002D62; }
    </style>
    """, unsafe_allow_html=True)

# --- হেডার সেকশন ---
st.markdown(f"""
    <div class="header-box">
        <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="100">
        <h1>সানরাইজ কিন্ডারগার্টেন</h1>
        <p>স্থাপিত: ২০২৫ খ্রিঃ | হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ</p>
    </div>
    """, unsafe_allow_html=True)

# স্ক্রলিং নোটিশ
st.markdown('<div class="marquee-text"><marquee>২০২৫ শিক্ষাবর্ষের ভর্তি চলছে... নতুন রুটিন প্রকাশিত হয়েছে... বার্ষিক ক্রীড়া প্রতিযোগিতা আগামী মাসে অনুষ্ঠিত হবে...</marquee></div>', unsafe_allow_html=True)

# --- সাইডবার মেনু ---
st.sidebar.title("মেইন মেনু")
menu = ["🏠 হোম পেজ", "📝 অনলাইন ভর্তি", "🎓 রেজাল্ট", "🎟️ এডমিট কার্ড", "👤 অ্যাডমিন লগইন"]
choice = st.sidebar.radio("বিভাগ নির্বাচন করুন", menu)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Class", "Phone", "Address", "Date"]

# --- ১. হোম পেজ (পাবলিক ভিউ) ---
if choice == "🏠 হোম পেজ":
    st.title("স্বাগতম!")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'><h3>স্কুল পরিচিতি</h3><p>শিক্ষাই শক্তি, জ্ঞানই আলো - এই স্লোগানকে সামনে রেখে আমাদের পথচলা। সানরাইজ কিন্ডারগার্টেন এলাকার প্রতিটি শিশুর গুণগত শিক্ষা নিশ্চিত করতে প্রতিশ্রুতিবদ্ধ।</p></div>", unsafe_allow_html=True)
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", caption="আমাদের ক্যাম্পাস (নমুনা ছবি)")

    with col2:
        st.markdown("<div class='card'><h3>জরুরি নোটিশ</h3><ul><li>ভর্তি ফরম বিতরণ শুরু</li><li>নতুন ইউনিফর্মের নির্দেশিকা</li><li>স্কুল ডায়েরি সংগ্রহ করুন</li></ul></div>", unsafe_allow_html=True)

# --- ২. অনলাইন ভর্তি (আপনার ছবির নমুনা অনুযায়ী) ---
elif choice == "📝 অনলাইন ভর্তি":
    st.title("📝 অনলাইন ভর্তি আবেদন")
    with st.form("admission_form", clear_on_submit=True):
        st.info("সঠিক তথ্য দিয়ে ফরমটি পূরণ করুন (ছবিতে দেওয়া তথ্য অনুযায়ী)")
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English Block)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        m_bn = c2.text_input("৪। মাতার নাম (বাংলা)")
        s_class = c1.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        phone = c2.text_input("মোবাইল নম্বর (জরুরি)")
        addr = st.text_area("ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("আবেদন জমা দিন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202500 + len(df) + 1
            new_data = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, s_class, phone, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"আপনার আবেদন সফল হয়েছে। আপনার আইডি: {new_id}")

# --- ৩. অ্যাডমিন সেকশন (লগইন প্রয়োজন) ---
elif choice == "👤 অ্যাডমিন লগইন":
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        user = st.text_input("অ্যাডমিন ইউজার")
        pw = st.text_input("পাসওয়ার্ড", type="password")
        if st.button("লগইন"):
            if user == "admin" and pw == "12345":
                st.session_state['logged_in'] = True
                st.rerun()
            else: st.error("ভুল তথ্য!")
    else:
        st.title("📊 ম্যানেজমেন্ট ড্যাশবোর্ড")
        df = load_data("students.csv", STD_COLS)
        st.metric("মোট শিক্ষার্থী", len(df))
        st.dataframe(df, use_container_width=True)
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
