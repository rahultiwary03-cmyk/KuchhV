import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & MEGA DATABASE FILES
# ==========================================
st.set_page_config(page_title="KuchhV | Har Zarurat, Ek Platform", layout="wide", page_icon="🇮🇳")

REQUIREMENTS_FILE = "req_v6.csv"
PARTNERS_FILE = "partners_v6.csv"
ORDERS_FILE = "orders_v6.csv"
PRODUCTS_FILE = "products_v6.csv"

# Comprehensive Pan-India Categories
INDIAN_SERVICES = sorted([
    "Grocery & Daily Needs", "Fresh Vegetables & Fruits", "Dairy & Milk Delivery",
    "Plumber", "Electrician", "Carpenter", "AC Repair & Servicing", "Pest Control",
    "IT Freelancer (Python/Data)", "Web & App Developer", "Video Editor & AI Creator",
    "Tractor & Harvester Rental", "JCB & Crane Rental", "Mini Truck (Tata Ace)", "Bike Taxi", "Cab Booking",
    "CA & GST Filing", "Pragya Kendra (CSC) & Forms", "Lawyer & Notary", "Pension & PF Help",
    "Real Estate (Rent/Buy)", "PG & Hostel Booking", "Commercial Shop Rent",
    "Doctor Appointment", "Medicine Delivery", "Lab Test at Home", "Ambulance Booking",
    "Men's Salon", "Women's Parlour", "Bridal Makeup", "Mehndi Artist",
    "Tent House & Decorator", "Caterers (Halwai)", "Pandit Ji for Puja",
    "Labour Contractor (Daily Wage)", "Rajmistri (Mason)", "Security Guards/Bouncers",
    "Online Kabaadiwala (Scrap)", "E-Auction & Properties"
])

for file, cols in [
    (REQUIREMENTS_FILE, ["Timestamp", "Phone", "Category", "Requirement", "Location", "Status"]),
    (PARTNERS_FILE, ["Phone", "Password", "Business_Name", "Category", "Verification_Status", "Base_Price"]),
    (ORDERS_FILE, ["Timestamp", "Customer_Phone", "Item_Name", "Category", "Price", "Partner_Assigned", "Status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

# Seed Mega Authentic Catalog with Colorful Symbolic Pictures
if not os.path.exists(PRODUCTS_FILE):
    dummy_products = pd.DataFrame([
        # Grocery & Daily
        {"Item_Name": "Aashirvaad Atta (5kg)", "Category": "Grocery & Daily Needs", "Price": "220", "Image_URL": "https://placehold.co/400x300/f59e0b/ffffff?text=Atta+(5kg)"},
        {"Item_Name": "Amul Taaza Milk (1L)", "Category": "Dairy & Milk Delivery", "Price": "68", "Image_URL": "https://placehold.co/400x300/3b82f6/ffffff?text=Amul+Milk"},
        {"Item_Name": "Fresh Onion (1kg)", "Category": "Fresh Vegetables & Fruits", "Price": "35", "Image_URL": "https://placehold.co/400x300/ec4899/ffffff?text=Fresh+Onion"},
        # Home Services
        {"Item_Name": "AC Deep Servicing", "Category": "AC Repair & Servicing", "Price": "499", "Image_URL": "https://placehold.co/400x300/06b6d4/ffffff?text=AC+Service"},
        {"Item_Name": "Plumber (Visit Charge)", "Category": "Plumber", "Price": "199", "Image_URL": "https://placehold.co/400x300/64748b/ffffff?text=Plumber+Visit"},
        # Logistics & Rentals
        {"Item_Name": "Tata Ace (Chota Hathi)", "Category": "Mini Truck (Tata Ace)", "Price": "800", "Image_URL": "https://placehold.co/400x300/eab308/ffffff?text=Tata+Ace+Booking"},
        {"Item_Name": "Mahindra Tractor Rental", "Category": "Tractor & Harvester Rental", "Price": "1200", "Image_URL": "https://placehold.co/400x300/ef4444/ffffff?text=Tractor+Rental"},
        # IT & Professional
        {"Item_Name": "GST Registration", "Category": "CA & GST Filing", "Price": "1499", "Image_URL": "https://placehold.co/400x300/10b981/ffffff?text=GST+Filing"},
        {"Item_Name": "Excel Data Management", "Category": "IT Freelancer (Python/Data)", "Price": "999", "Image_URL": "https://placehold.co/400x300/8b5cf6/ffffff?text=Data+Freelancer"},
        {"Item_Name": "JMMMSY / Pension Form Help", "Category": "Pragya Kendra (CSC) & Forms", "Price": "50", "Image_URL": "https://placehold.co/400x300/14b8a6/ffffff?text=CSC+Form+Help"},
        # Real Estate & Labour
        {"Item_Name": "Rajmistri (1 Day)", "Category": "Rajmistri (Mason)", "Price": "700", "Image_URL": "https://placehold.co/400x300/d97706/ffffff?text=Rajmistri"},
        {"Item_Name": "Labour (1 Day)", "Category": "Labour Contractor (Daily Wage)", "Price": "400", "Image_URL": "https://placehold.co/400x300/f97316/ffffff?text=Daily+Labour"},
        {"Item_Name": "2BHK Flat for Rent", "Category": "Real Estate (Rent/Buy)", "Price": "8500", "Image_URL": "https://placehold.co/400x300/6366f1/ffffff?text=2BHK+Rent"},
        # Events & Healthcare
        {"Item_Name": "Bridal Mehndi Design", "Category": "Mehndi Artist", "Price": "2100", "Image_URL": "https://placehold.co/400x300/be185d/ffffff?text=Bridal+Mehndi"},
        {"Item_Name": "Full Body Health Checkup", "Category": "Lab Test at Home", "Price": "1299", "Image_URL": "https://placehold.co/400x300/f43f5e/ffffff?text=Lab+Test"}
    ])
    dummy_products.to_csv(PRODUCTS_FILE, index=False)

def load_data(file_name):
    return pd.read_csv(file_name, dtype=str)

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

def overwrite_data(file_name, df):
    df.to_csv(file_name, index=False)

# ==========================================
# 2. VIBRANT PROFESSIONAL UI CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #020617 0%, #1e3a8a 100%); }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    .support-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-top: 20px; border: 1px solid rgba(255,255,255,0.1); }
    
    .product-card { 
        background: white; border-radius: 16px; border: 1px solid #e2e8f0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); text-align: center; margin-bottom: 25px; overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2); border-color: #3b82f6; }
    .product-image-container { width: 100%; height: 180px; overflow: hidden; background: #f1f5f9; }
    .product-image-container img { width: 100%; height: 100%; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-cat { font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;}
    .product-title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 8px 0; height: 50px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;}
    .product-price { color: #059669; font-size: 24px; font-weight: 900; margin-bottom: 10px;}
    
    h1, h2, h3 { color: #0f172a; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 3. APP NAVIGATION & SUPPORT
# ==========================================
st.sidebar.title("🇮🇳 KuchhV Super App")
st.sidebar.caption("India's Hyperlocal Engine")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Main Menu:", ["🛍️ Explore Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Control Room"])
st.sidebar.write("---")

st.sidebar.markdown("""
<div class='support-box'>
    <h3 style='color: white; margin-bottom: 5px; font-size: 16px;'>🎧 24/7 Customer Support</h3>
    <p style='font-size: 13px; color: #94a3b8; margin-bottom: 10px;'>Need help with booking?</p>
    <p style='margin: 0; font-weight: bold; font-size: 18px;'>📞 8521413089</p>
    <p style='margin: 0; font-size: 13px; color: #cbd5e1;'>✉️ Rahultiwary03@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. CUSTOMER MARKETPLACE (Colorful Catalog)
# ==========================================
if app_mode == "🛍️ Explore Marketplace":
    st.title("🛍️ KuchhV Marketplace")
    st.markdown("### Browse thousands of authentic products and professional services.")
    
    selected_cat = st.selectbox("🔍 Filter by Category:", ["All India Categories"] + INDIAN_SERVICES)
    
    products_df = load_data(PRODUCTS_FILE)
    if selected_cat != "All India Categories":
        products_df = products_df[products_df['Category'] == selected_cat]
        
    if not products_df.empty:
        st.write("---")
        cols = st.columns(3) # 3 columns for bigger, beautiful cards
        
        for index, row in products_df.iterrows():
            with cols[index % 3]:
                st.markdown(f"""
                <div class='product-card'>
                    <div class='product-image-container'>
                        <img src="{row['Image_URL']}" alt="{row['Item_Name']}">
                    </div>
                    <div class='product-info'>
                        <div class='product-cat'>{row['Category']}</div>
                        <div class='product-title'>{row['Item_Name']}</div>
                        <div class='product-price'>₹{row['Price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.popover(f"⚡ Book / Buy Now", use_container_width=True):
                    with st.form(f"order_form_{index}"):
                        st.markdown(f"**Confirm Order:** {row['Item_Name']}")
                        phone = st.text_input("Enter Mobile No. to Confirm:")
                        if st.form_submit_button("Place Order Securely"):
                            if phone:
                                save_data(ORDERS_FILE, {
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Customer_Phone": phone, "Item_Name": row['Item_Name'],
                                    "Category": row['Category'], "Price": row['Price'],
                                    "Partner_Assigned": "Unassigned", "Status": "Pending Admin Verification"
                                })
                                st.success("✅ Order Placed! Admin will assign the best partner.")
                            else:
                                st.error("Phone number is required.")
    else:
        st.info("No items found in this category yet. Admin is updating the catalog!")

# ==========================================
# 5. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 Custom Requirement Hub")
    st.write("If it's not in the catalog, just post it here. We will find it for you!")
    
    with st.container():
        with st.form("req_form"):
            col1, col2 = st.columns(2)
            with col1:
                req_cat = st.selectbox("Select Relevant Category", INDIAN_SERVICES)
                loc = st.text_input("Delivery Pincode / Area")
            with col2:
                phone = st.text_input("Your Mobile Number")
            desc = st.text_area("Describe exactly what you need in detail:")
            if st.form_submit_button("Broadcast Requirement 🚀"):
                if phone and desc and loc:
                    save_data(REQUIREMENTS_FILE, {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Phone": phone, "Category": req_cat, "Requirement": desc, "Location": loc, "Status": "Open"
                    })
                    st.success("✅ Broadcasted! Local partners will contact you.")
                else:
                    st.error("Please fill all details.")

# ==========================================
# 6. PARTNER PORTAL
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    if st.session_state['logged_in_partner'] is None:
        t1, t2 = st.tabs(["🔐 Login", "📝 Register New Business"])
        with t2:
            with st.form("reg_form"):
                biz_name = st.text_input("Business Name")
                phone = st.text_input("Mobile Number")
                pwd = st.text_input("Password", type="password")
                cat = st.selectbox("Category", INDIAN_SERVICES)
                if st.form_submit_button("Register Account"):
                    pdf = load_data(PARTNERS_FILE)
                    if phone in pdf['Phone'].values:
                        st.error("Already registered!")
                    else:
                        save_data(PARTNERS_FILE, {"Phone": phone, "Password": pwd, "Business_Name": biz_name, "Category": cat, "Verification_Status": "Pending", "Base_Price": "0"})
                        st.success("✅ Registered! Wait for Admin approval.")
        with t1:
            l_phone = st.text_input("Mobile Number ")
            l_pwd = st.text_input("Password ", type="password")
            if st.button("Login"):
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
# 7. ADMIN CONTROL ROOM
# ==========================================
elif app_mode == "⚙️ Admin Control Room":
    st.title("⚙️ Super Admin Dashboard")
    st.write("Complete system control: Manage Catalog, Orders, and Partners.")
    
    t_orders, t_catalog, t_partners = st.tabs(["🚨 Manage Orders", "📸 Global Catalog", "👥 Manage Partners"])
    
    with t_orders:
        st.subheader("Order Management & Assignment")
        odf = load_data(ORDERS_FILE)
        unassigned = odf[odf['Partner_Assigned'] == 'Unassigned']
        if not unassigned.empty:
            st.error(f"🚨 ACTION REQUIRED: {len(unassigned)} Order(s) need a partner assigned!")
            
        edited_odf = st.data_editor(odf, num_rows="dynamic", use_container_width=True, key="edit_orders")
        if st.button("💾 Save Order Changes"):
            overwrite_data(ORDERS_FILE, edited_odf)
            st.success("Orders updated successfully!")
            
    with t_catalog:
        st.subheader("Expand Platform Catalog")
        st.info("💡 Tip: To add a real photo, paste any image link from the internet in the 'Image_URL' column.")
        prodf = load_data(PRODUCTS_FILE)
        edited_prodf = st.data_editor(prodf, num_rows="dynamic", use_container_width=True, key="edit_catalog")
        if st.button("💾 Save Catalog Updates"):
            overwrite_data(PRODUCTS_FILE, edited_prodf)
            st.success("Catalog updated successfully!")

    with t_partners:
        st.subheader("Partner Database")
        pdf = load_data(PARTNERS_FILE)
        edited_pdf = st.data_editor(pdf, num_rows="dynamic", use_container_width=True, key="edit_partners")
        if st.button("💾 Save Partner Approvals"):
            overwrite_data(PARTNERS_FILE, edited_pdf)
            st.success("Partners updated successfully!")
