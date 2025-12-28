import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="Resort Operations Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: #f5f7fa;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(to right, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Cards */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Selectbox */
    .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Helper functions
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch {endpoint}")
            return []
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []

def update_status(endpoint, item_id, new_status):
    try:
        response = requests.put(
            f"{API_URL}/{endpoint}/{item_id}",
            json={"status": new_status}
        )
        if response.status_code == 200:
            st.success(f"Status updated to {new_status}!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Failed to update status")
    except Exception as e:
        st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    #st.image("https://via.placeholder.com/150/667eea/FFFFFF?text=Resort", use_container_width=True)
    st.title("🏨 Resort Ops")
    st.markdown("---")
    
    # Filters
    st.subheader("🔍 Filters")
    status_filter = st.multiselect(
        "Filter by Status",
        ["Pending", "Preparing", "Delivered", "In Progress", "Completed"],
        default=[]
    )
    
    room_filter = st.text_input("Room Number", placeholder="e.g., 101")
    
    st.markdown("---")
    
    # Auto-refresh
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.info("Dashboard will refresh every 30 seconds")
        time.sleep(30)
        st.rerun()
    
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.caption("Resort Operations Dashboard v2.0")

# Main content
st.title("🏨 Resort Operations Dashboard")
st.markdown("Real-time monitoring and management of resort operations")

# Fetch data
orders = fetch_data("orders")
requests_data = fetch_data("requests")

# Convert to DataFrames
df_orders = pd.DataFrame(orders) if orders else pd.DataFrame()
df_requests = pd.DataFrame(requests_data) if requests_data else pd.DataFrame()

# Apply filters
if not df_orders.empty and status_filter:
    df_orders = df_orders[df_orders['status'].isin(status_filter)]
if not df_orders.empty and room_filter:
    df_orders = df_orders[df_orders['room_number'].astype(str).str.contains(room_filter)]

if not df_requests.empty and status_filter:
    df_requests = df_requests[df_requests['status'].isin(status_filter)]
if not df_requests.empty and room_filter:
    df_requests = df_requests[df_requests['room_number'].astype(str).str.contains(room_filter)]

# Statistics Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_orders = len(df_orders) if not df_orders.empty else 0
    st.metric("📦 Total Orders", total_orders)

with col2:
    total_revenue = df_orders['total_amount'].sum() if not df_orders.empty else 0
    st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")

with col3:
    pending_orders = len(df_orders[df_orders['status'] == 'Pending']) if not df_orders.empty else 0
    st.metric("⏳ Pending Orders", pending_orders)

with col4:
    total_requests = len(df_requests) if not df_requests.empty else 0
    st.metric("🧹 Service Requests", total_requests)

st.markdown("---")

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🍽️ Orders", "🧹 Service Requests"])

with tab1:
    st.subheader("📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Order Status Distribution
        if not df_orders.empty:
            status_counts = df_orders['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Order Status Distribution",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available for chart")
    
    with col2:
        # Revenue by Room (Top 10)
        if not df_orders.empty:
            revenue_by_room = df_orders.groupby('room_number')['total_amount'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=revenue_by_room.index.astype(str),
                y=revenue_by_room.values,
                title="Top 10 Rooms by Revenue",
                labels={'x': 'Room Number', 'y': 'Revenue (₹)'},
                color=revenue_by_room.values,
                color_continuous_scale='Purples'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available for chart")
    
    # Service Request Types
    if not df_requests.empty:
        st.subheader("Service Request Types")
        request_types = df_requests['request_type'].value_counts()
        fig = px.bar(
            x=request_types.index,
            y=request_types.values,
            title="Service Requests by Type",
            labels={'x': 'Request Type', 'y': 'Count'},
            color=request_types.values,
            color_continuous_scale='Teal'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2d3748'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🍽️ Restaurant Orders")
    
    if not df_orders.empty:
        # Quick Action Buttons
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            selected_order = st.selectbox(
                "Select Order ID",
                df_orders['id'].tolist(),
                key="quick_order_select"
            )
        
        with col2:
            if st.button("🕒 Mark as Pending", key="order_pending_btn", use_container_width=True):
                update_status("orders", selected_order, "Pending")
        
        with col3:
            if st.button("🍳 Mark as Preparing", key="order_preparing_btn", use_container_width=True):
                update_status("orders", selected_order, "Preparing")
        
        with col4:
            if st.button("✅ Mark as Delivered", key="order_delivered_btn", use_container_width=True):
                update_status("orders", selected_order, "Delivered")
        
        st.markdown("---")
        
        # Format items column
        if "items" in df_orders.columns:
            df_orders_display = df_orders.copy()
            df_orders_display["items"] = df_orders_display["items"].apply(
                lambda x: ", ".join([f"{int(i['quantity'])}x {i['name']}" for i in x]) if isinstance(x, list) else str(x)
            )
        else:
            df_orders_display = df_orders
        
        # Display orders in editable table format
        display_cols = ['id', 'room_number', 'items', 'total_amount', 'status', 'created_at']
        available_cols = [col for col in display_cols if col in df_orders_display.columns]
        
        st.info("💡 Edit the status directly in the table below and click 'Save Changes' to update")
        
        edited_df = st.data_editor(
            df_orders_display[available_cols],
            use_container_width=True,
            hide_index=True,
            disabled=['id', 'room_number', 'items', 'total_amount', 'created_at'],
            column_config={
                "id": "Order ID",
                "room_number": "Room",
                "items": "Items",
                "total_amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pending", "Preparing", "Delivered"],
                    required=True
                ),
                "created_at": "Created At"
            },
            key="orders_editor"
        )
        
        # Check for changes and update
        if st.button("💾 Save Changes", key="save_orders", use_container_width=False):
            changes_made = False
            for idx in range(len(df_orders_display)):
                original_status = df_orders_display.iloc[idx]['status']
                new_status = edited_df.iloc[idx]['status']
                if original_status != new_status:
                    order_id = df_orders_display.iloc[idx]['id']
                    update_status("orders", order_id, new_status)
                    changes_made = True
            
            if not changes_made:
                st.info("No changes detected")
        
        # Export button
        st.markdown("---")
        csv = df_orders_display.to_csv(index=False)
        st.download_button(
            label="📥 Download Orders CSV",
            data=csv,
            file_name=f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No orders found")

with tab3:
    st.subheader("🧹 Service Requests")
    
    if not df_requests.empty:
        # Quick Action Buttons
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            selected_request = st.selectbox(
                "Select Request ID",
                df_requests['id'].tolist(),
                key="quick_request_select"
            )
        
        with col2:
            if st.button("🕒 Mark as Pending", key="request_pending_btn", use_container_width=True):
                update_status("requests", selected_request, "Pending")
        
        with col3:
            if st.button("🔧 Mark as In Progress", key="request_progress_btn", use_container_width=True):
                update_status("requests", selected_request, "In Progress")
        
        with col4:
            if st.button("✅ Mark as Completed", key="request_completed_btn", use_container_width=True):
                update_status("requests", selected_request, "Completed")
        
        st.markdown("---")
        
        # Display requests in editable table format
        display_cols = ['id', 'room_number', 'request_type', 'details', 'status', 'created_at']
        available_cols = [col for col in display_cols if col in df_requests.columns]
        
        st.info("💡 Edit the status directly in the table below and click 'Save Changes' to update")
        
        edited_requests = st.data_editor(
            df_requests[available_cols],
            use_container_width=True,
            hide_index=True,
            disabled=['id', 'room_number', 'request_type', 'details', 'created_at'],
            column_config={
                "id": "Request ID",
                "room_number": "Room",
                "request_type": "Type",
                "details": "Details",
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pending", "In Progress", "Completed"],
                    required=True
                ),
                "created_at": "Created At"
            },
            key="requests_editor"
        )
        
        # Check for changes and update
        if st.button("💾 Save Changes", key="save_requests", use_container_width=False):
            changes_made = False
            for idx in range(len(df_requests)):
                original_status = df_requests.iloc[idx]['status']
                new_status = edited_requests.iloc[idx]['status']
                if original_status != new_status:
                    request_id = df_requests.iloc[idx]['id']
                    update_status("requests", request_id, new_status)
                    changes_made = True
            
            if not changes_made:
                st.info("No changes detected")
        
        # Export button
        st.markdown("---")
        csv = df_requests.to_csv(index=False)
        st.download_button(
            label="📥 Download Requests CSV",
            data=csv,
            file_name=f"requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No service requests found")
