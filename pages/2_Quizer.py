import streamlit as st



st.title("Select the number of questions you want in the test")
# Single value slider
Number = st.slider("", min_value=0, max_value=25, value=0)

st.title("Choose Difficulty Level")

# Radio buttons for difficulty selection
difficulty = st.radio("Select difficulty level:", ("Easy", "Medium", "Hard"))

# Display the selected option
st.write(f"You selected: {difficulty}")

# Center the button and make it bigger
col1, col2, col3 = st.columns(3)
with col2:
    st.button("GENERATE", key="generate_button", use_container_width=True)
    
# Apply custom CSS to make the button bigger
st.markdown("""
    <style>
    .stButton button#generate_button {
        padding: 10px 20px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)