import streamlit as st
from cohere_api import get_medical_response
import re
from datetime import datetime

st.set_page_config(
    page_title="Medical Symptom Checker",
    page_icon="🏥",
    layout="wide"
)

def clean_input(text):
    """Basic input sanitization"""
    return re.sub(r'[^\w\s.,?!-]', '', text).strip()

def main():
    st.title("AI Medical Symptom Checker")
    st.markdown("""
    Describe your symptoms and get AI-powered medical guidance.
    **Remember:** This is not a substitute for professional medical advice.
    """)

    # Initialize session state for history if it doesn't exist
    if 'history' not in st.session_state:
        st.session_state.history = []

    with st.form("symptom_form"):
        user_input = st.text_area(
            "Describe your symptoms:",
            placeholder="e.g. I've had a headache and fever for 3 days...",
            height=150
        )
        submitted = st.form_submit_button("Get Analysis")

    if submitted:
        if not user_input.strip():
            st.warning("Please describe your symptoms")
        else:
            with st.spinner("Analyzing your symptoms..."):
                clean_text = clean_input(user_input)
                response = get_medical_response(clean_text)
            
            # Add to history
            st.session_state.history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'symptoms': clean_text,
                'response': response
            })
            
            st.subheader("Medical Guidance")
            st.markdown("---")
            
            st.markdown(response)
            
            st.markdown("---")
            st.warning("""
            **Important Disclaimer:**  
            This AI assistant provides general health information only.  
            Always consult a qualified healthcare professional for diagnosis and treatment.
            """)

    # Display history section
    st.sidebar.title("History")
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history[::-1]):  # Show most recent first
            with st.sidebar.expander(f"Consultation {i+1} - {entry['timestamp']}"):
                st.markdown(f"**Symptoms:** {entry['symptoms']}")
                st.markdown(f"**Response:** {entry['response']}")
                
                # Add delete button for each entry
                if st.button(f"Delete this entry", key=f"delete_{i}"):
                    del st.session_state.history[len(st.session_state.history) - 1 - i]
                    st.rerun()
        
        # Add clear all button
        if st.sidebar.button("Clear All History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.sidebar.info("No history yet. Your consultations will appear here.")

if __name__ == "__main__":
    main()