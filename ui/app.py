import streamlit as st


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
NETWORK ANALYSIS
------------------------------------------------- */

.network-area {
    background-color: #FFFFFF;
    border: 1px dashed #BFAF9E;
    border-radius: 10px;
    padding: 40px;
    text-align: center;
    color: #7A6A5F;
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
        placeholder="Search wallet address or transaction ID...",
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
# ANALYSIS RESULTS
# -------------------------------------------------

if analyze:

    # DASHBOARD TITLE

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
            """
<div class="card">
<div class="card-label">RISK SCORE</div>
<div class="card-value">78%</div>
<div class="card-description">High Risk</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="card">
<div class="card-label">NEAREST VASP</div>
<div class="card-value">Binance</div>
<div class="card-description">Predicted Service Provider</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
<div class="card">
<div class="card-label">GRAPH HOPS</div>
<div class="card-value">3</div>
<div class="card-description">Network Distance</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            """
<div class="card">
<div class="card-label">CONFIDENCE</div>
<div class="card-value">92%</div>
<div class="card-description">Attribution Confidence</div>
</div>
""",
            unsafe_allow_html=True
        )


    # SPACE

    st.markdown("<br>", unsafe_allow_html=True)


    # -------------------------------------------------
    # INVESTIGATION DETAILS + ATTRIBUTION RESULT
    # -------------------------------------------------

    left_col, right_col = st.columns([1.2, 1])


    # INVESTIGATION DETAILS

    with left_col:

        st.markdown(
            '<div class="section-title">Investigation Details</div>',
            unsafe_allow_html=True
        )

        details_html = f"""
<div class="detail-card">
<div class="detail-label">SUBMITTED IDENTIFIER</div>
<div class="detail-value">{wallet_id if wallet_id else "Not provided"}</div>

<div class="detail-label">INVESTIGATION STATUS</div>
<div class="detail-value">Complete</div>

<div class="detail-label">NETWORK</div>
<div class="detail-value">Ethereum</div>
</div>
"""

        st.markdown(
            details_html,
            unsafe_allow_html=True
        )


    # -------------------------------------------------
    # ATTRIBUTION RESULT
    # -------------------------------------------------

    with right_col:

        st.markdown(
            '<div class="section-title">Attribution Result</div>',
            unsafe_allow_html=True
        )

        result_html = """
<div class="result-card">
<div class="result-title">NEAREST IDENTIFIED VASP</div>

<div class="result-value">Binance</div>

<div class="result-description">
The submitted wallet is predicted to be closest to this identified service provider.
</div>
</div>
"""

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )


    # SPACE

    st.markdown("<br>", unsafe_allow_html=True)


    # -------------------------------------------------
    # NETWORK ANALYSIS
    # -------------------------------------------------

    st.markdown(
        '<div class="section-title">Network Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Transaction path and wallet relationship analysis.</div>',
        unsafe_allow_html=True
    )


    network_html = """
<div class="network-area">
<b>Network Visualization</b>
<br><br>
Transaction path and graph visualization will appear here after backend integration.
</div>
"""

    st.markdown(
        network_html,
        unsafe_allow_html=True
    )