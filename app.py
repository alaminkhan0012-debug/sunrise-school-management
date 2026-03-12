import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস ফাংশন
def load_data(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise K.G. Admin", layout="wide", page_icon="🏫")

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .main { background-color: #f0f2f6; }
    
    /* লগইন কার্ড ডিজাইন */
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* মেট্রিক কার্ড ডিজাইন */
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- লগইন সেকশন ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=100)
        st.markdown("<h2 style='color: #002D62;'>স্কুল অ্যাডমিন লগইন</h2>", unsafe_allow_html=True)
        
        user = st.text_input("ইউজারনেম", placeholder="Admin ID")
        pw = st.text_input("পাসওয়ার্ড", type="password", placeholder="******")
        
        if st.button("লগইন করুন"):
            if user == "admin" and pw == "12345":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("সঠিক তথ্য দিয়ে চেষ্টা করুন")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- সাইডবার মেনু ---
st.sidebar.markdown("<h2 style='text-align: center; color: white; background: #002D62; padding: 10px; border-radius: 5px;'>Sun Rise K.G.</h2>", unsafe_allow_html=True)
menu = ["🏠 ড্যাশবোর্ড", "📝 ভর্তি ফরম (ছবি অনুযায়ী)", "👥 শিক্ষার্থী ম্যানেজমেন্ট", "📊 হাজিরা ও বেতন", "🎓 রেজাল্ট ও এডমিট কার্ড"]
choice = st.sidebar.radio("মেইন মেনু", menu)

if st.sidebar.button("লগআউট"):
    st.session_state['logged_in'] = False
    st.rerun()

# --- ১. আধুনিক ড্যাশবোর্ড ---
if choice == "🏠 ড্যাশবোর্ড":
    st.markdown("<h1 style='color: #002D62;'>স্কুল সামারি ড্যাশবোর্ড</h1>", unsafe_allow_html=True)
    
    df = load_data("students.csv", ["ID", "Name", "Class", "Phone"])
    fees_df = load_data("fees.csv", ["ID", "Amount", "Month"])
    
    # ড্যাশবোর্ড কার্ডসমূহ
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("মোট শিক্ষার্থী", len(df))
    m2.metric("আজকের তারিখ", str(date.today().strftime("%d %b, %Y")))
    m3.metric("মোট শিক্ষক", "৪ জন")
    m4.metric("সংগৃহীত ফি", f"৳ {fees_df['Amount'].sum()}")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("শ্রেণীভিত্তিক শিক্ষার্থী")
        if not df.empty:
            class_counts = df['Class'].value_counts()
            st.bar_chart(class_counts)
        else:
            st.info("কোনো ডাটা নেই")
            
    with c2:
        st.subheader("সাম্প্রতিক নোটিশ")
        st.success("১. আগামী রবিবার থেকে বার্ষিক পরীক্ষার ফরম পূরণ শুরু হবে।")
        st.warning("২. স্কুল ড্রেস ছাড়া ক্লাসে আসা নিষেধ।")

# --- ২. ভর্তি ফরম (আপনার দেওয়া নমুনার হুবহু তথ্য) ---
elif choice == "📝 ভর্তি ফরম (ছবি অনুযায়ী)":
    st.markdown("<h2 style='text-align: center; background-color: #002D62; color: white; padding: 10px;'>ভর্তি আবেদন ফরম (Sun Rise K.G.)</h2>", unsafe_allow_html=True)
    
    with st.form("detailed_admission", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            n_bn = st.text_input("শিক্ষার্থীর নাম (বাংলা)")
            f_bn = st.text_input("পিতার নাম (বাংলা)")
            m_bn = st.text_input("মাতার নাম (বাংলা)")
            f_job = st.text_input("পিতার পেশা")
            s_class = st.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        with col2:
            n_en = st.text_input("Student Name (English)")
            f_en = st.text_input("Father's Name (English)")
            dob = st.date_input("জন্ম তারিখ")
            phone = st.text_input("মোবাইল নম্বর")
            prev_school = st.text_input("পূর্ববর্তী প্রতিষ্ঠানের নাম")
            
        address = st.text_area("ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("আবেদন সেভ করুন"):
            df = load_data("students.csv", ["ID", "Name", "Class", "Phone", "Father", "Address"])
            new_id = len(df) + 1001
            new_entry = pd.DataFrame([[new_id, n_bn, s_class, phone, f_bn, address]], columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"সফলভাবে সেভ হয়েছে! আইডি নম্বর: {new_id}")

# --- ৩. এডিট ও ডিলিট ম্যানেজমেন্ট ---
elif choice == "👥 শিক্ষার্থী ম্যানেজমেন্ট":
    st.header("শিক্ষার্থী তথ্য সংশোধন ও তালিকা")
    df = load_data("students.csv", ["ID", "Name", "Class", "Phone", "Father", "Address"])
    
    if not df.empty:
        # সার্চ বার
        search_query = st.text_input("আইডি বা নাম দিয়ে খুঁজুন")
        filtered_df = df[df['Name'].str.contains(search_query) | df['ID'].astype(str).contains(search_query)]
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---")
        col_del1, col_del2 = st.columns([1, 3])
        delete_id = col_del1.number_input("ডিলিট করতে আইডি দিন", min_value=1001)
        if col_del1.button("❌ তথ্য মুছে ফেলুন"):
            df = df[df['ID'] != delete_id]
            df.to_csv("students.csv", index=False)
            st.error(f"আইডি {delete_id} মুছে ফেলা হয়েছে।")
            st.rerun()
    else:
        st.info("তালিকা খালি।")

# --- বাকি ফিচারগুলো (রেজাল্ট, বেতন) উপরের ড্যাশবোর্ডের মতো করেই কাজ করবে ---
