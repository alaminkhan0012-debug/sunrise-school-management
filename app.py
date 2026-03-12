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

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise K.G. Master Pro", layout="wide", page_icon="🏫")

# --- কাস্টম প্রিমিয়াম স্টাইল ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background: #fff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #002D62; }
    .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .sidebar .sidebar-content { background: #002D62; color: white; }
    h1, h2, h3 { color: #002D62; }
    </style>
    """, unsafe_allow_html=True)

# --- লগইন সিস্টেম ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='card' style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=150)
        st.header("Admin Login")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("লগইন করুন", use_container_width=True):
            if user == "admin" and pw == "12345":
                st.session_state['logged_in'] = True
                st.rerun()
            else: st.error("তথ্য ভুল!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- সাইডবার ও নেভিগেশন ---
st.sidebar.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=100)
st.sidebar.title("Sun Rise K.G.")
menu = ["📊 ড্যাশবোর্ড", "📝 স্টুডেন্ট ভর্তি", "👥 ছাত্র-ছাত্রী তালিকা", "✅ হাজিরা", "🎓 রেজাল্ট ও মার্কশিট", "🎟️ এডমিট কার্ড", "💰 ফিস কালেকশন"]
choice = st.sidebar.radio("মেনু নির্বাচন করুন", menu)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "F_Job", "Class", "DOB", "Mobile", "Address", "Date"]

# --- ১. ড্যাশবোর্ড ---
if choice == "📊 ড্যাশবোর্ড":
    st.title("🏫 স্কুল ম্যানেজমেন্ট ড্যাশবোর্ড")
    df = load_data("students.csv", STD_COLS)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("মোট শিক্ষার্থী", len(df))
    col2.metric("আজকের তারিখ", date.today().strftime("%d %b, %y"))
    col3.metric("টিচার্স", "৪ জন")
    col4.metric("অবস্থান", "হূমাইপুর")

    st.markdown("---")
    c_l, c_r = st.columns([2, 1])
    with c_l:
        st.markdown("<div class='card'><h3>📈 শ্রেণীভিত্তিক পরিসংখ্যান</h3>", unsafe_allow_html=True)
        if not df.empty:
            fig = px.bar(df, x='Class', color='Class', title="Students by Class")
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("কোনো ডাটা নেই।")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c_r:
        st.markdown("<div class='card'><h3>🔔 নোটিশ বোর্ড</h3>", unsafe_allow_html=True)
        st.success("✅ ২০২৫ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.warning("⚠️ আগামী বুধবার মিটিং অনুষ্ঠিত হবে।")
        st.markdown("</div>", unsafe_allow_html=True)

# --- ২. ভর্তি ফরম (আপনার ছবির নমুনা অনুযায়ী) ---
elif choice == "📝 স্টুডেন্ট ভর্তি":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("📝 ভর্তি আবেদন ফরম")
    with st.form("admission", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            n_bn = st.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
            f_bn = st.text_input("২। পিতার নাম (বাংলা)")
            m_bn = st.text_input("৪। মাতার নাম (বাংলা)")
            f_job = st.text_input("৬। পিতার পেশা")
            s_class = st.selectbox("শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        with col2:
            n_en = st.text_input("Name (English Block)")
            f_en = st.text_input("Father's Name (Block)")
            m_en = st.text_input("Mother's Name (Block)")
            dob = st.date_input("৭। জন্ম তারিখ")
            mobile = st.text_input("মোবাইল নম্বর")
        
        addr = st.text_area("৫। ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("ভর্তি সম্পন্ন করুন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202500 + len(df) + 1
            new_row = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, f_job, s_class, str(dob), mobile, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.balloons()
            st.success(f"সাফল্যজনক ভর্তি! আইডি: {new_id}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ৩. এডিট ও ডিলিট ম্যানেজমেন্ট ---
elif choice == "👥 ছাত্র-ছাত্রী তালিকা":
    st.header("👥 শিক্ষার্থীর তথ্য ম্যানেজমেন্ট")
    df = load_data("students.csv", STD_COLS)
    
    search = st.text_input("🔍 নাম বা আইডি দিয়ে খুঁজুন")
    if search:
        df = df[df['Name_BN'].str.contains(search, na=False) | df['ID'].astype(str).contains(search, na=False)]
    
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🗑️ তথ্য সংশোধন বা ডিলিট")
    del_id = st.number_input("আইডি দিন", min_value=0)
    if st.button("মুছে ফেলুন"):
        df = df[df['ID'] != del_id]
        df.to_csv("students.csv", index=False)
        st.warning(f"আইডি {del_id} মুছে ফেলা হয়েছে।")
        st.rerun()

# --- ৪. এডমিট কার্ড প্রিন্ট ---
elif choice == "🎟️ এডমিট কার্ড":
    st.header("🎟️ প্রবেশ পত্র জেনারেটর")
    a_id = st.number_input("আইডি দিন", min_value=0)
    df = load_data("students.csv", STD_COLS)
    if st.button("তৈরি করুন"):
        std = df[df['ID'] == a_id]
        if not std.empty:
            s = std.iloc[0]
            st.markdown(f"""
            <div style="border: 5px solid #002D62; padding: 20px; width: 500px; margin: auto; background: white;">
                <div style="text-align: center;">
                    <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="80">
                    <h2 style="margin: 0;">Sun Rise Kinder Garten</h2>
                    <p>স্থাপিত: ২০২৫ খ্রিঃ</p>
                </div>
                <hr>
                <p><b>আইডি:</b> {s['ID']} | <b>শ্রেণী:</b> {s['Class']}</p>
                <p><b>নাম:</b> {s['Name_BN']}</p>
                <p><b>পরীক্ষা:</b> বার্ষিক পরীক্ষা - ২০২৬</p>
            </div>
            """, unsafe_allow_html=True)
        else: st.error("আইডি পাওয়া যায়নি।")

# লগআউট
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()
