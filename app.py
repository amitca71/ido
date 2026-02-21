import streamlit as st
import pickle
import numpy as np
import random

# --- 1. פונקציית חישוב המרחק הסמנטי ---
def cosine_sim(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# --- 2. טעינת מילון הניחושים המלא ---
@st.cache_data
def load_dictionary():
    # שים לב: ודא ששם הקובץ כאן תואם במדויק לשם הקובץ שהורדת מ-Colab!
    # (לדוגמה: "hebrew_embeddings_15k_fixed.pkl" או כל שם אחר ששמרת)
    with open("hebrew_embeddings_everyday.pkl", "rb") as f:
        return pickle.load(f)

with st.spinner("טוען את מילון המשחק..."):
    word_vectors = load_dictionary()
    # ALL_GUESSES מכיל את כל 15,000+ המילים שהשחקן רשאי לנחש
    ALL_GUESSES = list(word_vectors.keys())

# --- 3. רשימת הזהב: מילות היעד הסודיות ---
# מתוך הרשימה הזו *בלבד* המחשב יגריל את מילת הסוד.
# אתה יכול להוסיף לכאן כמה מילים שרק תרצה!
SECRET_TARGET_WORDS = [
    "קנקן", "שולחן", "כלב", "חתול", "בית", "ים", "הר", "מחשב", "אהבה", 
    "עץ", "דג", "אש", "מים", "שמש", "ירח", "כוכב", "רכב", "ילד", "אוכל",
    "לחם", "אדמה", "כיסא", "חלון", "דלת", "שמחה", "חבר", "ספר", "עט", 
    "בוקר", "לילה", "מדינה", "עיר", "רחוב", "משפחה", "אמא", "אבא", "זמן",
    "שבוע", "חודש", "שנה", "חיים", "שלום", "מלחמה", "צבא", "חייל", "רופא",
    "פרח", "ציפור", "שמיים", "ענן", "גשם", "שלג", "רוח", "אור", "חושך",
    "כדור", "משחק", "שיר", "סיפור", "תמונה", "צבע", "כסף", "זהב", "ברזל",
    "מלך", "מלכה", "גיבור", "חכם", "טיפש", "טוב", "רע", "גדול", "קטן", 
    "ארוך", "קצר", "מהיר", "לאט", "חזק", "חלש", "יפה", "מתוק", "מר", "חם", "קר"
]

# מוודאים שכל מילות הסוד שלנו אכן קיימות במילון הגדול, כדי למנוע קריסות
VALID_SECRET_WORDS = [word for word in SECRET_TARGET_WORDS if word in word_vectors]

# --- 4. אתחול ומצב המשחק ---
def new_game():
    # המחשב מגריל מילה רק מהרשימה הנקייה שלנו
    st.session_state.secret_word = random.choice(VALID_SECRET_WORDS)
    st.session_state.guesses = []
    st.session_state.game_over = False

if "secret_word" not in st.session_state:
    new_game()

# --- 5. ממשק המשתמש (UI) ---
st.title("🎯 סמנטל עברי - הגרסה המדויקת")
st.write(f"המודל בחר מילת בסיס אחת מתוך רשימה מוקפדת של {len(VALID_SECRET_WORDS)} מילים. נסה לנחש אותה!")

with st.form(key="guess_form", clear_on_submit=True):
    user_guess = st.text_input("הכנס ניחוש:", disabled=st.session_state.game_over)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submit_button = st.form_submit_button("נחש")

if submit_button and not st.session_state.game_over:
    if user_guess:
        user_guess = user_guess.strip()
        
        # בדיקה 1: האם המילה בכלל קיימת בשפה/במודל הגדול?
        if user_guess not in ALL_GUESSES:
            st.error(f"המילה '{user_guess}' לא מוכרת למילון שלנו. נסה מילה נפוצה יותר.")
        
        # בדיקה 2: האם השחקן כבר ניחש את זה?
        elif any(guess == user_guess for guess, score in st.session_state.guesses):
            st.warning("כבר ניחשת את המילה הזו!")
            
        # חישוב הניחוש!
        else:
            secret_vec = word_vectors[st.session_state.secret_word]
            guess_vec = word_vectors[user_guess]
            
            similarity = cosine_sim(secret_vec, guess_vec)
            score = max(0, int(similarity * 100))
            
            st.session_state.guesses.append((user_guess, score))

            if user_guess == st.session_state.secret_word:
                st.success(f"🎉 מדהים! המילה הסודית היא אכן: {st.session_state.secret_word}")
                st.balloons()
                st.session_state.game_over = True
            else:
                st.info(f"📊 '{user_guess}' קיבלה רמת קרבה: {score}/100")

# --- 6. הצגת היסטוריית ניחושים ---
if st.session_state.guesses:
    st.divider()
    st.subheader("📜 היסטוריית ניחושים (מהקרוב לרחוק)")
    
    sorted_guesses = sorted(st.session_state.guesses, key=lambda x: -x[1])
    
    for guess, score in sorted_guesses:
        if score == 100 and guess == st.session_state.secret_word:
            st.success(f"**{guess} - {score}** 🏆")
        else:
            st.write(f"**{guess}**: {score}/100")
            st.progress(score)

st.divider()

# --- 7. כפתורי שליטה (משחק חדש / גלה לי) ---
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🔄 משחק חדש", use_container_width=True):
        new_game()
        st.rerun()

with col_b:
    if not st.session_state.game_over:
        if st.button("🏳️ התייאשתי, גלה לי", use_container_width=True):
            st.error(f"המילה הסודית הייתה: **{st.session_state.secret_word}**")
            st.session_state.game_over = True
