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

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise Kinder Garten Portal", layout="wide")
st.title("☀️ Sun Rise Kinder Garten Management System")

# সাইডবার মেনু
menu = ["📊 ড্যাশবোর্ড", "📝 ছাত্র ভর্তি", "📋 ছাত্র তালিকা", "✅ হাজিরা (Attendance)", "💰 বেতন ও ফিস", "📝 পরীক্ষার রেজাল্ট"]
choice = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu)

# --- ১. ড্যাশবোর্ড ---
if choice == "📊 ড্যাশবোর্ড":
    st.header("স্কুলের সংক্ষিপ্ত চিত্র")
    std_df = load_data("students.csv", ["Name", "Roll", "Class", "Phone"])
    col1, col2, col3 = st.columns(3)
    col1.metric("মোট শিক্ষার্থী", len(std_df))
    col2.metric("আজকের তারিখ", str(date.today()))
    col3.info("আপনার ডিজিটাল স্কুল ম্যানেজমেন্ট সফলভাবে চলছে।")

# --- ২. ছাত্র ভর্তি ---
elif choice == "📝 ছাত্র ভর্তি":
    st.header("নতুন শিক্ষার্থী ভর্তি ফরম")
    with st.form("admission"):
        name = st.text_input("শিক্ষার্থীর নাম")
        roll = st.text_input("রোল নম্বর")
        s_class = st.selectbox("শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        guardian = st.text_input("পিতার নাম")
        phone = st.text_input("মোবাইল নম্বর")
        if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
            df = load_data("students.csv", ["Name", "Roll", "Class", "Guardian", "Phone"])
            new_data = pd.DataFrame([[name, roll, s_class, guardian, phone]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success("শিক্ষার্থী সফলভাবে নিবন্ধিত হয়েছে!")

# --- ৩. ছাত্র তালিকা ---
elif choice == "📋 ছাত্র তালিকা":
    st.header("শিক্ষার্থীদের ডাটাবেস")
    df = load_data("students.csv", ["Name", "Roll", "Class", "Guardian", "Phone"])
    st.dataframe(df, use_container_width=True)

# --- ৪. হাজিরা (Attendance) ---
elif choice == "✅ হাজিরা (Attendance)":
    st.header("দৈনিক হাজিরা")
    df = load_data("students.csv", ["Name", "Roll", "Class", "Guardian", "Phone"])
    today = str(date.today())
    if not df.empty:
        status = []
        for i, row in df.iterrows():
            st.write(f"{row['Name']} (রোল: {row['Roll']})")
            present = st.checkbox("উপস্থিত", key=f"att_{i}")
            status.append("Present" if present else "Absent")
        
        if st.button("হাজিরা সেভ করুন"):
            att_df = pd.DataFrame({"Date": [today]*len(df), "Name": df["Name"], "Status": status})
            att_df.to_csv(f"attendance_{today}.csv", index=False)
            st.success("আজকের হাজিরা সম্পন্ন হয়েছে।")

# --- ৫. বেতন ও ফিস ---
elif choice == "💰 বেতন ও ফিস":
    st.header("শিক্ষার্থীদের মাসিক ফিস")
    with st.form("fees"):
        f_roll = st.text_input("রোল নম্বর")
        amount = st.number_input("টাকার পরিমাণ", min_value=0)
        month = st.selectbox("মাস", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"])
        if st.form_submit_button("পেমেন্ট সেভ করুন"):
            fees_df = load_data("fees.csv", ["Roll", "Amount", "Month", "Date"])
            new_fee = pd.DataFrame([[f_roll, amount, month, str(date.today())]], columns=fees_df.columns)
            fees_df = pd.concat([fees_df, new_fee], ignore_index=True)
            fees_df.to_csv("fees.csv", index=False)
            st.success(f"রোল {f_roll}-এর {month} মাসের বেতন জমা হয়েছে।")

# --- ৬. পরীক্ষার রেজাল্ট ---
elif choice == "📝 পরীক্ষার রেজাল্ট":
    st.header("রেজাল্ট ও মার্কশিট জেনারেটর")
    r_roll = st.text_input("শিক্ষার্থীর রোল লিখুন")
    ban = st.number_input("বাংলা", 0, 100)
    eng = st.number_input("ইংরেজি", 0, 100)
    math = st.number_input("গণিত", 0, 100)
    if st.button("রেজাল্ট কার্ড দেখুন"):
        total = ban + eng + math
        avg = total / 3
        st.subheader("প্রোগ্রেস রিপোর্ট")
        st.write(f"মোট নম্বর: {total} (গড়: {avg:.2f})")
        if avg >= 33: st.success("ফলাফল: পাস")
        else: st.error("ফলাফল: অকৃতকার্য")
