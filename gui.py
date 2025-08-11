import customtkinter as ctk
import json
import random
# gui.py - A simple GUI application using CustomTkinter for a quiz interface
class quiz_app(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SMILBridge")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")

        # Create frames
        self.menu_frame = ctk.CTkFrame(self)
        self.quiz_frame = ctk.CTkFrame(self)

        self.show_menu()

    def show_menu(self):
        self.clear_frames()
        self.menu_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.menu_frame, text="SMILBridge Quiz", font=("Helvetica", 24))
        title.pack(pady=20)

        start_btn = ctk.CTkButton(self.menu_frame, text="Start Quiz", command=self.start_quiz)
        start_btn.pack(pady=10)

    def start_quiz(self):
        # LOAD AND SHUFFLE QUIZ HERE
        with open("questions.json", "r") as file:
            self.questions_list = json.load(file)["quiz_questions"]
        random.shuffle(self.questions_list)

        self.current_index = 0
        self.show_question()

    def show_question(self):
        
        self.clear_frames()
        self.quiz_frame.pack(fill="both", expand=True)

        question_data = self.questions_list[self.current_index]
        question_label = ctk.CTkLabel(self.quiz_frame, text=question_data["question"], font=("Arial", 16))
        question_label.pack(pady=20)

        self.option_buttons.clear()
  
        for opt in question_data["options"]:
            btn = ctk.CTkButton(self.quiz_frame, text=opt, command=lambda opt=opt: self.check_answer(opt))
            btn.pack(pady=2)
            self.option_buttons.append(btn)
        

    def check_answer(self, selected_option):
        correct = self.questions_list[self.current_index]["answer"]
        if selected_option == correct:
            self.show_result("✅ Correct!")
        else:
            self.show_result("❌ Incorrect!")

    def next_question(self):
    
        self.current_index += 1
        if self.current_index < len(self.questions_list):
            self.show_question()
        elif self.current_index == len(self.questions_list):
            self.clear_frames()
            done_label = ctk.CTkLabel(self.quiz_frame, text="Quiz Finished!", font=("Helvetica", 16))
            done_label.pack(pady=20)
            back_btn = ctk.CTkButton(self.quiz_frame, text="Back to Menu", command=self.show_menu)
            back_btn.pack(pady=10)
            self.quiz_frame.pack_forget()

    def show_result(self, message):
        result_label = ctk.CTkLabel(self.quiz_frame, text=message, font=("Helvetica", 16))
        result_label.pack(pady=10)
        next_btn = ctk.CTkButton(self.quiz_frame, text="Next Question", command=self.next_question)
        next_btn.pack(pady=10)

    def clear_frames(self):
        for frame in (self.menu_frame, self.quiz_frame):
            frame.pack_forget()
            for widget in frame.winfo_children():
                widget.destroy()

        self.questions_label = ctk.CTkLabel(self.quiz_frame, text="", font=("Arial", 16))
        self.questions_label.pack(pady=20)

        self.option_buttons = []