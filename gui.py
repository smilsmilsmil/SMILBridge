import customtkinter as ctk
import json
import random
# gui.py - A simple GUI application using CustomTkinter for a quiz interface
class quiz_app(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SMILBridge")
        self.geometry("400x400")
        ctk.set_appearance_mode("dark")

        # Prepare frames (defined ONCE)
        self.menu_frame = ctk.CTkFrame(self)
        self.quiz_frame = ctk.CTkFrame(self)
        self.frame = ctk.CTkFrame(self, width=150, height=150, corner_radius=10)

        self.option_buttons = []  # keep this here
        self.initial_menu()

    def initial_menu(self):
        self.clear_frames()
        self.menu_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.menu_frame, text="bridgeproject01", font=("Helvetica", 24))
        title.pack(pady=20)

        start_btn = ctk.CTkButton(self.menu_frame, text="Show Menu", command=self.show_menu)
        start_btn.pack(pady=10)

    def show_menu(self):
        self.clear_frames()
        self.menu_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.menu_frame, text="Welcome to the Flashcard!", font=("Helvetica", 24))
        title.pack(pady=20)

        play_btn = ctk.CTkButton(self.menu_frame, text="Start Quiz", command=self.start_quiz)
        play_btn.pack(pady=10)
        bestscore_btn = ctk.CTkButton(self.menu_frame, text="Best Score", command=self.show_best_score)
        bestscore_btn.pack(pady=20)

    def show_best_score(self):
        # Bestscore menu
        self.clear_frames()
        self.frame.pack(fill="both", expand=True)

        titlescore = ctk.CTkLabel(self.frame, text="Current Bestscore", font=("Helvetica", 24))
        titlescore.pack(pady=10)

        with open("questions.json", "r") as f:
            data = json.load(f)
            bestscore = data.get("bestscores",[{
                "currentbest":0,
                "currentbestname":"none"
            }])
            score_data_name = bestscore[0].get("currentbestname","None")
            score_data = bestscore[0].get("currentbest", 0)


        scoreLabel = ctk.CTkLabel(self.frame, text=f"{score_data} by {score_data_name}", font=("Helvetica", 30), text_color=("#0999FF"))
        scoreLabel.pack(side="top",pady=10)
        reset_btn = ctk.CTkButton(self.frame, text="Reset Best Score", command=self.reset_best_score)
        reset_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self.frame, text="Back to Menu", command=self.show_menu)
        back_btn.pack(side="bottom", pady=10)

    def reset_best_score(self):
        # Read the file and overwrite here
        with open("questions.json", "r") as f:
            data = json.load(f)
        data["bestscores"] = [{
            "currentbest": 0,
            "currentbestname": "None"
        }]
        with open("questions.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Best scores have been reset.")

    def start_quiz(self):
        # Load and shuffle quiz
        with open("questions.json", "r") as file:
            self.questions_list = json.load(file)["quiz_questions"]
        random.shuffle(self.questions_list)

        self.current_index = 0
        self.current_score = 0
        self.show_question()

    def show_question(self):
        
        self.clear_frames()
        self.quiz_frame.pack(fill="both", expand=True)

        question_data = self.questions_list[self.current_index]
        question_label = ctk.CTkLabel(self.quiz_frame, text=question_data["question"], font=("Arial", 16))
        question_label.pack(pady=1)
  
        for opt in question_data["options"]:
            btn = ctk.CTkButton(self.quiz_frame, text=opt, command=lambda opt=opt: self.check_answer(opt))
            btn.pack(pady=2)
        

    def check_answer(self, selected_option):
        correct = self.questions_list[self.current_index]["answer"]
        self.current_index += 1
        if selected_option == correct:
            self.show_result("✅ Correct!")
            self.current_score += 1
        else:
            self.show_result("❌ Incorrect!")

    def next_question(self):
            self.clear_frames()
            self.show_question()

    def show_result(self, message):
        result_label = ctk.CTkLabel(self.quiz_frame, text=message, font=("Helvetica", 16))
        result_label.pack(pady=10)

        if self.current_index < len(self.questions_list):
            next_btn = ctk.CTkButton(self.quiz_frame, text="Next Question", command=self.next_question)
            next_btn.pack(pady=10)
        elif self.current_index == len(self.questions_list):
            done_btn = ctk.CTkButton(self.quiz_frame, text="Finish Quiz", command=self.score_check)
            done_btn.pack(pady=10)

    def score_check(self):
        self.clear_frames()

        # show the result screen
        self.frame.pack(fill="both", expand=True)
        with open("questions.json", "r") as f:
            current_bestscore = json.load(f)["bestscores"][0]["currentbest"]
            current_bestscore = int(current_bestscore)
        
        if self.current_score > current_bestscore:
            print("yes")
            congrats_title = ctk.CTkLabel(
                self.frame, 
                text=f"Congratulation! You just got the new bestscore : {self.current_score}!!",
                font=("Helvetica", 16)
                )
            congrats_title.pack(pady=10)

            self.input_name = ctk.CTkEntry(self.frame, placeholder_text="Enter your name")
            self.input_name.pack(pady=10)

            record = ctk.CTkButton(self.frame, text="Save", command=lambda: (self.record_score(), self.clear_frames(), self.show_menu()))
            record.pack(pady=10)



        else:
            no_label = ctk.CTkLabel(
                self.frame,
                text=f"Your score is {self.current_score}. Better luck next time!",
                font=("Helvetica", 16)
                )
            no_label.pack(pady=10)

    def record_score(self):
        with open("questions.json", "r") as f:
            data = json.load(f)
            bestscores = data.get("bestscores", [
                {
                    "currentbest" : 0,
                    "currentbestname": "None"
                }
            ])
            name_value = self.input_name.get().strip().title()
            bestscores[0]["currentbest"] = self.current_score
            bestscores[0]["currentbestname"] = name_value
            data["bestscores"] = bestscores

        with open("questions.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def clear_frames(self):
        for frame in (self.menu_frame, self.quiz_frame, self.frame):
            frame.pack_forget()
            for widget in frame.winfo_children():
                widget.destroy()