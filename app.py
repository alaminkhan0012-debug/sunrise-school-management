import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস হ্যান্ডলিং
def load_data(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=columns)

st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide", page_icon="🏫")

# মেনু
menu = ["📊 ড্যাশবোর্ড", "📝 ভর্তি ফরম", "📋 শিক্ষার্থী তালিকা"]
choice = st.sidebar.selectbox("মেনু", menu)

if choice == "📊 ড্যাশবোর্ড":
    st.markdown("<h1 style='text-align: center;'>Sun Rise Kinder Garten Portal</h1>", unsafe_allow_html=True)
    st.info("আপনার স্কুলের ডিজিটাল ম্যানেজমেন্ট সিস্টেমে স্বাগতম।")

elif choice == "📝 ভর্তি ফরম":
    st.markdown("<h2 style='text-align: center; background-color: #002D62; color: white; padding: 10px;'>ভর্তি আবেদন ফরম</h2>", unsafe_allow_html=True)
    
    with st.form("admission_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name_bn = st.text_input("১। শিক্ষার্থীর নাম (বাংলায়)")
            father_bn = st.text_input("২। পিতার নাম (বাংলায়)")
            mother_bn = st.text_input("৪। মাতার নাম (বাংলায়)")
            address = st.text_area("৫। ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
            f_job = st.text_input("৬। পিতার পেশা")
            last_school = st.text_input("৮। পূর্বে কোন শ্রেণীতে পড়েছো?")
        
        with col2:
            name_en = st.text_input("শিক্ষার্থীর নাম (ইংরেজিতে বড় অক্ষরে)")
            father_en = st.text_input("পিতার নাম (ইংরেজিতে বড় অক্ষরে)")
            mother_en = st.text_input("মাতার নাম (ইংরেজিতে বড় অক্ষরে)")
            dob = st.date_input("৭। জন্ম তারিখ", min_value=date(2010, 1, 1))
            m_job = st.text_input("মাতার পেশা")
            last_inst = st.text_input("৯। পূর্বে কোন প্রতিষ্ঠানে সেবা গ্রহণ করেছো?")

        st.markdown("---")
        col3, col4, col5 = st.columns(3)
        with col3:
            prev_roll = st.text_input("১০। পি.এস.সি/জে.এস.সি রোল (যদি থাকে)")
        with col4:
            prev_gpa = st.text_input("প্রাপ্ত জি.পি.এ")
        with col5:
            mobile = st.text_input("মোবাইল নম্বর (জরুরি যোগাযোগের জন্য)")

        st.warning("অঙ্গীকারনামা: আমি এই মর্মে অঙ্গীকার করছি যে, বিদ্যালয়ের সকল নির্দেশাবলী মেনে চলব।")
        
        submit = st.form_submit_button("আবেদন জমা দিন (Submit Application)")

        if submit:
            cols = ["Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Address", "DOB", "Mobile"]
            df = load_data("admissions.csv", cols)
            new_data = pd.DataFrame([[name_bn, name_en, father_bn, mother_bn, address, str(dob), mobile]], columns=cols)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("admissions.csv", index=False)
            st.success("আবেদনটি সফলভাবে ডাটাবেসে সেভ হয়েছে!")

elif choice == "📋 শিক্ষার্থী তালিকা":
    st.header("📋 নিবন্ধিত শিক্ষার্থীদের তালিকা")
    df = load_data("admissions.csv", ["Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Address", "DOB", "Mobile"])
    st.dataframe(df, use_container_width=True)
