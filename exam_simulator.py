import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
import random
import time
import sqlite3
from datetime import datetime
import os

# Configurazione Iniziale CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DatabaseManager:
    def __init__(self, db_name="exam_history.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                score INTEGER,
                total INTEGER,
                percentage REAL,
                passed INTEGER
            )
        ''')
        self.conn.commit()

    def add_record(self, score, total, percentage, passed):
        cursor = self.conn.cursor()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO history (date, score, total, percentage, passed) VALUES (?, ?, ?, ?, ?)",
                       (date_str, score, total, percentage, 1 if passed else 0))
        self.conn.commit()

    def get_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, score, total, percentage, passed FROM history ORDER BY id DESC LIMIT 50")
        return cursor.fetchall()

class ExamSimulatorV3(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Exam Simulator v3.0 - Professional Edition")
        self.geometry("1100x750")
        
        # Dati
        self.db_manager = DatabaseManager()
        self.questions_db = []
        self.filtered_questions = []
        self.current_question_index = 0
        self.score = 0
        self.wrong_questions = []
        self.user_answers = {}
        self.exam_start_time = 0
        self.timer_running = False
        self.chapters_found = set()
        self.selected_chapters = []
        
        # Editor
        self.editor_questions_buffer = []

        # Layout Principale a Schede
        self.tabview = ctk.CTkTabview(self, width=1000, height=650)
        self.tabview.pack(padx=20, pady=(10, 0), fill="both", expand=True)

        self.tab_home = self.tabview.add("🏠 Home")
        self.tab_exam = self.tabview.add("📝 Esame")
        self.tab_editor = self.tabview.add("🛠 Editor & Export")
        self.tab_stats = self.tabview.add("📊 Storico")

        self.setup_home_tab()
        self.setup_exam_tab()
        self.setup_editor_tab()
        self.setup_stats_tab()
        
        # --- FOOTER CREDITS ---
        self.credit_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.credit_frame.pack(side="bottom", fill="x", padx=20, pady=5)
        
        self.lbl_credits = ctk.CTkLabel(
            self.credit_frame, 
            text="Developed by David Aulicino - Version 3.0", 
            font=("Arial", 11, "italic"),
            text_color="gray"
        )
        self.lbl_credits.pack(side="right")
        
        self.tabview.set("🏠 Home")

    # --- TAB HOME ---
    def setup_home_tab(self):
        frame_left = ctk.CTkFrame(self.tab_home, width=300)
        frame_left.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(frame_left, text="Configurazione", font=("Arial", 20, "bold")).pack(pady=10)

        self.btn_load = ctk.CTkButton(frame_left, text="📂 Carica Database (JSON/CSV)", command=self.load_database)
        self.btn_load.pack(pady=10, padx=10, fill="x")

        self.switch_mode = ctk.CTkSwitch(frame_left, text="Modalità Esame (No Feedback)")
        self.switch_mode.pack(pady=10, padx=10, anchor="w")
        
        self.switch_timer = ctk.CTkSwitch(frame_left, text="Abilita Timer (90 min)")
        self.switch_timer.select()
        self.switch_timer.pack(pady=10, padx=10, anchor="w")

        self.slider_questions = ctk.CTkSlider(frame_left, from_=10, to=100, number_of_steps=9)
        self.slider_questions.set(50)
        self.slider_questions.pack(pady=(20, 0), padx=10, fill="x")
        self.lbl_slider = ctk.CTkLabel(frame_left, text="Limite Domande: 50")
        self.lbl_slider.pack(pady=5)
        self.slider_questions.configure(command=lambda val: self.lbl_slider.configure(text=f"Limite Domande: {int(val)}"))

        self.btn_start = ctk.CTkButton(frame_left, text="🚀 Avvia Simulazione", command=self.start_simulation, state="disabled", fg_color="green")
        self.btn_start.pack(pady=20, padx=10, fill="x")

        frame_right = ctk.CTkFrame(self.tab_home)
        frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame_right, text="Filtro Capitoli", font=("Arial", 16)).pack(pady=5)
        
        self.scroll_chapters = ctk.CTkScrollableFrame(frame_right, label_text="Capitoli Trovati")
        self.scroll_chapters.pack(fill="both", expand=True, padx=5, pady=5)
        self.chapter_vars = {}

    # --- TAB EXAM ---
    def setup_exam_tab(self):
        self.top_bar = ctk.CTkFrame(self.tab_exam, height=50)
        self.top_bar.pack(fill="x", padx=5, pady=5)
        
        self.lbl_progress = ctk.CTkLabel(self.top_bar, text="Domanda 0/0", font=("Arial", 14))
        self.lbl_progress.pack(side="left", padx=20)
        
        self.lbl_timer = ctk.CTkLabel(self.top_bar, text="⏱ 00:00", font=("Arial", 14, "bold"), text_color="#e74c3c")
        self.lbl_timer.pack(side="right", padx=20)
        
        self.progress_bar = ctk.CTkProgressBar(self.tab_exam)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=5)

        self.scroll_q = ctk.CTkScrollableFrame(self.tab_exam)
        self.scroll_q.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.lbl_question_text = ctk.CTkLabel(self.scroll_q, text="Carica un DB e premi Start...", font=("Arial", 18), wraplength=800, justify="left")
        self.lbl_question_text.pack(pady=20, padx=10, anchor="w")
        
        self.options_frame = ctk.CTkFrame(self.scroll_q, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=10, pady=10)
        self.radio_var = tk.StringVar(value="")
        self.check_vars = []
        self.option_widgets = []

        self.lbl_feedback = ctk.CTkLabel(self.scroll_q, text="", font=("Arial", 14), wraplength=800, justify="left")
        self.lbl_feedback.pack(pady=10, padx=10, anchor="w")

        self.footer_exam = ctk.CTkFrame(self.tab_exam, height=60)
        self.footer_exam.pack(fill="x", padx=20, pady=10)
        
        self.btn_confirm = ctk.CTkButton(self.footer_exam, text="Conferma Risposta", command=self.check_answer)
        self.btn_confirm.pack(side="right", padx=10)
        
        self.btn_next = ctk.CTkButton(self.footer_exam, text="Prossima ➡", command=self.next_question, state="disabled")
        self.btn_next.pack(side="right", padx=10)

    # --- TAB EDITOR ---
    def setup_editor_tab(self):
        frame_input = ctk.CTkScrollableFrame(self.tab_editor)
        frame_input.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(frame_input, text="Crea Nuova Domanda", font=("Arial", 18, "bold")).pack(pady=10)

        self.entry_cap = ctk.CTkEntry(frame_input, placeholder_text="Capitolo")
        self.entry_cap.pack(fill="x", pady=5)
        
        self.entry_arg = ctk.CTkEntry(frame_input, placeholder_text="Argomento")
        self.entry_arg.pack(fill="x", pady=5)
        
        self.txt_domanda = ctk.CTkTextbox(frame_input, height=80)
        self.txt_domanda.pack(fill="x", pady=5)

        self.entries_opts = []
        labels = ["A", "B", "C", "D"]
        for l in labels:
            e = ctk.CTkEntry(frame_input, placeholder_text=f"Opzione {l}")
            e.pack(fill="x", pady=2)
            self.entries_opts.append(e)

        self.entry_correct = ctk.CTkEntry(frame_input, placeholder_text="Risposta Corretta (es. A)")
        self.entry_correct.pack(fill="x", pady=5)

        self.txt_explain = ctk.CTkTextbox(frame_input, height=60)
        self.txt_explain.pack(fill="x", pady=5)

        frame_btns = ctk.CTkFrame(self.tab_editor)
        frame_btns.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(frame_btns, text="➕ Aggiungi alla Lista", command=self.add_to_buffer).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="💾 Esporta Lista in JSON", command=self.export_buffer, fg_color="green").pack(side="right", padx=10)
        
        self.lbl_buffer_count = ctk.CTkLabel(frame_btns, text="Domande in memoria: 0")
        self.lbl_buffer_count.pack(side="left", padx=20)

    # --- TAB STATS ---
    def setup_stats_tab(self):
        self.stats_frame = ctk.CTkScrollableFrame(self.tab_stats)
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.btn_refresh_stats = ctk.CTkButton(self.stats_frame, text="🔄 Aggiorna Storico", command=self.refresh_stats)
        self.btn_refresh_stats.pack(pady=10)
        
        self.stats_container = ctk.CTkFrame(self.stats_frame)
        self.stats_container.pack(fill="both", expand=True)
        self.refresh_stats()

    def load_database(self):
        files = filedialog.askopenfilenames(filetypes=[("Data Files", "*.json;*.csv")])
        if not files: return
        self.questions_db = []
        self.chapters_found = set()
        for file_path in files:
            try:
                if file_path.lower().endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list): self.questions_db.extend(data)
            except Exception as e:
                messagebox.showerror("Errore", f"Errore lettura file {file_path}:\n{e}")
        for q in self.questions_db:
            if "capitolo" in q: self.chapters_found.add(q["capitolo"])
        self.populate_chapter_filter()
        self.btn_start.configure(state="normal")
        messagebox.showinfo("Caricamento", f"Caricate {len(self.questions_db)} domande.")

    def populate_chapter_filter(self):
        for widget in self.scroll_chapters.winfo_children(): widget.destroy()
        self.chapter_vars = {}
        self.var_all_caps = ctk.BooleanVar(value=True)
        cb_all = ctk.CTkCheckBox(self.scroll_chapters, text="-- TUTTI --", variable=self.var_all_caps, command=self.toggle_all_chapters)
        cb_all.pack(anchor="w", pady=2)
        for cap in sorted(list(self.chapters_found)):
            var = ctk.BooleanVar(value=True)
            self.chapter_vars[cap] = var
            ctk.CTkCheckBox(self.scroll_chapters, text=cap, variable=var).pack(anchor="w", pady=2)

    def toggle_all_chapters(self):
        val = self.var_all_caps.get()
        for cap in self.chapter_vars: self.chapter_vars[cap].set(val)

    def start_simulation(self):
        selected_caps = [cap for cap, var in self.chapter_vars.items() if var.get()]
        if not selected_caps:
            messagebox.showwarning("Attenzione", "Seleziona almeno un capitolo!")
            return
        pool = [q for q in self.questions_db if q.get("capitolo") in selected_caps]
        limit = int(self.slider_questions.get())
        self.filtered_questions = random.sample(pool, min(limit, len(pool)))
        random.shuffle(self.filtered_questions)
        self.current_question_index = 0
        self.score = 0
        self.wrong_questions = []
        self.user_answers = {}
        self.timer_running = True
        self.tabview.set("📝 Esame")
        self.load_question_ui()
        if self.switch_timer.get():
            self.exam_start_time = time.time()
            self.update_timer()
        else: self.lbl_timer.configure(text="--:--")

    def load_question_ui(self):
        for widget in self.options_frame.winfo_children(): widget.destroy()
        self.lbl_feedback.configure(text="")
        self.btn_confirm.configure(state="normal")
        self.btn_next.configure(state="disabled")
        q_data = self.filtered_questions[self.current_question_index]
        total = len(self.filtered_questions)
        self.lbl_progress.configure(text=f"Domanda {self.current_question_index + 1}/{total}")
        self.progress_bar.set((self.current_question_index) / total)
        self.lbl_question_text.configure(text=f"[{q_data.get('capitolo')}]\n\n{q_data['domanda']}")
        self.option_widgets = []
        opts = q_data['opzioni'][:]
        random.shuffle(opts)
        if q_data.get('tipo') == 'multipla':
            self.check_vars = []
            for opt_text in opts:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(self.options_frame, text=opt_text, variable=var)
                cb.pack(anchor="w", pady=5, padx=10); self.check_vars.append((var, opt_text))
        else:
            self.radio_var.set(None)
            for opt_text in opts:
                ctk.CTkRadioButton(self.options_frame, text=opt_text, variable=self.radio_var, value=opt_text).pack(anchor="w", pady=5, padx=10)

    def check_answer(self):
        q_data = self.filtered_questions[self.current_question_index]
        user_ans_list = []
        if q_data.get('tipo') == 'multipla':
            for var, text in self.check_vars:
                if var.get(): user_ans_list.append(text)
        else:
            val = self.radio_var.get()
            if val and val != "None": user_ans_list.append(val)
        if not user_ans_list: return
        correct_letters = q_data['risposta_corretta']
        if isinstance(correct_letters, str): correct_letters = [x.strip() for x in correct_letters.replace(",", " ").split()]
        user_letters = [ans_text.split('.')[0].strip() for ans_text in user_ans_list]
        is_correct = set(user_letters) == set(correct_letters)
        if is_correct: self.score += 1
        self.user_answers[q_data['id']] = is_correct
        self.btn_confirm.configure(state="disabled"); self.btn_next.configure(state="normal")
        if not self.switch_mode.get():
            msg = "✅ Corretto!" if is_correct else f"❌ Errato.\nCorretta: {q_data['risposta_corretta']}"
            self.lbl_feedback.configure(text=f"{msg}\n\n{q_data.get('spiegazione')}", text_color="green" if is_correct else "red")

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.filtered_questions): self.load_question_ui()
        else: self.finish_exam()

    def finish_exam(self):
        self.timer_running = False
        total = len(self.filtered_questions)
        perc = (self.score / total) * 100 if total > 0 else 0
        passed = perc >= 82
        self.db_manager.add_record(self.score, total, perc, passed)
        self.refresh_stats()
        messagebox.showinfo("Risultato", f"Punteggio: {self.score}/{total} ({perc:.1f}%)\nESITO: {'PROMOSSO' if passed else 'BOCCIATO'}")
        self.tabview.set("🏠 Home")

    def update_timer(self):
        if not self.timer_running: return
        rem = (90 * 60) - (time.time() - self.exam_start_time)
        if rem <= 0: self.finish_exam(); return
        m, s = divmod(int(rem), 60); self.lbl_timer.configure(text=f"⏱ {m:02d}:{s:02d}")
        self.after(1000, self.update_timer)

    def add_to_buffer(self):
        domanda = self.txt_domanda.get("0.0", "end").strip()
        if not domanda: return
        opts = [f"{chr(65+i)}. {e.get().strip()}" for i, e in enumerate(self.entries_opts) if e.get().strip()]
        correct = self.entry_correct.get().strip().upper()
        self.editor_questions_buffer.append({
            "id": str(int(time.time())), "capitolo": self.entry_cap.get().strip() or "Custom",
            "argomento": self.entry_arg.get().strip() or "Custom", "tipo": "multipla" if "," in correct else "singola",
            "domanda": domanda, "opzioni": opts, "risposta_corretta": correct, "spiegazione": self.txt_explain.get("0.0", "end").strip()
        })
        self.lbl_buffer_count.configure(text=f"Domande in memoria: {len(self.editor_questions_buffer)}")

    def export_buffer(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if f:
            with open(f, 'w', encoding='utf-8') as out: json.dump(self.editor_questions_buffer, out, indent=4)
            self.editor_questions_buffer = []; self.lbl_buffer_count.configure(text="Domande in memoria: 0")

    def refresh_stats(self):
        for w in self.stats_container.winfo_children(): w.destroy()
        history = self.db_manager.get_history()
        for i, h in enumerate(["Data", "Punti", "Tot", "%", "Esito"]):
            ctk.CTkLabel(self.stats_container, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10)
        for r_idx, row in enumerate(history):
            color = "green" if row[4] else "red"
            for c_idx, v in enumerate([row[0], str(row[1]), str(row[2]), f"{row[3]:.1f}%", "Promosso" if row[4] else "Bocciato"]):
                ctk.CTkLabel(self.stats_container, text=v, text_color=color if c_idx == 4 else None).grid(row=r_idx+1, column=c_idx, padx=10)

if __name__ == "__main__":
    app = ExamSimulatorV3()
    app.mainloop()