import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="AI Homework & Quiz Maker", page_icon="📝", layout="centered")

# Title and Subtitle
st.title("📝 AI Homework & Quiz Maker")
st.write("टीचर्स और ट्यूटर्स के लिए 1-क्लिक में टेस्ट पेपर और वर्कशीट बनाने वाला टूल।")

# Sidebar for API Key & Pricing Information
with st.sidebar:
    st.header("🔑 सेटिंग्स")
    api_key = st.text_input("OpenAI API Key दर्ज करें:", type="password")
    
    st.markdown("---")
    st.header("💎 सब्सक्रिप्शन प्लान्स")
    st.write("• **₹29** / 1 महीना")
    st.write("• **₹49** / 2 महीने")
    st.write("• **₹99** / 3 महीने")
    st.write("• **₹1000** / 1 साल")
    st.info("एक्सेस पाने के लिए एडमिन से संपर्क करें।")

# Input Form
with st.form("quiz_form"):
    subject = st.text_input("सब्जेक्ट (Subject):", placeholder="जैसे: Science, Class 8")
    topic = st.text_input("टॉपिक (Topic):", placeholder="जैसे: Crop Production, Force and Pressure")
    grade = st.selectbox("क्लास (Class/Grade):", ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Other"])
    
    num_mcq = st.slider("MCQs (बहुविकल्पीय प्रश्न) की संख्या:", min_value=1, max_value=15, value=5)
    num_short = st.slider("Short Questions (लघु प्रश्न) की संख्या:", min_value=1, max_value=10, value=3)
    include_answers = st.checkbox("उत्तर कुंजी (Answer Key) शामिल करें", value=True)

    submitted = st.form_submit_button("🚀 टेस्ट पेपर जनरेट करें")

# Logic execution
if submitted:
    if not api_key:
        st.error("कृपया बाईं तरफ साइडबार में अपनी OpenAI API Key दर्ज करें।")
    elif not topic:
        st.warning("कृपया टॉपिक का नाम दर्ज करें।")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            prompt = f"""
            You are an expert teacher. Create a test paper/worksheet based on the following requirements:
            - Subject: {subject}
            - Topic: {topic}
            - Grade Level: {grade}
            - Number of Multiple Choice Questions (MCQs): {num_mcq}
            - Number of Short Answer Questions: {num_short}
            - Include Answer Key at the end: {include_answers}
            
            Format the output cleanly using Markdown with clear section headers for Section A (MCQs), Section B (Short Questions), and Answer Key.
            """

            with st.spinner("टेस्ट पेपर तैयार किया जा रहा है..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
            st.success("टेस्ट पेपर सफलतापूर्वक तैयार हो गया!")
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"एक त्रुटि (Error) आई: {str(e)}")
