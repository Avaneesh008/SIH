import os
import requests
import streamlit as st

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
API_BASE_URL = os.getenv("BACKEND_API_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="TRACE",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

header {
    visibility: hidden;
}

/* MAIN PAGE */
.stApp {
    background-color: #F8F4EE;
    color: #2E251F;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* -------------------------------------------------
LOGO
------------------------------------------------- */
.trace-logo {
    font-size: 2.5rem;
    font-weight: 750;
    letter-spacing: 1px;
    color: #3D2B1F;
    line-height: 1;
}

.trace-dot {
    color: #8B6B52;
}

.trace-subtitle {
    font-size: 0.75rem;
    color: #7A6A5F;
    margin-top: 6px;
    white-space: nowrap;
}

/* -------------------------------------------------
SEARCH BAR
------------------------------------------------- */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #2E251F !important;
    border: 1px solid #D8CCBE !important;
    border-radius: 8px !important;
    height: 46px;
    font-size: 0.95rem;
}

.stTextInput input:focus {
    border: 1px solid #8B6B52 !important;
    box-shadow: none !important;
}

/* -------------------------------------------------
BUTTON
------------------------------------------------- */
.stButton button {
    background-color: #4A3728 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    height: 46px;
    font-weight: 500;
}

.stButton button:hover {
    background-color: #634B38 !important;
    color: #FFFFFF !important;
}

/* -------------------------------------------------
SECTION TITLES
------------------------------------------------- */
.section-title {
    font-size: 1.55rem;
    font-weight: 650;
    color: #3D2B1F;
    margin-bottom: 0.4rem;
}

.section-subtitle {
    font-size: 0.9rem;
    color: #7A6A5F;
    margin-bottom: 1.2rem;
}

/* -------------------------------------------------
SUMMARY CARDS
------------------------------------------------- */
.card {
    background-color: #FFFFFF;
    border: 1px solid #DED3C7;
    border-radius: 10px;
    padding: 20px;
    min-height: 130px;
}

.card-label {
    color: #7A6A5F;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.card-value {
    color: #3D2B1F;
    font-size: 1.7rem;
    font-weight: 650;
    margin-top: 12px;
}

.card-description {
    color: #8B6B52;
    font-size: 0.82rem;
    margin-top: 6px;
}

.badge-illicit {
    color: #B91C1C;
    font-weight: 600;
}

.badge-licit {
    color: #15803D;
    font-weight: 600;
}

.badge-uncertain {
    color: #B45309;
    font-weight: 600;
}

/* -------------------------------------------------
DETAIL CARD
------------------------------------------------- */
.detail-card {
    background-color: #FFFFFF;
    border: 1px solid #DED3C7;
    border-radius: 10px;
    padding: 22px;
}

.detail-label {
    font-size: 0.75rem;
    color: #7A6A5F;
    font-weight: 600;
    letter-spacing: 0.8px;
}

.detail-value {
    font-size: 1rem;
    color: #3D2B1F;
    margin-top: 5px;
    margin-bottom: 18px;
    word-break: break-all;
}

/* -------------------------------------------------
ATTRIBUTION RESULT
------------------------------------------------- */
.result-card {
    background-color: #FFFFFF;
    border: 1px solid #BFAF9E;
    border-radius: 10px;
    padding: 24px;
}

.result-title {
    color: #7A6A5F;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.result-value {
    color: #3D2B1F;
    font-size: 2rem;
    font-weight: 650;
    margin-top: 10px;
}

.result-description {
    color: #7A6A5F;
    font-size: 0.9rem;
    margin-top: 8px;
}

/* -------------------------------------------------
NETWORK ANALYSIS & TAGS
------------------------------------------------- */
.network-area {
    background-color: #FFFFFF;
    border: 1px dashed #BFAF9E;
    border-radius: 10px;
    padding: 24px;
    text-align: left;
    color: #3D2B1F;
}

.feature-tag {
    display: inline-block;
    background-color: #F1ECE4;
    color: #4A3728;
    border: 1px solid #D8CCBE;
    padding: 6px 12px;
    border-radius: 6px;
    margin: 4px 6px 4px 0;
    font-size: 0.85rem;
    font-family: monospace;
}

.error-banner {
    background-color: #FEF2F2;
    border: 1px solid #F87171;
    color: #991B1B;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# TOP HEADER
# -------------------------------------------------

logo_col, search_col, button_col = st.columns([2, 7, 1.5])

# LOGO
with logo_col:
    st.markdown(
        '<div class="trace-logo">TRACE<span class="trace-dot">.</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="trace-subtitle">Blockchain Intelligence Workspace</div>',
        unsafe_allow_html=True
    )

# SEARCH BAR
with search_col:
    wallet_id = st.text_input(
        "Search Wallet",
        placeholder="Search wallet address or transaction ID (e.g. 230425980 or 0xd90e...)...",
        label_visibility="collapsed"
    )

# ANALYZE BUTTON
with button_col:
    analyze = st.button(
        "Analyze",
        use_container_width=True
    )


# -------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------

st.divider()


# -------------------------------------------------
# EMPTY STATE
# -------------------------------------------------

if not analyze:
    st.markdown(
        '<div class="section-title">Analysis Dashboard</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Search for a wallet or transaction to begin an investigation.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        """
<div class="detail-card">
<div class="detail-label">READY FOR INVESTIGATION</div>
<div class="detail-value">
Enter a wallet address or transaction ID using the search bar above.
</div>
</div>
""",
        unsafe_allow_html=True
    )


# -------------------------------------------------
# ANALYSIS EXECUTION & RESULTS
# -------------------------------------------------

if analyze:
    clean_id = wallet_id.strip() if wallet_id else ""

    if not clean_id:
        st.warning("Please enter a valid wallet address or transaction ID in the search bar.")
    else:
        # Fetch score from FastAPI Backend
        api_url = f"{API_BASE_URL}/score/{clean_id}"
        response_data = None
        error_message = None

        try:
            res = requests.get(api_url, timeout=10)
            if res.status_code == 200:
                response_data = res.json()
            elif res.status_code == 404:
                error_detail = res.json().get("detail", f"Wallet ID '{clean_id}' not found in dataset.")
                error_message = f"**Wallet Not Found (404):** {error_detail}"
            elif res.status_code == 500:
                error_detail = res.json().get("detail", "Internal server error occurred.")
                error_message = f"**Backend Server Error (500):** {error_detail}"
            else:
                error_message = f"**API Error ({res.status_code}):** {res.text}"
        except requests.exceptions.ConnectionError:
            error_message = f"**Connection Error:** Unable to connect to the backend service at `{API_BASE_URL}`. Please verify that the FastAPI backend is running."
        except requests.exceptions.Timeout:
            error_message = f"**Request Timeout:** The backend at `{API_BASE_URL}` took too long to respond."
        except Exception as e:
            error_message = f"**Unexpected Error:** {str(e)}"

        if error_message:
            st.markdown(f'<div class="error-banner">{error_message}</div>', unsafe_allow_html=True)
        elif response_data:
            # Extract fields aligning exactly with CONTRACT.md
            res_wallet = response_data.get("wallet_address", clean_id)
            res_score = response_data.get("risk_score", 0.0)
            res_label = str(response_data.get("risk_label", "uncertain")).lower()
            res_hops = response_data.get("graph_hops_to_nearest_vasp")
            res_vasp = response_data.get("nearest_vasp_name", "unidentified")
            res_conf = str(response_data.get("attribution_confidence", "low")).capitalize()
            res_features = response_data.get("top_features", [])

            # Formatting
            score_percent = f"{float(res_score) * 100:.1f}%"
            hops_display = str(res_hops) if res_hops is not None else "N/A"
            label_display = res_label.capitalize()
            badge_class = f"badge-{res_label}" if res_label in ["illicit", "licit", "uncertain"] else "badge-uncertain"

            st.markdown(
                '<div class="section-title">Analysis Dashboard</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="section-subtitle">Investigation results for the submitted identifier.</div>',
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # SUMMARY CARDS
            # -------------------------------------------------
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f"""
<div class="card">
<div class="card-label">RISK SCORE</div>
<div class="card-value">{score_percent}</div>
<div class="card-description <span class='{badge_class}'>{label_display} Risk</span></div>
</div>
""",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
<div class="card">
<div class="card-label">NEAREST VASP</div>
<div class="card-value">{res_vasp}</div>
<div class="card-description">Attributed Entity</div>
</div>
""",
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f"""
<div class="card">
<div class="card-label">GRAPH HOPS</div>
<div class="card-value">{hops_display}</div>
<div class="card-description">Network Distance</div>
</div>
""",
                    unsafe_allow_html=True
                )

            with col4:
                st.markdown(
                    f"""
<div class="card">
<div class="card-label">CONFIDENCE</div>
<div class="card-value">{res_conf}</div>
<div class="card-description">Attribution Certainty</div>
</div>
""",
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # -------------------------------------------------
            # INVESTIGATION DETAILS + ATTRIBUTION RESULT
            # -------------------------------------------------
            left_col, right_col = st.columns([1.2, 1])

            with left_col:
                st.markdown(
                    '<div class="section-title">Investigation Details</div>',
                    unsafe_allow_html=True
                )
                details_html = f"""
<div class="detail-card">
<div class="detail-label">SUBMITTED IDENTIFIER</div>
<div class="detail-value">{res_wallet}</div>

<div class="detail-label">RISK CLASSIFICATION</div>
<div class="detail-value"><span class="{badge_class}">{label_display} ({score_percent})</span></div>

<div class="detail-label">INVESTIGATION STATUS</div>
<div class="detail-value">Complete — Scored & Attributed</div>
</div>
"""
                st.markdown(details_html, unsafe_allow_html=True)

            with right_col:
                st.markdown(
                    '<div class="section-title">Attribution Result</div>',
                    unsafe_allow_html=True
                )
                result_html = f"""
<div class="result-card">
<div class="result-title">NEAREST IDENTIFIED VASP</div>
<div class="result-value">{res_vasp}</div>
<div class="result-description">
The queried wallet is <b>{hops_display}</b> hop(s) away from <b>{res_vasp}</b> with <b>{res_conf.lower()}</b> confidence.
</div>
</div>
"""
                st.markdown(result_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # -------------------------------------------------
            # TOP INFLUENCING FEATURES & NETWORK ANALYSIS
            # -------------------------------------------------
            st.markdown(
                '<div class="section-title">Top Influencing Features & Network Analysis</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="section-subtitle">Model feature importances and topological relationship summary.</div>',
                unsafe_allow_html=True
            )

            tags_html = "".join([f'<span class="feature-tag">{feat}</span>' for feat in res_features]) if res_features else "<em>No feature weights available</em>"

            network_html = f"""
<div class="network-area">
<div style="font-weight: 600; margin-bottom: 8px; color: #3D2B1F;">Key Behavioral & Graph Features:</div>
<div style="margin-bottom: 18px;">
{tags_html}
</div>
<div style="font-weight: 600; margin-bottom: 6px; color: #3D2B1F;">Topological Path Summary:</div>
<div style="font-size: 0.9rem; color: #7A6A5F; line-height: 1.5;">
Target Node <code>{res_wallet}</code> ➔ Shortest BFS Graph Distance: <b>{hops_display} hops</b> to known entity <b>{res_vasp}</b> (Certainty: <b>{res_conf}</b>).
</div>
</div>
"""
            st.markdown(network_html, unsafe_allow_html=True)