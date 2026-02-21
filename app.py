import tkinter as tk
import random

# פונקציה שבוחרת "כן" או "לא" באקראי ומעדכנת את המסך
def get_random_answer():
    answers = ["כן", "לא"]
    result = random.choice(answers)
    label_result.config(text=result)

# יצירת החלון הראשי
root = tk.Tk()
root.title("כן או לא?")
root.geometry("300x200") # גודל החלון

# יצירת הכפתור
button = tk.Button(root, text="לחץ לקבלת תשובה", command=get_random_answer, font=("Arial", 14))
button.pack(pady=30) # מיקום הכפתור עם רווח למעלה ולמטה

# יצירת אזור הטקסט (תווית) בו תופיע התשובה
label_result = tk.Label(root, text="", font=("Arial", 28, "bold"))
label_result.pack(pady=10)

# הפעלת התוכנה והשארת החלון פתוח
root.mainloop()
