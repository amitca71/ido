import streamlit as st
import random
from gensim.models import KeyedVectors

# 1. Load the tiny model efficiently
@st.cache_resource
def load_model():
    return KeyedVectors.load('tiny_hebrew_fasttext.kv')

with st.spinner("טוען את המילון..."):
    model = load_model()

# 2. Word List
WORDS = [
    "כלב", "חתול", "מחשב", "בית", "עץ",
    "ים", "אהבה", "חבר", "ספר", "מכונית",
    "שמש", "ירח", "מלך", "ילד", "אוכל"
]

# 3. Game State Initialization
def new_game():
    st.session_state.secret_word = random.choice(WORDS)
    st.session_state.guesses = []

if "secret_word" not in st.session_state:
    new_game()

# 4. User Interface
st.title("🎯 משחק ניחוש מילים סמנטי")
st.write("נסה לנחש את המילה שהמחשב בחר. כל ניחוש יקבל ציון קרבה סמנטית (0-100).")

# Using a form so the user can just press "Enter" to submit
with st.form(key="guess_form", clear_on_submit=True):
    user_guess = st.text_input("הכנס ניחוש:")
    submit_button = st.form_submit_button("נחש")

if submit_button:
    if user_guess:
        user_guess = user_guess.strip()
        
        # Check if the word exists in our tiny dictionary
        if user_guess not in model.key_to_index:
            st.error(f"המילה '{user_guess}' לא מוכרת למילון שלנו. נסה מילה נפוצה יותר!")
        
        # Prevent duplicate guesses
        elif any(guess == user_guess for guess, score in st.session_state.guesses):
            st.warning("כבר ניחשת את המילה הזו!")
            
        else:
            # Calculate similarity using Gensim
            similarity = model.similarity(st.session_state.secret_word, user_guess)
            
            # Convert to a 0-100 score (ignoring negative similarities)
            score = max(0, int(similarity * 100))
            
            st.session_state.guesses.append((user_guess, score))

            if user_guess == st.session_state.secret_word:
                st.success(f"🎉 כל הכבוד! ניחשת נכון: {st.session_state.secret_word}")
                st.balloons()
            else:
                st.info(f"📊 המילה '{user_guess}' קיבלה רמת קרבה: {score}")

# 5. Display Guess History
if st.session_state.guesses:
    st.divider()
    st.subheader("📜 היסטוריית ניחושים (מהקרוב לרחוק)")
    
    # Sort guesses by score descending
    sorted_guesses = sorted(st.session_state.guesses, key=lambda x: -x[1])
    
    for guess, score in sorted_guesses:
        # Highlight the winning word if it's in the list
        if score == 100 and guess == st.session_state.secret_word:
            st.success(f"**{guess} - {score}** 🏆")
        else:
            st.write(f"{guess} - {score}")

st.divider()

# 6. Restart Game
if st.button("🔄 משחק חדש"):
    new_game()
    st.rerun()
