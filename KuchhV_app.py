import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & DATABASE FILES
# ==========================================
st.set_page_config(page_title="KuchhV | Har Zarurat, Ek Platform", layout="wide", page_icon="🛒")

# Using v5 files to keep new structure clean
REQUIREMENTS_FILE = "req_v5.csv"
PARTNERS_FILE = "partners_v5.csv"
ORDERS_FILE = "orders_v5.csv"
PRODUCTS_FILE = "products_v5.csv"  # NEW: Global Catalog with Photos

INDIAN_SERVICES = [
    "Grocery & Daily Needs", "Fresh Vegetables & Fruits", "Plumber", "Electrician", 
    "AC Repair & Servicing", "IT Freelancer (Python/Excel)", "Web Developer",
    "Tractor Rental", "Mini Truck (Tata Ace) Booking", "Bike Taxi",
    "CA & GST Filing", "Real Estate (Rent/Buy)", "Medicine Delivery", "Men's Salon"
]

# Create files if missing
for file, cols in [
    (REQUIREMENTS_FILE, ["Timestamp", "Phone", "Category", "Requirement", "Location", "Status"]),
    (PARTNERS_FILE, ["Phone", "Password", "Business_Name", "Category", "Verification_Status", "Base_Price"]),
    (ORDERS_FILE, ["Timestamp", "Customer_Phone", "Item_Name", "Category", "Price", "Partner_Assigned", "Status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

# Seed dummy products with images if catalog is empty
if not os.path.exists(PRODUCTS_FILE):
    dummy_products = pd.DataFrame([
        {"Item_Name": "Aashirvaad Atta (5kg)", "Category": "Grocery & Daily Needs", "Price": "220", "Image_URL": "https://placehold.co/300x300/e2e8f0/1e293b?text=Atta+5kg"},
        {"Item_Name": "Amul Taaza Milk (1L)", "Category": "Grocery & Daily Needs", "Price": "68", "Image_URL": "https://placehold.co/300x300/e2e8f0/1e293b?text=Amul+Milk"},
        {"Item_Name": "AC Deep Servicing", "Category": "AC Repair & Servicing", "Price": "499", "Image_URL": "https://placehold.co/300x300/e2e8f0/1e293b?text=AC+Service"},
        {"Item_Name": "Tata Ace (Chota Hathi)", "Category": "Mini Truck (Tata Ace) Booking", "Price": "800", "Image_URL": "https://placehold.co/300x300/e2e8f0/1e293b?text=Tata+Ace"},
    ])
    dummy_products.to_csv(PRODUCTS_FILE, index=False)

def load_data(file_name):
    return pd.read_csv(file_name, dtype=str)

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

def overwrite_data(file_name, df):
    df.to_csv(file_name, index=False)

# CSS for Product Grid and UI
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e3a8a 100%); }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .support-box { background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(255,255,255,0.3); }
    .product-card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;}
    .product-price { color: #16a34a; font-size: 20px; font-weight: 800; margin: 10px 0;}
    .product-title { font-size: 16px; font-weight: 700; color: #1e293b; height: 45px; overflow: hidden;}
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 2. APP NAVIGATION & SUPPORT
# ==========================================
st.sidebar.title("📱 KuchhV Super App")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Main Menu:", ["🏠 Visual Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Control Room"])
st.sidebar.write("---")

st.sidebar.markdown("""
<div class='support-box'>
    <h3 style='color: white; margin-bottom: 5px;'>🎧 24/7 Support</h3>
    <p style='margin: 0; font-weight: bold;'>📞 8521413089</p>
    <p style='margin: 0; font-size: 12px;'>✉️ Rahultiwary03@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. CUSTOMER MARKETPLACE (Visual Catalog)
# ==========================================
if app_mode == "🏠 Visual Marketplace":
    st.title("🛒 KuchhV Marketplace")
    st.markdown("### Browse Items & Services with Lowest Prices")
    
    selected_cat = st.selectbox("🔍 Filter by Category:", ["All Categories"] + INDIAN_SERVICES)
    
    products_df = load_data(PRODUCTS_FILE)
    if selected_cat != "All Categories":
        products_df = products_df[products_df['Category'] == selected_cat]
        
    if not products_df.empty:
        st.write("---")
        # Create a grid of 4 columns
        cols = st.columns(4)
        
        for index, row in products_df.iterrows():
            with cols[index % 4]: # Distribute items across columns
                st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                st.image(row['Image_URL'], use_container_width=True)
                st.markdown(f"<div class='product-title'>{row['Item_Name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-price'>₹{row['Price']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.popover(f"Buy {row['Item_Name']}"):
                    with st.form(f"order_form_{index}"):
                        st.write(f"**Order:** {row['Item_Name']}")
                        phone = st.text_input("Enter Mobile No.")
                        if st.form_submit_button("Confirm Order"):
                            if phone:
                                save_data(ORDERS_FILE, {
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Customer_Phone": phone,
                                    "Item_Name": row['Item_Name'],
                                    "Category": row['Category'],
                                    "Price": row['Price'],
                                    "Partner_Assigned": "Unassigned", # Goes to Admin pool
                                    "Status": "Pending Admin/Partner Action"
                                })
                                st.success("Order Placed! Our team will contact you.")
                            else:
                                st.error("Phone number is required.")
    else:
        st.info("No items found in this category yet. Admin is updating the catalog!")

# ==========================================
# 4. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 Custom Requirement Hub")
    st.write("If you can't find an item with a photo, just post your requirement here!")
    
    with st.container():
        with st.form("req_form"):
            col1, col2 = st.columns(2)
            with col1:
                req_cat = st.selectbox("Category", INDIAN_SERVICES)
                loc = st.text_input("Pincode / City")
            with col2:
                phone = st.text_input("Mobile Number")
            desc = st.text_area("Detail your exact need:")
            if st.form_submit_button("Broadcast to Partners 🚀"):
                if phone and desc and loc:
                    save_data(REQUIREMENTS_FILE, {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Phone": phone, "Category": req_cat, "Requirement": desc, "Location": loc, "Status": "Open"
                    })
                    st.success("✅ Broadcasted!")
                else:
                    st.error("Please fill all details.")

# ==========================================
# 5. PARTNER PORTAL
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    if st.session_state['logged_in_partner'] is None:
        t1, t2 = st.tabs(["🔐 Login", "📝 Register Business"])
        with t2:
            with st.form("reg_form"):
                biz_name = st.text_input("Business Name")
                phone = st.text_input("Mobile Number")
                pwd = st.text_input("Password", type="password")
                cat = st.selectbox("Category", INDIAN_SERVICES)
                if st.form_submit_button("Register"):
                    pdf = load_data(PARTNERS_FILE)
                    if phone in pdf['Phone'].values:
                        st.error("Already registered!")
                    else:
                        save_data(PARTNERS_FILE, {"Phone": phone, "Password": pwd, "Business_Name": biz_name, "Category": cat, "Verification_Status": "Pending", "Base_Price": "0"})
                        st.success("✅ Registered! Wait for Admin approval.")
        with t1:
            l_phone = st.text_input("Mobile Number ")
            l_pwd = st.text_input("Password ", type="password")
            if st.button("Login Now"):
                pdf = load_data(PARTNERS_FILE)
                user = pdf[(pdf['Phone'] == l_phone) & (pdf['Password'] == l_pwd)]
                if not user.empty:
                    if user.iloc[0]['Verification_Status'] == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.rerun()
                    else:
                        st.error("Admin approval is pending.")
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"👋 Welcome, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
            
        st.subheader("📦 Orders Assigned to You")
        odf = load_data(ORDERS_FILE)
        my_orders = odf[odf['Partner_Assigned'] == st.session_state['logged_in_partner']]
        st.dataframe(my_orders, use_container_width=True)

# ==========================================
# 6. ADMIN CONTROL ROOM (Unassigned Orders & Catalog)
# ==========================================
elif app_mode == "⚙️ Admin Control Room":
    st.title("⚙️ Super Admin Dashboard")
    
    t_orders, t_catalog, t_partners = st.tabs(["🚨 Manage Orders", "📸 Global Catalog", "👥 Manage Partners"])
    
    with t_orders:
        st.subheader("Order Management")
        odf = load_data(ORDERS_FILE)
        
        # Highlight Unassigned Orders for Admin
        unassigned = odf[odf['Partner_Assigned'] == 'Unassigned']
        if not unassigned.empty:
            st.error(f"🚨 ALERT: {len(unassigned)} Order(s) need a partner assigned!")
            
        edited_odf = st.data_editor(odf, num_rows="dynamic", use_container_width=True, key="edit_orders")
        if st.button("💾 Save Order Changes"):
            overwrite_data(ORDERS_FILE, edited_odf)
            st.success("Orders updated!")
            
    with t_catalog:
        st.subheader("Add/Edit Products & Photos")
        st.info("Paste image URLs (e.g., from Google Images or Drive) in the 'Image_URL' column.")
        prodf = load_data(PRODUCTS_FILE)
        edited_prodf = st.data_editor(prodf, num_rows="dynamic", use_container_width=True, key="edit_catalog")
        if st.button("💾 Save Catalog"):
            overwrite_data(PRODUCTS_FILE, edited_prodf)
            st.success("Catalog updated!")

    with t_partners:
        st.subheader("Partner Database")
        pdf = load_data(PARTNERS_FILE)
        edited_pdf = st.data_editor(pdf, num_rows="dynamic", use_container_width=True, key="edit_partners")
        if st.button("💾 Save Partners"):
            overwrite_data(PARTNERS_FILE, edited_pdf)
            st.success("Partners updated!")
