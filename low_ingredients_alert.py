# ------------------------------
# 11) SIDEBAR: MONTHLY REVIEWS (May–October)
# ------------------------------
st.sidebar.markdown("---")
st.sidebar.header("📅 Shipment Monthly Reviews")

try:
    st.sidebar.dataframe(shipments)
    
    # Normalize column names to handle variations
    shipments.columns = shipments.columns.str.strip().str.lower()

    months = ["May", "June", "July", "August", "September", "October"]

    for month in months:
        st.sidebar.subheader(f"Monthly Review: {month}")
        st.sidebar.markdown(f"**Start Date:** {month} 1, 2025")

        for _, row in shipments.iterrows():
            ingredient = row.get("ingredient", "Unknown Ingredient")
            freq = str(row.get("frequency", "unknown")).lower()
            qty = row.get("quantity per shipment", "N/A")
            unit = row.get("unit of shipment", "")
            total = row.get("total received", "N/A")
            est_weekly = row.get("estimated weekly supply", "N/A")

            # Determine restock interval (approximate days)
            if "week" in freq:
                interval = 7
            elif "biweek" in freq:
                interval = 14
            elif "month" in freq:
                interval = 30
            else:
                interval = 14  # fallback

            restock_date = pd.to_datetime(f"2025-{month}-01", errors="coerce") + pd.Timedelta(days=interval)
            restock_str = restock_date.strftime("%B %d, %Y")

            st.sidebar.markdown(f"""
            • **{ingredient}**
                - Restocked **{freq}**
                - Next restock due **{restock_str}**
                - Shipment size: **{qty} {unit}**
                - Estimated weekly supply: **{est_weekly} units**
                - Total received this cycle: **{total}**
            """)

        st.sidebar.markdown("---")

except Exception as e:
    st.sidebar.error(f"Error generating shipment review: {e}")




