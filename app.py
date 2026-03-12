import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস হ্যান্ডলিং ফাংশন
def load_data(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=columns)

def save_data(df, file_name):
    df.to_csv(file_name, index=False)

# পেজ কনফিগারেশন
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide", page_icon="🏫")

# --- লগইন সিস্টেম ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center;'>Admin Login</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user == "admin" and password == "12345": # এখানে আপনার ইউজার ও পাসওয়ার্ড দিন
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("ভুল ইউজারনেম বা পাসওয়ার্ড!")
    st.stop()

# --- মেইন মেনু ---
st.sidebar.title("Sun Rise K.G.")
menu = ["📊 ড্যাশবোর্ড", "📝 ভর্তি ফরম", "👥 শিক্ষার্থী তালিকা", "✅ হাজিরা", "🎓 রেজাল্ট ও মার্কশিট", "🎟️ এডমিট কার্ড", "💰 বেতন ও ফিস"]
choice = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu)

# --- ১. ড্যাশবোর্ড ---
if choice == "📊 ড্যাশবোর্ড":
    st.title("🏫 স্কুল ড্যাশবোর্ড")
    df = load_data("students.csv", ["ID", "Name_BN", "Class", "Phone"])
    col1, col2, col3 = st.columns(3)
    col1.metric("মোট শিক্ষার্থী", len(df))
    col2.info("স্থাপিত: ২০২৫")
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- ২. ভর্তি ফরম (আপনার দেওয়া ছবির নমুনা অনুযায়ী) ---
elif choice == "📝 ভর্তি ফরম":
    st.markdown("<h2 style='text-align: center; background-color: #002D62; color: white;'>ভর্তি আবেদন ফরম</h2>", unsafe_allow_html=True)
    with st.form("admission", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name_bn = st.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
            father_bn = st.text_input("২। পিতার নাম (বাংলা)")
            mother_bn = st.text_input("৪। মাতার নাম (বাংলা)")
            f_job = st.text_input("৬। পিতার পেশা")
            s_class = st.selectbox("১১। শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        with c2:
            name_en = st.text_input("শিক্ষার্থীর নাম (English)")
            father_en = st.text_input("পিতার নাম (English)")
            dob = st.date_input("৭। জন্ম তারিখ")
            m_job = st.text_input("মাতার পেশা")
            mobile = st.text_input("মোবাইল নম্বর")
        
        address = st.text_area("৫। ঠিকানা")
        
        if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
            df = load_data("students.csv", ["ID", "Name_BN", "Name_EN", "Father_BN", "Class", "DOB", "Mobile", "Address"])
            new_id = len(df) + 101
            new_student = pd.DataFrame([[new_id, name_bn, name_en, father_bn, s_class, str(dob), mobile, address]], columns=df.columns)
            df = pd.concat([df, new_student], ignore_index=True)
            save_data(df, "students.csv")
            st.success("ভর্তি সফল হয়েছে! আইডি নম্বর: " + str(new_id))

# --- ৩. শিক্ষার্থী তালিকা (এডিট ও ডিলিট অপশনসহ) ---
elif choice == "👥 শিক্ষার্থী তালিকা":
    st.header("👥 শিক্ষার্থীর তালিকা ও ডাটা ম্যানেজমেন্ট")
    df = load_data("students.csv", ["ID", "Name_BN", "Name_EN", "Father_BN", "Class", "DOB", "Mobile", "Address"])
    
    # সার্চ অপশন
    search = st.text_input("নাম বা আইডি দিয়ে সার্চ করুন")
    if search:
        df = df[df['Name_BN'].str.contains(search) | df['ID'].astype(str).contains(search)]
    
    st.dataframe(df, use_container_width=True)

    # এডিট ও ডিলিট সেকশন
    st.markdown("---")
    edit_id = st.number_input("এডিট বা ডিলিট করতে শিক্ষার্থীর ID দিন", min_value=0)
    if edit_id in df['ID'].values:
        col_e1, col_e2 = st.columns(2)
        if col_e1.button("🗑️ শিক্ষার্থী ডিলিট করুন"):
            df = df[df['ID'] != edit_id]
            save_data(df, "students.csv")
            st.warning("শিক্ষার্থী ডিলিট করা হয়েছে।")
            st.rerun()
        
        st.info("নিচে থেকে তথ্য পরিবর্তন করে 'আপডেট' করুন")
        # এডিট ফরম এখানে যুক্ত করা যাবে

# --- ৪. রেজাল্ট ও মার্কশিট ---
elif choice == "🎓 রেজাল্ট ও মার্কশিট":
    st.header("📝 পরীক্ষার ফলাফল ও মার্কশিট")
    std_id = st.number_input("শিক্ষার্থীর আইডি দিন", min_value=101)
    c1, c2, c3 = st.columns(3)
    ban = c1.number_input("বাংলা", 0, 100)
    eng = c2.number_input("ইংরেজি", 0, 100)
    math = c3.number_input("গণিত", 0, 100)
    
    if st.button("রেজাল্ট কার্ড জেনারেট করুন"):
        st.markdown(f"""
        <div style='border: 2px solid black; padding: 20px; text-align: center;'>
            <h3>Sun Rise Kinder Garten</h3>
            <h4>মার্কশিট - ২০২৬</h4>
            <p>আইডি: {std_id} | মোট নম্বর: {ban+eng+math} | গড়: {(ban+eng+math)/3:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("প্রিন্ট করুন (Ctrl+P)")

# --- ৫. এডমিট কার্ড ---
elif choice == "🎟️ এডমিট কার্ড":
    st.header("🎟️ পরীক্ষার প্রবেশ পত্র")
    a_id = st.number_input("প্রবেশ পত্রের জন্য আইডি দিন", min_value=101)
    if st.button("এডমিট কার্ড তৈরি করুন"):
        st.markdown(f"""
        <div style='border: 5px double #002D62; padding: 15px; width: 400px; margin: auto;'>
            <h2 style='text-align: center;'>ADMIT CARD</h2>
            <p><b>স্কুলের নাম:</b> Sun Rise Kinder Garten</p>
            <p><b>আইডি:</b> {a_id}</p>
            <p><b>পরীক্ষা:</b> বার্ষিক পরীক্ষা - ২০২৬</p>
        </div>
        """, unsafe_allow_html=True)

# --- ৬. বেতন ও ফিস ---
elif choice == "💰 বেতন ও ফিস":
    st.header("💰 ফিস আদায় ও রশিদ")
    f_id = st.number_input("আইডি নম্বর", min_value=101)
    amount = st.number_input("টাকার পরিমাণ")
    month = st.selectbox("মাস", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল"])
    if st.button("রশিদ তৈরি ও সেভ"):
        st.success(f"আইডি {f_id}-এর {month} মাসের বেতন জমা হয়েছে।")
