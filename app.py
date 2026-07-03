import streamlit as st
import gspread
import json
import pandas as pd
from datetime import datetime

# 1. Google Sheets ချိတ်ဆက်ခြင်း
creds_dict = json.loads(st.secrets["gcp_service_account"]["json_key"])
gc = gspread.service_account_from_dict(creds_dict)

# Sheet နှစ်ခုကို ဖွင့်ခြင်း (နာမည်အမှန်အတိုင်းဖြစ်ဖို့လိုပါတယ်)
sh_master = gc.open("Master_Products").sheet1
sh_sales = gc.open("Sales_Record").sheet1

# 2. Master_Products ကနေ ပစ္စည်းစာရင်းတွေ ဖတ်ထုတ်ခြင်း
products_data = sh_master.get_all_records()
df = pd.DataFrame(products_data)

st.title("🛒 Hardware POS System")

# ပစ္စည်းစာရင်းကို ပြပေးခြင်း
st.subheader("ပစ္စည်းစာရင်း")
st.dataframe(df)

# 3. ရောင်းချမှု ပုံစံ (Form)
st.subheader("ရောင်းချမှု မှတ်တမ်းသွင်းရန်")

# ပစ္စည်းနာမည်များကို ရွေးချယ်ရန် Dropdown
# (df['Product'] နေရာမှာ အစ်ကို့ Sheet ထဲက ပစ္စည်းနာမည်ရှိတဲ့ Column ခေါင်းစဉ်နဲ့ တူအောင် ပြင်ပေးပါ)
product_list = df['Product'].tolist() 
selected_product = st.selectbox("ပစ္စည်းရွေးချယ်ပါ", product_list)

qty = st.number_input("အရေအတွက် (Quantity)", min_value=1, value=1)

# Save လုပ်သည့်အခါ
if st.button("ရောင်းချမှု မှတ်တမ်းသိမ်းမည်"):
    # လက်ရှိအချိန်ကို ယူခြင်း
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sales_Record ထဲကို အချက်အလက် ပို့ခြင်း
    # [ရက်စွဲ, ပစ္စည်းနာမည်, အရေအတွက်]
    sh_sales.append_row([sale_date, selected_product, qty])
    
    st.success(f"{selected_product} ({qty} ခု) ကို ရောင်းချမှုမှတ်တမ်းထဲ ထည့်လိုက်ပါပြီ။")
