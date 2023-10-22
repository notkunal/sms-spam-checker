import streamlit as st
import time
import pickle
import pyautogui
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
st.sidebar.image("main_logo.png")

def nlp_preprocess(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    text=y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text=y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

tfid=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))
st.title("SpamGuard")
input_sms=st.text_area("Enter the SMS that you have received")
col1, col2= st.columns([1,1])
with col1:
    if st.button("Predict"):
        if len(input_sms)==0:
                st.warning("Text Box is Empty!!")
        else:
            with st.spinner("In progress...!!"):
                time.sleep(1)
            # 1.Preprocess
            new_text=nlp_preprocess(input_sms)
            # 2.Vectorize
            vector_input=tfid.transform([new_text])
            # 3.Predict
            result = model.predict(vector_input)[0]
            # 4.Display
            if result==1:
                st.error("This is a spam message!!")
            else:
                st.success("This is not a spam message!!")
with col2:
    if st.button(" Reset "):
        pyautogui.hotkey("ctrl","F5")
st.caption("Developed by [Not Kunal :)](https://twitter.com/Not__Kunal)")
st.sidebar.title("Connect me via :")
st.sidebar.header("[X/Twitter](https://twitter.com/Not__Kunal)")
st.sidebar.header("[LinkedIn](https://linkedin.com/in/notkunal)")
st.sidebar.header("[GitHub](https://github.com/notkunal)")
