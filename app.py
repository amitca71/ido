import streamlit as st
import random
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# טעינת מודל אמבדינג (תומך בעברית)
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()

# רשימת מילים אפשריות
WORDS = [
    "כלב", "חתול", "מחשב", "בית", "עץ",
    "ים", "אהבה", "חבר", "ספר", "מכונית",
    "שמש", "ירח", "מלך", "ילד", "אוכל"
]

# התחלת משחק חדש
def new_game():
    st.session_state.secret_word = random.choice(WORDS)
    st.session_state.guesses = []

if "secret_word" not in st.session_state:
    new_game()

st.title("🎯 משחק ניחוש מילים סמנטי")

st.write("נסה לנחש את המילה שהמחשב בחר. כל ניחוש יקבל ציון קרבה סמנטית (0-100).")

user_guess = st.text_input("הכנס ניחוש:")

if st.button("נחש"):
    if user_guess:
        # חישוב אמבדינג
        secret_embedding = model.encode([st.session_state.secret_word])
        guess_embedding = model.encode([user_guess])

        similarity = cosine_similarity(secret_embedding, guess_embedding)[0][0]
        score = int(similarity * 100)

        st.session_state.guesses.append((user_guess, score))

        if user_guess == st.session_state.secret_word:
            st.success(f"🎉 כל הכבוד! ניחשת נכון: {st.session_state.secret_word}")
        else:
            st.info(f"📊 רמת קרבה: {score}")

# הצגת היסטוריית ניחושים
if st.session_state.guesses:
    st.subheader("📜 היסטוריית ניחושים")
    for guess, score in sorted(st.session_state.guesses, key=lambda x: -x[1]):
        st.write(f"{guess} - {score}")

if st.button("🔄 משחק חדש"):
    new_game()
    st.experimental_rerun() 
