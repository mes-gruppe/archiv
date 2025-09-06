# Copyright (c) 2025 Tomas Spratek. All rights reserved.
# Kopirovani, upravovani nebo sdileni bez souhlasu zakazano.

import tkinter as tk
from tkinter import ttk
import os
import pygame
import re

LINKY_FOLDER = "linky"
SOUNDS_FOLDER = "zvuky"
GONG_FILE = os.path.join(SOUNDS_FOLDER, "upozorneni/gong.wav")

pygame.mixer.init()

class AVISApp:
    def __init__(self, root):
        self.root = root
        root.title("AVIS")
        root.geometry("500x400")

        # Text v rohu
        self.corner_label = tk.Label(root, text="Audiovizualni Informacni System (testovaci verze)", font=("Arial", 12))
        self.corner_label.place(x=5, y=5)

        # Tlacitko NASLEDUJICI
        self.next_button = tk.Button(root, text="NASLEDUJICI >", command=self.next_line)
        self.next_button.place(x=5, y=40)

        # Vyber souboru
        self.file_select = ttk.Combobox(root, state="readonly")
        self.file_select.place(x=5, y=75)
        self.file_select.bind("<<ComboboxSelected>>", self.load_file)

        # Textove okno
        self.text_area = tk.Text(root, width=55, height=12)
        self.text_area.place(x=5, y=110)

        # Copyright v pravem dolnim rohu
        self.copyright_label = tk.Label(
            root,
            text="©2025 Tomas Spratek",
            font=("Arial", 10),
            anchor="se"
        )
        self.copyright_label.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

        # Verze v levem dolnim rohu
        self.version_label = tk.Label(
            root,
            text="verze 25.001T",
            font=("Arial", 10),
            anchor="sw"
        )
        self.version_label.place(x=5, rely=1.0, anchor="sw", y=-5)

        # Infotabule - maximalizované okno
        self.info_window = tk.Toplevel(root)
        self.info_window.title("Infotabule")
        self.info_window.state("zoomed")
        self.info_window.configure(bg="#2e2e2e")

        # Hlavní text
        self.main_label = tk.Label(
            self.info_window,
            text="",
            font=("Arial", 36, "bold"),
            fg="#40E0D0",
            bg="#2e2e2e",
            justify="center",
            anchor="center"
        )
        self.main_label.pack(fill=tk.BOTH, expand=False, pady=(200,0))

        # Malý červený text
        self.sub_label = tk.Label(
            self.info_window,
            text="",
            font=("Arial", 24, "italic"),
            fg="#FF0000",
            bg="#2e2e2e",
            justify="center",
            anchor="center"
        )
        self.sub_label.pack(fill=tk.BOTH, expand=False)

        self.info_window.bind("<Configure>", self.resize_text)

        self.lines = []
        self.current_index = 0
        self.current_file_path = None
        self.all_main_texts = []
        self.all_sub_texts = []

        self.load_files()

    def resize_text(self, event):
        width = event.width
        height = event.height

        # Hlavní text - velký modrý
        if self.main_label['text']:
            max_text_width = width - 100  # padding 50px z každé strany
            test_font_size = 10
            test_label = tk.Label(self.info_window, text=self.main_label['text'], font=("Arial", test_font_size, "bold"))
            test_label.update_idletasks()
            while test_label.winfo_reqwidth() < max_text_width and test_font_size < 200:
                test_font_size += 1
                test_label.config(font=("Arial", test_font_size, "bold"))
                test_label.update_idletasks()
            main_size = test_font_size - 1
        else:
            main_size = 36

        # Malý text - červený
        sub_size = max(int(main_size / 2), 12)

        self.main_label.config(font=("Arial", main_size, "bold"))
        self.sub_label.config(font=("Arial", sub_size, "italic"))

    def load_files(self, event=None):
        if not os.path.exists(LINKY_FOLDER):
            os.makedirs(LINKY_FOLDER)
        txt_files = [f for f in os.listdir(LINKY_FOLDER) if f.endswith(".txt")]
        self.file_select['values'] = txt_files
        self.file_select.set('')
        self.text_area.delete(1.0, tk.END)

    def load_file(self, event):
        filename = self.file_select.get()
        if not filename:
            return
        path = os.path.join(LINKY_FOLDER, filename)
        self.current_file_path = path
        self.lines = []
        self.all_main_texts = []
        self.all_sub_texts = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.lines.append(line)
                # Extrahovat hlavni text mezi *...*
                main_match = re.search(r"\*(.*?)\*", line)
                main_text = main_match.group(1).strip() if main_match else ""
                self.all_main_texts.append(main_text)
                # Extrahovat sub text mezi "...", pokud existuje
                sub_match = re.search(r'\"(.*?)\"', line)
                sub_text = sub_match.group(1).strip() if sub_match else ""
                self.all_sub_texts.append(sub_text)

        self.current_index = 0
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n".join(self.lines))
        self.main_label.config(text="")
        self.sub_label.config(text="")

    def play_sound(self, filepath):
        if not os.path.exists(filepath):
            print(f"Soubor {filepath} neexistuje")
            return
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def next_line(self):
        if self.current_index >= len(self.lines):
            print("Konec souboru")
            return

        line = self.lines[self.current_index]
        main_text = self.all_main_texts[self.current_index]
        sub_text = self.all_sub_texts[self.current_index]
        self.current_index += 1

        # Přehrání gongu
        self.play_sound(GONG_FILE)

        # Přehrání zvuku pokud je definován
        if "=" in line:
            parts = line.split("=", 1)
            path_part = parts[1].strip()
            sound_path = path_part.split("*",1)[0].strip()
            target_file_path = os.path.join(sound_path)
            self.play_sound(target_file_path)

        # Aktualizace infotabule
        if main_text:
            words = main_text.split()
            if len(words) > 1:
                display_text = words[0] + "\n" + " ".join(words[1:])
            else:
                display_text = main_text
            self.main_label.config(text=display_text)
        else:
            self.main_label.config(text="")

        if sub_text:
            self.sub_label.config(text=sub_text)
        else:
            self.sub_label.config(text="")

root = tk.Tk()
app = AVISApp(root)
root.mainloop()
