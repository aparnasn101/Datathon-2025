
# ------------------------------
# 11) SIDEBAR: RESTOCK RECOMMENDATIONS (SHIPMENT FILE) - robust & formatted
# ------------------------------
import difflib
from textwrap import dedent

def _find_best_match(name, choices):
    """Return best matching key from choices for name (case-insensitive); or None."""
    if name is None:
        return None
    name_l = name.strip().lower()
    choices_l = {c: c.strip().lower() for c in choices}
    # exact match
    for c, c_l in choices_l.items():
        if c_l == name_l:
            return c
    # startswith / contains
    for c, c_l in choices_l.items():
        if name_l in c_l or c_l in name_l:
            return c
    # fuzzy
    close = difflib.get_close_matches(name_l, list(choices_l.values()), n=1, cutoff=0.6)
    if close:
        # find original key
        for c, c_l in choices_l.items():
            if c_l == close[0]:
                return c
    return None

# Ensure shipments DF exists
try:
    shipment_df = shipments.copy()
except Exception as e:
    st.sidebar.error(f"Shipment data not loaded: {e}")
    shipment_df = None

st.sidebar.markdown("---")
st.sidebar.header("📦 Restock Recommendations (from shipments)")

if shipment_df is None or shipment_df.empty:
    st.sidebar.info("No shipment data found. Please ensure 'MSY Data - Shipment.csv' is in the project folder.")
else:
    # normalize shipment column names to friendly keys by substring matching
    cols = {c.lower().strip(): c for c in shipment_df.columns}
    # mapping expected fields (use substring matching)
    def _col(keys):
        for k in keys:
            for low, orig in cols.items():
                if k in low:
                    return orig
        return None

    col_ing = _col(["ingredient", "item", "name"])
    col_qty_per = _col(["quantity per", "quantity", "qty", "quantity per shipment"])
    col_unit = _col(["unit", "unit of", "unit of shipment"])
    col_num_ship = _col(["number of", "num", "number of shipments"])
    col_freq = _col(["frequency", "freq"])
    col_total_received = _col(["total received", "total", "received"])
    col_est_week = _col(["estimated weekly", "estimated weekly supply", "weekly supply", "estimated"])

    # show a small table in the sidebar so user can confirm the shipment file mapping
    st.sidebar.subheader("Shipment file preview")
    display_cols = [c for c in [col_ing, col_qty_per, col_unit, col_num_ship, col_freq, col_total_received, col_est_week] if c]
    if len(display_cols) == 0:
        st.sidebar.error("Shipment file columns could not be auto-detected. Expected columns like: Ingredient, Quantity per shipment, Unit of shipment, Number of shipments, frequency, Total Received, Estimated Weekly Supply")
    else:
        # show first 8 rows
        st.sidebar.dataframe(shipment_df[display_cols].head(8).rename(columns=lambda x: x.strip()), height=240)

        # Normalize frequency into shipments/month (approx)
        freq_map = {
            "weekly": 4,
            "week": 4,
            "biweekly": 2,
            "bi-weekly": 2,
            "bimonthly": 2,
            "monthly": 1,
            "month": 1,
        }

        def _freq_to_per_month(f):
            if pd.isna(f):
                return np.nan
            fs = str(f).strip().lower()
            for k, v in freq_map.items():
                if k in fs:
                    return v
            # numeric fallback: if f is numeric treat as count per month
            try:
                return float(fs)
            except Exception:
                return np.nan

        # Prepare latest usage map from monthly_totals for the selected last_month
        last_month = months_in_data[-1]
        if last_month not in monthly_totals["Month"].values:
            # fallback: take last row of monthly_totals
            current_vals = monthly_totals.iloc[-1][valid_cols]
            shown_last_month = monthly_totals.iloc[-1]["Month"]
        else:
            current_vals = monthly_totals[monthly_totals["Month"] == last_month][valid_cols].iloc[0]
            shown_last_month = last_month

        # Build alerts list
        alerts = []
        # create set of valid ingredients for matching
        valid_ings = list(valid_cols)

        for i, row in shipment_df.iterrows():
            ing_raw = row[col_ing] if col_ing else None
            if pd.isna(ing_raw):
                continue
            ing_raw = str(ing_raw).strip()
            matched = _find_best_match(ing_raw, valid_ings)
            total_received = None
            # pull numbers safely
            if col_total_received and col_total_received in row:
                try:
                    total_received = float(str(row[col_total_received]).replace(',', '').strip())
                except Exception:
                    total_received = np.nan
            # fallback to Estimated Weekly Supply * 4 if no Total Received but estimated weekly exists
            if (pd.isna(total_received) or total_received == 0) and col_est_week and col_est_week in row:
                try:
                    est_week = float(str(row[col_est_week]).replace(',', '').strip())
                    total_received = est_week * 4  # approximate monthly intake
                except Exception:
                    pass
            # If still NaN, skip for numeric calculations but still show info
            if matched is None:
                used = None
            else:
                used = float(current_vals.get(matched, 0))

            freq_raw = row[col_freq] if col_freq else None
            freq_monthly = _freq_to_per_month(freq_raw)

            qty_per = row[col_qty_per] if col_qty_per else None
            unit = row[col_unit] if col_unit else None
            num_ship = row[col_num_ship] if col_num_ship else None

            # compute percent used/remaining
            pct_used = None
            pct_remaining = None
            timing = "Unknown"
            if total_received and total_received > 0 and used is not None:
                pct_used = (used / total_received) * 100
                pct_remaining = max(0.0, 100.0 - pct_used)
                # classify timing (more aggressive thresholds for urgent)
                if pct_used >= 75:
                    timing = "Week 4 (Urgent)"
                elif pct_used >= 50:
                    timing = "Week 3"
                elif pct_used >= 25:
                    timing = "Week 2"
                else:
                    timing = "Sufficient (no immediate restock)"
            # Build human readable recommendation
            rec = ""
            if pct_used is None:
                rec = "No usage data available to compute recommendation."
            else:
                rec = dedent(f"""
                    • Frequency: {freq_raw or 'unknown'} (~{freq_monthly if not pd.isna(freq_monthly) else '?'} shipments/month)
                    • Quantity per shipment: {qty_per or 'unknown'} {unit or ''}
                    • Number of shipments (period): {num_ship or 'unknown'}
                    • Total received (shipment file): {total_received if not pd.isna(total_received) else 'unknown'}
                    • Used this month ({shown_last_month}): {used:.1f}
                    • Percent used: {pct_used:.1f}%
                    • Percent remaining: {pct_remaining:.1f}%
                    • Recommended timing: {timing}
                    • Timestamp: {'third week of the month' if timing == 'Week 3' else ('fourth week' if timing.startswith('Week 4') else ('second week' if timing == 'Week 2' else 'start of month'))}
                """).strip()

            alerts.append({
                "ingredient_raw": ing_raw,
                "matched_ing": matched,
                "pct_used": pct_used,
                "pct_remaining": pct_remaining,
                "rec_text": rec
            })

        # Filter to items that appear to be low-ish (used >= 50% OR explicitly in previously computed low_ingredients)
        compiled = []
        # create quick lookup set for previously low ingredients by name (case-insensitive)
        low_set = set([i.lower() for i in low_ingredients.index]) if 'low_ingredients' in locals() else set()
        for a in alerts:
            add_flag = False
            if a["pct_used"] is not None:
                if a["pct_used"] >= 50:  # used half or more -> consider restock suggestion
                    add_flag = True
            # also include if matched ingredient was flagged earlier as low (<=25% remaining)
            if a["matched_ing"] and a["matched_ing"].lower() in low_set:
                add_flag = True
            if add_flag:
                compiled.append(a)

        if len(compiled) == 0:
            st.sidebar.success("✅ Shipment checks: no strong restock recommendations right now.")
        else:
            st.sidebar.markdown("**Every two weeks, consider restocking the following (based on shipments & monthly usage):**")
            for a in compiled:
                title = a["matched_ing"] if a["matched_ing"] else a["ingredient_raw"]
                st.sidebar.markdown(f"**🔸 {title}**")
                # print recommendation bullet points
                for line in a["rec_text"].split("\n"):
                    st.sidebar.markdown(f"- {line}")
                st.sidebar.markdown("")  # small spacer



