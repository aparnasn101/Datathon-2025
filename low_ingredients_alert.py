# ------------------------------
# 10) SIDEBAR: INGREDIENTS RUNNING LOW + DETAILED RESTOCK RECOMMENDATIONS
# ------------------------------
import datetime
st.sidebar.header("⚠️ Ingredients Running Low")

# Timestamp of check
today = datetime.datetime.now()
st.sidebar.markdown(f"📅 **Status checked:** {today.strftime('%B %d, %Y')}")

if len(valid_cols) == 0:
    st.sidebar.info("No valid ingredients available to check.")
else:
    last_month = months_in_data[-1]
    current_data = monthly_totals[monthly_totals["Month"] == last_month]

    max_per_ing = monthly_totals[valid_cols].max()
    current_vals = current_data[valid_cols].iloc[0]
    percent_remaining = (current_vals / max_per_ing) * 100
    low_ingredients = percent_remaining[percent_remaining <= 25]

    if low_ingredients.empty:
        st.sidebar.success("✅ No ingredients currently running low!")
    else:
        st.sidebar.warning(f"{len(low_ingredients)} ingredients running low.")
        
        # Bar chart
        fig_low, ax_low = plt.subplots(figsize=(5, len(low_ingredients) * 0.4))
        ax_low.barh(low_ingredients.index, low_ingredients.values, color="salmon")
        ax_low.set_xlabel("% Remaining")
        ax_low.set_title(f"Ingredients Running Low - {last_month}")
        plt.tight_layout()
        st.sidebar.pyplot(fig_low)

        # ------------------------------------
        # Shipment-based details per ingredient
        # ------------------------------------
        st.sidebar.markdown("### 📦 Detailed Restock Insights")

        shipments.columns = [c.strip().lower().replace(" ", "_") for c in shipments.columns]

        for ing, pct in low_ingredients.items():
            st.sidebar.markdown(f"#### 🧂 {ing}")
            match = shipments[shipments["ingredient"].str.lower().str.contains(ing.lower(), na=False)]

            if not match.empty:
                row = match.iloc[0]
                freq = str(row.get("frequency", "Unknown")).capitalize()
                qty = row.get("quantity_per_shipment", "Unknown")
                unit = row.get("unit_of_shipment", "")
                est_supply = row.get("estimated_weekly_supply", "Unknown")
                total_recv = row.get("total_received", "Unknown")

                # Interpret timing and alert intensity
                if pct <= 10:
                    urgency = "🚨 Critically low – immediate restock needed!"
                    suggestion = "Contact supplier ASAP or pull from backup stock."
                    week = "Final week of the month"
                elif pct <= 20:
                    urgency = "⚠️ Low supply detected."
                    suggestion = "Restock during the third week to avoid shortages."
                    week = "Third week of the month"
                else:
                    urgency = "⚠️ Below ideal threshold."
                    suggestion = "Monitor daily and prepare restock order."
                    week = "Second week of the month"

                # Smart frequency note
                if "biweek" in freq.lower():
                    freq_note = "Delivered twice per month (every 2 weeks)."
                elif "week" in freq.lower():
                    freq_note = "Delivered weekly."
                elif "month" in freq.lower():
                    freq_note = "Delivered monthly."
                else:
                    freq_note = "Delivery schedule not specified."

                # Rich bullet point summary
                st.sidebar.markdown(f"""
                • **Status:** {urgency}  
                • **Frequency:** {freq_note}  
                • **Quantity per shipment:** {qty} {unit}  
                • **Total received per cycle:** {total_recv} {unit}  
                • **Estimated weekly supply:** {est_supply}  
                • **Stock level:** {pct:.1f}% of normal usage remaining  
                • **Suggested restock timing:** {week}  
                • **Action:** {suggestion}
                """)

            else:
                st.sidebar.markdown(f"""
                • No shipment data found for **{ing}**.  
                • Review manually and verify supplier frequency.  
                • Recommended: Add entry to `shipmentfile.csv` for tracking.
                """)

        st.sidebar.markdown("---")
        st.sidebar.caption("🔄 Data synced from shipmentfile.csv and monthly usage patterns.")




