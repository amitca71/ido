import streamlit as st
import random

# כותרת לאפליקציה
st.title("מחולל 'כן' או 'לא' אקראי")

st.write("לחץ על הכפתור כדי לקבל החלטה:")

# יצירת כפתור
if st.button('לחץ כאן לתשובה'):
    # בחירה אקראית
    תשובה = random.choice(["כן", "לא"])
    
    # הצגת התשובה בעיצוב בולט
    if תשובה == "כן":
        st.success(f"התשובה היא: {תשובה} ✅")
    else:
        st.error(f"התשובה היא: {תשובה} ❌")
