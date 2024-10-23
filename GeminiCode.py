import os
import re
from collections import Counter
import tkinter as tk
from tkinter import messagebox

class LanguageDetector:
    def __init__(self, languages_folder):
        self.language_profiles = self.load_language_profiles(languages_folder)

    def load_language_profiles(self, folder):
        profiles = {}
        for filename in os.listdir(folder):
            if filename.endswith('.txt'):
                language = filename[:-4]  # Remove the .txt extension
                with open(os.path.join(folder, filename), 'r', encoding='utf-8') as file:
                    words = {line.strip().lower() for line in file if line.strip()}
                    profiles[language] = words
        return profiles

    def clean_text(self, text):
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text)
        return text.lower()

    def detect_language(self, text):
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()

        # Count word frequencies
        word_count = Counter(words)

        # Score each language based on the presence of known words
        language_scores = {language: 0 for language in self.language_profiles.keys()}
        for language, known_words in self.language_profiles.items():
            for word in words:
                if word in known_words:
                    language_scores[language] += word_count[word]

        # Determine the language with the highest score
        detected_language = max(language_scores, key=language_scores.get)
        return detected_language


# Function to create the enhanced GUI with clear button and hover effect
def create_gui():
    # Function to handle language detection on button click
    def detect_language_gui():
        sentence = entry.get()  # Get the input from user
        if sentence:
            detected_language = detector.detect_language(sentence)
            result_label.config(text=f"Detected Language: {detected_language}")
        else:
            messagebox.showerror("Input Error", "Please enter a sentence!")

    # Function to clear the entry and result label
    def clear_text():
        entry.delete(0, tk.END)  # Clear the input field
        result_label.config(text="")  # Clear the result label

    # Hover effect function to create glow on hover
    def on_enter(e):
        e.widget['background'] = '#45a049'  # Change to lighter green on hover

    def on_leave(e):
        e.widget['background'] = '#4CAF50'  # Revert back to original color

    # Create the main window
    window = tk.Tk()
    window.title("Language Detector")
    window.geometry("500x350")
    window.configure(bg="#f7f7f7")  # Light gray background for a modern look

    # Create a frame for centering content
    frame = tk.Frame(window, bg="#f7f7f7")
    frame.pack(pady=20, padx=20)

    # Add a title label with custom styling
    title_label = tk.Label(
        frame, text="Language Detection App", font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#333333"
    )
    title_label.pack(pady=10)

    # Add label and entry for input sentence with styling
    label = tk.Label(frame, text="Enter a sentence:", font=("Arial", 12), bg="#f7f7f7", fg="#333333")
    label.pack(pady=10)

    entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=2, relief="solid")
    entry.pack(pady=10)

    # Add a styled button to detect language
    detect_button = tk.Button(
        frame, text="Detect Language", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", 
        command=detect_language_gui
    )
    detect_button.pack(pady=10)

    # Add a clear button to reset the input and result
    clear_button = tk.Button(
        frame, text="Clear", font=("Arial", 12, "bold"), bg="#f44336", fg="white", relief="flat", 
        command=clear_text
    )
    clear_button.pack(pady=10)

    # Label to display the result with custom font and spacing
    result_label = tk.Label(frame, text="", font=("Arial", 14, "bold"), bg="#f7f7f7", fg="#333333")
    result_label.pack(pady=10)

    # Apply hover effects to buttons (detect and clear)
    detect_button.bind("<Enter>", on_enter)
    detect_button.bind("<Leave>", on_leave)

    clear_button.bind("<Enter>", lambda e: e.widget.config(background="#e53935"))
    clear_button.bind("<Leave>", lambda e: e.widget.config(background="#f44336"))

    # Run the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    # Set the folder path containing your language dictionaries
    folder_path = './dictionaries'
    detector = LanguageDetector(folder_path)

    # Start the GUI
    create_gui()
