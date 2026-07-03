import streamlit as st
import gspread
import json
import pandas as pd
from datetime import datetime

# 1. Google Sheets ချိတ်ဆက်ခြင်း (Secrets ထည့်ထားပြီးသားလို့ ယူဆပါတယ်)
creds_dict = json.loads(st.secrets["gcp_service_account"]["json_key"])
gc = gspread.service_account_from_dict(creds_dict)

# *** ဒီနေရာမှာ အစ်ကို့ Google Sheet ဖိုင်နာမည်ကို အမှန်အတိုင်း ပြင်ရေးပါ ***
# ဥပမာ - "Hardware_POS_Data"
spreadsheet = gc.open("hardware_pos_app") 

sh_master = spreadsheet.worksheet("Master_Products")
sh_sales = spreadsheet.worksheet("Sales_Record")

# 2. ပစ္စည်းစာရင်းကို DataFrame အဖြစ် ဖတ်ခြင်း
data = sh_master.get_all_records()
df = pd.DataFrame(data)

st.title("🛒 Hardware POS System")

# ပစ္စည်းရွေးချယ်ရန်
st.subheader("ရောင်းချရန် ပစ္စည်းရွေးချယ်ပါ")
selected_product_name = st.selectbox("ပစ္စည်းနာမည် (Product Name)", df['Product_Name'].tolist())

# ရွေးလိုက်တဲ့ ပစ္စည်းရဲ့ အချက်အလက်တွေကို ရှာဖွေခြင်း
product_info = df[df['Product_Name'] == selected_product_name].iloc[0]

# အချက်အလက်များ ပြသခြင်း
col1, col2 = st.columns(2)
with col1:
    st.write(f"**ID:** {product_info['Porduct_ID']}")
    st.write(f"**Category:** {product_info['Category']}")
with col2:
    st.write(f"**Price:** {product_info['Sell_Price']} MMK")
    st.write(f"**Stock:** {product_info['In_Stock']}")

# အရောင်းမှတ်တမ်းသွင်းရန် Form
st.subheader("အရောင်းမှတ်တမ်းသွင်းရန်")
customer_name = st.text_input("Customer Name")
qty = st.number_input("Quantity", min_value=1, value=1)

# တွက်ချက်ခြင်း
amount = product_info['Sell_Price'] * qty
total_amount = amount # (ဒီနေရာမှာ tax တို့ ဘာတို့ ထည့်ချင်ရင် ပြင်လို့ရပါတယ်)

if st.button("Save Sale"):
    try:
        # Sales_Record format အတိုင်း Append လုပ်ခြင်း
        # [Transition_Date, Product_ID, Customer_Name, Category, Qty, Amount, Total_Amount]
        sh_sales.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product_info['Porduct_ID'],
            customer_name,
            product_info['Category'],
            qty,
            product_info['Sell_Price'],
            total_amount
        ])
        st.success(f"{customer_name} အတွက် အရောင်းမှတ်တမ်း သိမ်းပြီးပါပြီ!")
    except Exception as e:
        st.error(f"Error တက်နေပါတယ်: {e}")
