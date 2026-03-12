import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস হ্যান্ডলিং
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        # নিশ্চিত করা যে সব কলাম আছে, না থাকলে যোগ করা
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise K.G. Admin", layout="wide", page_icon="🏫")

# --- লগইন সেকশন ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='background:white; p:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align:center;'>", unsafe_allow_html=True)
        st.title("🔐 Admin Login")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("লগইন"):
            if user == "admin" and pw == "12345":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("ভুল তথ্য!")
    st.stop()

# --- সাইডবার ---
st.sidebar.title("Sun Rise K.G.")
menu = ["🏠 ড্যাশবোর্ড", "📝 ভর্তি ফরম", "👥 শিক্ষার্থী ম্যানেজমেন্ট", "🎓 রেজাল্ট ও এডমিট কার্ড"]
choice = st.sidebar.selectbox("মেনু", menu)

# ফাইল কলাম ডিফাইন করা (Error এড়াতে এটি গুরুত্বপূর্ণ)
STD_COLS = ["ID", "Name_BN", "Name_EN", "Class", "Phone", "Father", "Address"]

# --- ১. ড্যাশবোর্ড ---
if choice == "🏠 ড্যাশবোর্ড":
    st.title("📊 স্কুল ড্যাশবোর্ড")
    df = load_data("students.csv", STD_COLS)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("মোট শিক্ষার্থী", len(df))
    c2.metric("আজকের তারিখ", str(date.today()))
    c3.success("অ্যাডমিন প্যানেল সচল আছে।")
    
    st.markdown("---")
    st.subheader("সাম্প্রতিক ভর্তি হওয়া শিক্ষার্থী")
    st.table(df.tail(5))

# --- ২. ভর্তি ফরম ---
elif choice == "📝 ভর্তি ফরম":
    st.header("📝 নতুন ছাত্র ভর্তি")
    with st.form("admission", clear_on_submit=True):
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("নাম (বাংলা)")
        n_en = c2.text_input("Name (English)")
        f_bn = c1.text_input("পিতার নাম")
        s_class = c2.selectbox("শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        phone = c1.text_input("মোবাইল নম্বর")
        addr = c2.text_area("ঠিকানা")
        
        if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 2026001 + len(df)
            new_data = pd.DataFrame([[new_id, n_bn, n_en, s_class, phone, f_bn, addr]], columns=STD_COLS)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"সফলভাবে সেভ হয়েছে! আইডি: {new_id}")

# --- ৩. শিক্ষার্থী ম্যানেজমেন্ট (Error Fix করা হয়েছে) ---
elif choice == "👥 শিক্ষার্থী ম্যানেজমেন্ট":
    st.header("👥 শিক্ষার্থী তথ্য এডিট ও ডিলিট")
    df = load_data("students.csv", STD_COLS)
    
    if not df.empty:
        search_query = st.text_input("নাম (বাংলা) বা আইডি দিয়ে খুঁজুন")
        
        # এখানে Name এর বদলে Name_BN ব্যবহার করা হয়েছে এরর ঠিক করতে
        if search_query:
            filtered_df = df[df['Name_BN'].str.contains(search_query, na=False) | df['ID'].astype(str).contains(search_query, na=False)]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True)
        
        st.markdown("---")
        del_id = st.number_input("ডিলিট করতে আইডি দিন", min_value=0)
        if st.button("❌ ডিলিট করুন"):
            df = df[df['ID'] != del_id]
            df.to_csv("students.csv", index=False)
            st.warning(f"আইডি {del_id} মুছে ফেলা হয়েছে।")
            st.rerun()
    else:
        st.info("কোনো ডাটা পাওয়া যায়নি।")

elif st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()
