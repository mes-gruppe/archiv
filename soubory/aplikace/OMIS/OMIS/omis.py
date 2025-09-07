import os
import pygame
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Nastavení pracovního adresáře na adresář, kde je uložen skript
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Inicializace pygame pro přehrávání zvuků
pygame.mixer.init()

class MetroHlasicApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("OMIS 1 HLASIC ZASTAVEK (v1.0) MENU")

        # Nastavení ikony
        self.set_icon()

        # Vytvoření nadpisu
        self.title_label = tk.Label(root, text="OMIS 1 HLASIC ZASTAVEK (v1.0)", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Proměnné pro sledování složky a aktuálního indexu
        self.current_index = 1
        self.selected_folder = None

        # Tlačítka pro výběr směru
        self.direction_button_kuncice = tk.Button(root, text="Smer Kuncice", command=self.select_folder_kuncice, width=20, height=2)
        self.direction_button_kuncice.pack(pady=10)

        self.direction_button_salamounova = tk.Button(root, text="Smer Salamonova", command=self.select_folder_salamounova, width=20, height=2)
        self.direction_button_salamounova.pack(pady=10)

        # Umístění copyrightu do dolního rohu
        self.copyright_label = tk.Label(root, text="(c) 2024 OMIS Systemy, s.r.o.", font=("Arial", 8))
        self.copyright_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    def set_icon(self):
        # Nastavení ikony pro hlavní okno
        icon_path = "icon.ico"
        if os.path.isfile(icon_path):
            self.root.iconbitmap(icon_path)

    def select_folder_kuncice(self):
        self.selected_folder = "kuncice"
        self.current_index = 1
        self.open_play_window()

    def select_folder_salamounova(self):
        self.selected_folder = "salamounova"
        self.current_index = 1
        self.open_play_window()

    def open_play_window(self):
        # Vytvoření nového okna pro přehrávání zvuků
        self.play_window = tk.Toplevel(self.root)
        self.play_window.geometry("400x300")
        self.play_window.title("OMIS hlaseni zastavek")

        # Nastavení ikony pro okno přehrávání
        self.set_icon_play_window()

        # Tlačítko pro přehrání zvuku
        self.play_button = tk.Button(self.play_window, text="Hlasit nasledujici stanici", command=self.play_next_stop, width=20, height=2)
        self.play_button.pack(pady=10)

        # Tlačítko pro zobrazení jízdního řádu
        self.show_schedule_button = tk.Button(self.play_window, text="Zobrazit jizdni rad", command=self.show_schedule, width=20, height=2)
        self.show_schedule_button.pack(pady=10)

        # Přidání copyrightu do dolního rohu
        self.play_window.copyright_label = tk.Label(self.play_window, text="(c) 2024 OMIS Systemy, s.r.o.", font=("Arial", 8))
        self.play_window.copyright_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    def set_icon_play_window(self):
        # Nastavení ikony pro okno přehrávání
        icon_path = "icon.ico"
        if os.path.isfile(icon_path):
            self.play_window.iconbitmap(icon_path)

    def show_schedule(self):
        schedule_file_path = os.path.join(self.selected_folder, "jizdni-rad.txt")
        
        # Ověření existence souboru jízdního řádu
        if not os.path.isfile(schedule_file_path):
            messagebox.showerror("Chyba souboru!", f"Soubor jizdni-rad.txt nebyl nalezen: {schedule_file_path}")
            return

        # Vytvoření nového okna pro zobrazení jízdního řádu
        schedule_window = tk.Toplevel(self.play_window)
        schedule_window.title("Nahlednuti do jizdniho radu")
        schedule_window.geometry("400x300")

        # Scrollable text area for displaying the schedule
        schedule_text = scrolledtext.ScrolledText(schedule_window, wrap=tk.WORD)
        schedule_text.pack(expand=True, fill=tk.BOTH)

        # Načtení a zobrazení obsahu souboru
        with open(schedule_file_path, 'r', encoding='utf-8') as file:
            schedule_content = file.read()
            schedule_text.insert(tk.END, schedule_content)
        
        # Deaktivace možnosti úpravy textu
        schedule_text.configure(state='disabled')

    def play_next_stop(self):
        if self.selected_folder is None:
            messagebox.showwarning("Vyber smeru", "Nejdrive vyberte smer jizdy.")
            return
        
        # Soubory pro gong a aktuální zvuk
        gong_path = os.path.join(self.selected_folder, "gong.wav")
        stop_path = os.path.join(self.selected_folder, f"{self.current_index}.wav")

        # Ověření existence zvukových souborů
        if not os.path.isfile(gong_path):
            messagebox.showerror("Chyba souboru!", f"Gong zvuk nebyl nalezen na ceste: {gong_path}")
            return
        if not os.path.isfile(stop_path):
            messagebox.showerror("Chyba souboru!", f"Zvuk {self.current_index}.wav nebyl nalezen na ceste: {stop_path}")
            return

        # Přehrání gongu a následně 0,5 s pauza před přehráním zastávky
        gong_sound = pygame.mixer.Sound(gong_path)
        gong_sound.play()

        # Počkej na dohrání gongu
        while pygame.mixer.get_busy():
            pygame.time.delay(10)  # Malá prodleva pro kontrolu stavu přehrávání

        # 0,5 s pauza
        pygame.time.delay(500)

        # Přehrání zastávky
        stop_sound = pygame.mixer.Sound(stop_path)
        stop_sound.play()

        # Zvyšte index pro další přehrání
        self.current_index += 1

# Vytvoření hlavního okna a spuštění aplikace
root = tk.Tk()
app = MetroHlasicApp(root)
root.mainloop()
