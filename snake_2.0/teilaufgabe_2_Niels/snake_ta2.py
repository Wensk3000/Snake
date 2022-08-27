"""todo: -self.bewege_schlange fertig stellen
        - Parameter auf "normal" setzten -> kennt var nicht
        - neue Methode: kollision und aktualisiere einführen"""


import tkinter as tk
import random
from tkinter import messagebox
from collections import namedtuple
import glob, os
from enum import Enum
import numpy as np
import torch
Punkt = namedtuple('Punkt', 'x, y')  #Klasse zum Speichern der Koordinaten

LAENGE_SCHLANGE = 2
START_POS_X = 155
START_POS_Y = 155


BELOHNUNG_NIEDERLAGE = -10
BELOHNUNG_ABBRUCH = -20
BELOHNUNG_FUTTER = 10
BELOHNUNG_SCHRITT = 0


class Richtung(Enum):
    RECHTS = 1
    LINKS = 2
    HOCH = 3
    RUNTER = 4


class Spiel(tk.Frame):

    """ Diese Klasse beinhaltet ein GUI zur Ausführung eines Snake
    Spiels. Das GUI wurde mit "tkinter" programmiert.

    """
    belohnung_x = 0
    belohnung_y = 0


    def __init__(self, master, breite, hoehe):

        super(Spiel, self).__init__(master)

        self.x_richtung = 1
        self.y_richtung = 0
        self.punkte= 0
        self.record = 0

        self.starten = isinstance(False, bool)



        """ Das ist der Konstruktor der Klasse "Spiel".
            Hier werden alle Attribute der Klasse deklariert und
            initialisiert. 12 Zu den Attributen gehören auch die Widgets des GUIs.

        :param master: Ein Objekt des Typs Tk(), welches das Fenster
                    für die Erzeugung des GUIs darstellt
        :param breite: Die Breite des Spielfelds in Pixeln
        :param hoehe: Die Höhe des Spielfelds in Pixeln
        """


        self.schlange_koord = None
        """ Das ist der Superkonstruktor 
            ( der Konstruktor der Vererbenden Klasse) 
        """

        self.master = master
        self.breite = breite
        self.hoehe = hoehe

        #Canvas

        w = tk.Canvas(master, bg='black', bd=5, relief='sunken',
                   width=self.breite,
                   height=self.hoehe)
        w.pack()
        w.create_rectangle(0, 10, 435, 435)

        #Frame

        frame_eingabe = tk.Frame(master, bg='grey')
        frame_eingabe.place(x=10, y=445, height=205, width=445)

        #3. Label
        self.punkte_name = tk.Label(master, bg='white', anchor='w', fg='black', text='Punkte:', font=('arial', 12, 'normal'))
        self.punkte_name.place(x=15, y=450, width=80, height=25)

        self.record_name = tk.Label(master, bg='white', anchor='w', fg='black', text='Rekord:', font=('arial', 12, 'normal'))
        self.record_name.place(x=15, y=480, width=80, height=25)

        self.spielzeit_name = tk.Label(master, bg='white', anchor='w', fg='black', text='Spielzeit:', font=('arial', 12, 'normal'))
        self.spielzeit_name.place(x=15, y=510, width=80, height=25)

        # 4. Label
        self.punkte_txt = tk.Label(master, bg='white', relief='sunken', fg='black', text='0', font=('arial', 12, 'normal'))
        self.punkte_txt.place(x=100, y=450, width=50, height=25)

        self.record_txt = tk.Label(master, bg='white', relief='sunken', fg='black', text='0', font=('arial', 12, 'normal'))
        self.record_txt.place(x=100, y=480, width=50, height=25)

        self.spielzeit_txt = tk.Label(master, bg='white', relief='sunken', fg='black', text='0', font=('arial', 12, 'normal'))
        self.spielzeit_txt.place(x=100, y=510, width=50, height=25)

        # 5. Label
        self.label = tk.Label(master, bg='white', fg='black', text='Geschwindigkeit:', relief="solid", font=('arial', 12, 'normal'))
        self.label.place(x=170, y=450, width=150, height=25)

        # 6. Scale
        self.geschwindigkeit = tk.IntVar(None, 1)
        geschwindigkeit_schieber = tk.Scale(master, orient='horizontal', variable=self.geschwindigkeit , from_=10, to=450, sliderlength=10, tickinterval=100, bg='white', troughcolor='red', resolution=10, width=10, relief='sunken')
        geschwindigkeit_schieber.place(x=170, y=480, width=150, height=55)

        # 7. Button
        button_start = tk.Button(master, text="START", font=('arial', 10, 'bold'), bg='grey', relief='raised')
        button_start.place(x=390, y=580, width=50, height=20)
        button_start.config(command=self.starte_spiel)

        button_ende = tk.Button(master, text="ENDE", font=('arial', 10, 'bold'), bg='grey', relief='raised')
        button_ende.place(x=390, y=610, width=50, height=20)
        button_ende.config(command=self.master.destroy)

        button_stop = tk.Button(master, text="STOP", font=('arial', 10, 'bold'), bg='grey', relief='raised')
        button_stop.place(x=330, y=580, width=50, height=20)
        button_stop.config(command=self.stop)


        # Label KI
        self.alpha_wert = tk.StringVar(master, "0.001")
        self.epsilon_wert = tk.StringVar(master, "0.9")
        self.gamma_wert = tk.StringVar(master, "0.9")
        self.epsilon_verfall_spiele = tk.IntVar(master, 100)
        self.rb_modul_wert = tk.IntVar(master, 0)
        self.speichern_eingabe = tk.StringVar(master, "model.pth")

        # Button KI

        # Radio Button
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="Modus:", font=('arial', 12, 'normal'))  # Farbe hinzu
        self.modus_lable.place(x=360, y=450, width=80, height=30)

        self.radio = tk.Label(master, anchor='w', borderwidth=2, relief="solid") # Farbe hinzu!!
        self.radio.place(x=360, y=490, width=80, height=80)

        radio_button_normal = tk.Radiobutton(self.radio, text="Normal", variable=tk.StringVar, value="0") # hier intvar zuweisen?
        radio_button_normal.pack()
        radio_button_ki = tk.Radiobutton(self.radio, text="RL-Agent", variable=tk.StringVar, value="1")
        radio_button_ki.pack()
        radio_button_ki = tk.Radiobutton(self.radio, text="Training", variable=tk.StringVar, value="2")
        radio_button_ki.pack()

        #RLA-Modell:
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="RLA-Modell:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=15, y=540, width=135, height=30)
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="Lad.:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=15, y=575, width=40, height=25)
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="Spe.:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=15, y=605, width=40, height=25)

        self.model_pth = tk.Entry(master, textvariable=self.speichern_eingabe)
        self.model_pth.place(x=60, y=605, width=90, height=25)

        self.listbox_modell_laden = tk.Listbox(self.master, font=('arial', 10, 'normal'), bg='white',
                                               relief = 'sunken', selectbackground = 'blue', exportselection = 0)

        self.path_dict = {}
        os.chdir("model")

        i = 0
        for file_name in glob.glob("*.pth"):
            self.path_dict[i] = f"model/{file_name}"
            self.listbox_modell_laden.insert(i, file_name)
            i += 1
        os.chdir(os.path.dirname(os.getcwd()))
        self.listbox_modell_laden.see(0)
        self.listbox_modell_laden.select_set(first=0)
        self.listbox_modell_laden.place(x=60, y=575, width=90, height=25)

        # RLA-Parameter
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="RLA-PArameter:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=170, y=540, width=150, height=30)

        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="α:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=170, y=575, width=25, height=25)
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="ε:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=170, y=605, width=25, height=25)
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="γ:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=240, y=575, width=25, height=25)
        self.modus_lable = tk.Label(master, anchor='w', borderwidth=2, relief="solid", text="εVS:",
                                    font=('arial', 12, 'normal'))
        self.modus_lable.place(x=240, y=605, width=35, height=25)

        self.alpha_entry = tk.Entry(master, textvariable=self.alpha_wert)
        self.alpha_entry.place(x=197.5, y=575, width=40, height=25)
        self.epsilon_entry = tk.Entry(master, textvariable=self.epsilon_wert)
        self.epsilon_entry.place(x=197.5, y=605, width=40, height=25)
        self.gamma_entry = tk.Entry(master, textvariable=self.gamma_wert)
        self.gamma_entry.place(x=270, y=575, width=50, height=25)
        self.epsilon_VS_entry = tk.Entry(master, textvariable=self.epsilon_verfall_spiele)
        self.epsilon_VS_entry.place(x=280, y=605, width=40, height=25)


        #GUI
        self.neues_spiel = isinstance(True, bool)
        self.schlange = []
        self.schlange_koord = []
        self.kopf_img = tk.PhotoImage(file='images/kopf.png')
        self.koerper_img = tk.PhotoImage(file='images/koerper.png')
        self.futter_img = tk.PhotoImage(file='images/futter.png')
        self.kopf = tk.Label(w, bg='black', image=self.kopf_img)
        self.futter = tk.Label(w, bg='black', image=self.futter_img)


        #Merker
        self.neu = isinstance(True, bool)

        #Speichert Koordinaten der Belohnung
        self.belohnung_x = 0
        self.belohnung_y = 0

        self.punkt = 0

        #Score
        self.highscore = 0
        self.start_zeit = None

        self.schlange_fertig= isinstance(False, bool)

        self.iteration = 0
        self.richtung = Richtung.RECHTS
        self.belohnung_wert = 0
        self.agent = None
        self.trainieren = isinstance(False, bool)
        self.plot_punkt = None
        self.plot_punkte_durchschnitt = None
        self.punkte_gesamt = None
        self.modell_geladen = isinstance(False, bool)

        self.game_over = isinstance(False, bool)
        self.starten = False


        self.erzeuge_schlange()

        self.tasten_funktionen()

        self.aktualisiere()

        self.erzeuge_belohnung()


    def erzeuge_schlange(self):
        if self.neues_spiel:
            self.schlange_koord.append(Punkt(START_POS_X, START_POS_Y))
            self.schlange.append(self.kopf)
            self.schlange[0].place(x=self.schlange_koord[0].x, y=self.schlange_koord[0].y)
            for i in range(LAENGE_SCHLANGE):
                self.schlange_koord.append(Punkt(165-25*(i+1), 155))  # Noch nicht ganz richtig # Versatz von Start_pos
                self.schlange.append(tk.Label(self.master, bg='black', image=self.koerper_img))
                self.schlange[i+1].place(x=self.schlange_koord[i+1].x, y=self.schlange_koord[i+1].y)
                print("erste schlange")
        self.neues_spiel = False


    def links(self, event):
        if self.x_richtung != 1:
            self.x_richtung = -1
            self.y_richtung = 0
            print("left")

    def rechts(self, event):
        if self.x_richtung != -1:
            self.x_richtung = 1
            self.y_richtung = 0
            print("rechts")

    def hoch(self, event):
        if self.y_richtung != 1:
            self.y_richtung = -1
            self.x_richtung = 0
            print("hoch")

    def runter(self, event):
        if self.y_richtung != -1:
            self.y_richtung = 1
            self.x_richtung = 0
            print("runter")


    def tasten_funktionen(self):  # Verknüpfung mit Tastatur

            self.master.bind('<Left>', self.links)
            self.master.bind('<Right>', self.rechts)
            self.master.bind('<Up>', self.hoch)
            self.master.bind('<Down>', self.runter)

    def starte_spiel(self):
        print("self.starte_spiel")
        self.starten = isinstance(True, bool)


    def bewege_schlange(self):
        if self.neu:  # neu so richtig? siehe Teilaufgabe
            """ Bewegt die Schlange weiter und prüft auf Kollisionen. 3 """

            kopf_x = self.schlange_koord[0].x
            kopf_y = self.schlange_koord[0].y

            if self.x_richtung == 1:
                x = kopf_x + 25
                y = kopf_y
            elif self.x_richtung == -1:
                x = kopf_x - 25
                y = kopf_y
            elif self.y_richtung == 1:
                x = kopf_x
                y = kopf_y + 25
            elif self.y_richtung == -1:
                x = kopf_x
                y = kopf_y - 25
            self.neu = False
            print ("Length of snake: " + str(len(self.schlange_koord)))
            for i in range(len(self.schlange_koord) - 1, -1, -1):
                print ("Koordinaten [" + str(i) + "]" + str(self.schlange_koord[i]))
                if i == 0:
                    print("Setting at index 0: " + str(self.schlange_koord[i]))
                    self.schlange_koord[i] = Punkt(x, y)
                else:
                    self.schlange_koord[i] = self.schlange_koord[i-1]
                self.schlange[i].place(x=self.schlange_koord[i].x, y=self.schlange_koord[i].y)
                self.neu = True
            #Methode bei game over verlassen
            if self.pruef_kollision(kopf_x, kopf_y) == True:
                self.message = "Du hast " + str(self.punkte) + " Punkte erreicht."
                messagebox.showinfo("Game over", self.message)  # Punkte anzeigen
                self.stop()


    def aktualisiere(self):   # alt
        """ Aktualisiert das GUI und führt die Spiellogik aus. 4 """
        print("starten", self.starten)
        if self.starten:
            self.bewege_schlange()
            self.pruefe_belohnung()
        self.after(500 - self.geschwindigkeit.get(), self.aktualisiere)


    """def aktualisiere(self):  # neu
        Aktualisiert das GUI und führt die Spiellogik aus. 
        if self.game_over:
            self.initialisiere()
        else:
            if self.starten:
                self.radio_button_ki.config(state='disabled')
                self.radio_button_normal.config(state='disabled')
                self.radio_button_training.config(state='disabled')
                self.alpha_eingabe.config(state='disabled')
                self.epsilon_eingabe.config(state='disabled')
                self.gamma_eingabe.config(state='disabled')
                self.epsilon_verfall_eingabe.config(state='disabled')
                if self.rb_modus_wert.get() == 0:
                    self.normal()
                elif self.rb_modus_wert.get() == 2:
                    self.training()
                else:
                    self.rl_agent()
            else:
                self.after(self.geschwindigkeit.get(), self.aktualisiere())"""

    def erzeuge_belohnung(self):
        self.wiederholen = isinstance(True, bool)
        while self.wiederholen:
            self.belohnung_x = random.choice(range(5, self.breite - 5, 25))
            self.belohnung_y = random.choice(range(5, self.breite - 5, 25))

            self.wiederholen = False

        for i in range(len(self.schlange_koord)):
            if self.schlange_koord[i].x == self.belohnung_x and self.schlange_koord[i].y == self.belohnung_y:
                self.wiederholen = True
            self.futter.place(x=self.belohnung_x, y=self.belohnung_y, width=25, height=25)


    def pruefe_belohnung(self):
        if self.schlange_koord[0].x == self.belohnung_x and self.schlange_koord[0].y == self.belohnung_y:
            # Punkt hinzufügen und anzeigen
            self.punkte += 1
            self.punkte_txt.config(text=self.punkte)
            self.belohnung_wert = BELOHNUNG_FUTTER

            # Rekord
            if self.punkte >= self.record:
                self.record = self.punkte
                self.record_txt.config(text=self.record)

            #Neues Futter erzeugen
            self.erzeuge_belohnung()

            #Schlange verlängern
            print("Schlange verlängern")
            laenge = len(self.schlange_koord)
            self.schlange_koord.append(Punkt(self.schlange_koord[laenge-1].x, self.schlange_koord[laenge-1].y))  # Noch nicht ganz richtig
            self.schlange.append(tk.Label(self.master, bg='black', image=self.koerper_img))


    def pruef_kollision(self, kopf_x, kopf_y):   # alte Methode
        self.game_over = isinstance(False, bool)
        # Kollidiert Kopf mit Rand?
        if self.schlange_koord[0].x > 420 or self.schlange_koord[0].y > 420 or \
                self.schlange_koord[0].x < 5 or self.schlange_koord[0].y < 5:
            self.game_over = True
            print("game_over1")
            return self.game_over
        else:
            i = 1
            while i < len(self.schlange_koord):
                # Kollidiert Körper mit Kopf?
                if self.schlange_koord[i].x == self.schlange_koord[0].x and \
                        self.schlange_koord[i].y == self.schlange_koord[0].y: # Funktion fehlerhaft
                    self.game_over = True
                    print("game_over2")
                    return self.game_over
                i += 1
        self.game_over = False
        return self.game_over

    """
    def pruefe_kollision(self, kopf_x, kopf_y, state_test=False):       # neue Methode soll alte ersetzten
        if kopf_x < 5 or kopf_x > (self.breite - 30) or kopf_y < 5 or kopf_y > (self.hoehe - 30):
            if not state_test:
                self.belohnung_wert = BELOHNUNG_NIEDERLAGE
            return True

        elif self.rb_modus_wert.get() != 0 and self.iteration > 100 * len(self.schlange) and not state_test:
            self.belohnung_wert = BELOHNUNG_ABBRUCH
            return True

        else:
            for koerper in self.schlange_koord[1:]:
                if kopf_x == koerper.x and kopf_y == koerper.y:
                    if not state_test:
                     self.belohnung_wert = BELOHNUNG_NIEDERLAGE
                return True

            if not state_test:
                self.belohnung_wert = BELOHNUNG_SCHRITT
            return False"""

    def loesche_schlange(self):
            self.neues_spiel = isinstance(True, bool)
            self.schlange = []
            self.schlange_koord = []




    def initialisiere(self):
        self.loesche_schlange()
        self.erzeuge_schlange()

        self.iteration = 0
        self.richtung = Richtung.RECHTS
        self.modell_geladen = False

        self.punkte = 0  # Punkte auf 0 setzten
        self.punkte_txt.config(text=self.punkte)

        """if not self.starten: # Wird gesprerrt nach Spielstart

            self.radio_button_ki.config(state='normal')  # Warum attribute nicht gefunden??
            self.radio_button_normal.config(state='normal')
            self.radio_button_training.config(state='normal')
            self.alpha_eingabe.config(state='normal')
            self.epsilon_eingabe.config(state='normal')
            self.gamma_eingabe.config(state='normal')
            self.epsilon_verfall_eingabe.config(state='normal')"""


    def stop(self):  # Funktion funktioniert nicht
        self.game_over = True
        self.starten = False
        self.initialisiere()





 

