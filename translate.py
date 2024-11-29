import tkinter as tk
from tkinter import messagebox
from deep_translator import GoogleTranslator


progress = {"French": 0, "Spanish": 0}


quiz_data = {
    "French": {
        "cat": "chat",
        "dog": "chien",
        "apple": "pomme",
        "book": "livre",
        "car": "voiture",
        "house": "maison",
        "school": "école",
        "flower": "fleur",
        "water": "eau",

        "tree": "arbre",
    },
    "Spanish": {
        "cat": "gato",
        "dog": "perro",
        "apple": "manzana",
        "book": "libro",
        "car": "coche",
        "house": "casa",
        "school": "escuela",
        "flower": "flor",
        "water": "agua",
        "tree": "árbol",
    },
}


def translate_text():
    input_text = input_box.get("1.0", "end-1c").strip()
    if not input_text:
        messagebox.showerror("Error", "Please enter text to translate.")
        return

    language = lang_var.get()
    target_lang = "fr" if language == "French" else "es" if language == "Spanish" else "en"

    try:
        translated = GoogleTranslator(source="en", target=target_lang).translate(input_text)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")
        return

    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", translated)
    output_box.config(state="disabled")

# Start Quiz
def start_quiz():
    language = lang_var.get()
    if language not in quiz_data:
        messagebox.showerror("Error", "Please select a valid language for the quiz.")
        return
    QuizWindow(language)

# Progress Tracker
def update_progress(language):
    progress[language] += 1
    progress_label.config(
        text=f"French: {progress['French']}/10 | Spanish: {progress['Spanish']}/10"
    )

# Quiz Window
class QuizWindow:
    def __init__(self, language):  # Fixed `__init__`
        self.language = language
        self.questions = list(quiz_data[language].items())
        self.index = 0
        self.score = 0
        self.window = tk.Toplevel(root)
        self.window.title(f"{language} Quiz")
        self.setup_ui()

    def setup_ui(self):
        self.question_label = tk.Label(self.window, text="", font=("Arial", 14))
        self.question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.window, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(
            self.window, text="Submit", command=self.check_answer
        )
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(self.window, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.index < len(self.questions):
            self.question_label.config(
                text=f"Translate to {self.language}: {self.questions[self.index][0]}"
            )
        else:
            self.end_quiz()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.questions[self.index][1]
        if user_answer == correct_answer:
            self.score += 1
            update_progress(self.language)
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(
                text=f"Wrong! Correct answer: {correct_answer}", fg="red"
            )
        self.index += 1
        self.answer_entry.delete(0, "end")
        self.load_question()

    def end_quiz(self):
        self.question_label.config(
            text=f"Quiz Finished! Your score: {self.score}/{len(self.questions)}"
        )
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.feedback_label.pack_forget()

# Main Window
root = tk.Tk()
root.title("Language Learning Bot")
root.geometry("500x500")

# GUI Elements
tk.Label(root, text="Language Learning Bot", font=("Arial", 20)).pack(pady=10)

tk.Label(root, text="Enter text to translate:", font=("Arial", 14)).pack(pady=5)
input_box = tk.Text(root, height=5, width=50)
input_box.pack(pady=5)

tk.Label(root, text="Select language:", font=("Arial", 14)).pack(pady=5)
lang_var = tk.StringVar(value="French")
lang_menu = tk.OptionMenu(root, lang_var, "French", "Spanish")
lang_menu.pack(pady=5)

tk.Button(root, text="Translate", command=translate_text).pack(pady=10)

tk.Label(root, text="Translated text:", font=("Arial", 14)).pack(pady=5)
output_box = tk.Text(root, height=5, width=50, state="disabled")
output_box.pack(pady=5)

tk.Button(root, text="Start Quiz", command=start_quiz).pack(pady=10)

progress_label = tk.Label(
    root, text=f"French: {progress['French']}/10 | Spanish: {progress['Spanish']}/10", font=("Arial", 14)
)
progress_label.pack(pady=10)

# Run the App
root.mainloop()
