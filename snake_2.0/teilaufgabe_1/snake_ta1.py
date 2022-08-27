import tkinter as tk
import random
from tkinter import messagebox
from collections import namedtuple
import glob, os
Punkt = namedtuple('Punkt', 'x, y')  #Klasse zum Speichern der Koordinaten

LAENGE_SCHLANGE = 2
START_POS_X = 155
START_POS_Y = 155


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
        self.label = tk.Label(master, bg='white', fg='black', text='Geschwindigkeit:', font=('arial', 12, 'normal'))
        self.label.place(x=170, y=450, width=150, height=25)

        # 6. Scale
        self.geschwindigkeit = tk.IntVar(None, 1)
        geschwindigkeit_schieber = tk.Scale(master, orient='horizontal', variable=self.geschwindigkeit , from_=10, to=450, sliderlength=10, tickinterval=100, bg='white', troughcolor='red', resolution=10, width=10, relief='sunken')
        geschwindigkeit_schieber.place(x=170, y=480, width=150, height=60)



        # 7. Button
        button = tk.Button(master, text="START", font=('arial', 12, 'bold'), bg='grey', relief='raised',
                           command=self.starte_spiel)
        button.place(x=350, y=485, width=75, height=25)

        button = tk.Button(master, text="ENDE", font=('arial', 12, 'bold'), bg='grey', relief='raised')
        button.place(x=350, y=515, width=75, height=25)
        button.config(command=self.master.destroy)

        # Label KI
        self.alpha_wert = tk.StringVar(master, "0.001")
        self.epsilon_wert = tk.StringVar(master, "0.9")
        self.gamma_wert = tk.StringVar(master, "0.9")
        self.epsilon_verfall_spiele = tk.IntVar(master, 100)
        self.rb_modu_wert = tk.IntVar(master, 0)
        self.speichern_eingabe = tk.StringVar(master, "model.path")

        # Button KI
        #radio_button_normal = RadioButton(master, text="normal", variable=tk.StringVar, value="0") # hier intvar zuweisen?
        #radio_button_normal.pack(anchor = master)

        #Listbox Widget
        """"
        self.listbox_modell_laden = tk.Listbox(self.container, font=('arial', 2 10, 'normal'), bg='white',
        relief = 'sunken',
        selectbackground = 'blue',
        exportselection = 0)

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
        self.listbox_modell_laden.place(x=50, y=130, width=90, height=25)"""


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


        """self.koerper = tk.Label(w, bg='black', image=self.koerper_img)
        self.kopf.place(x=100, y=100, width=25, height=25)
        self.koerper.place(x=125, y=100, width=25, height=25)
        self.futter.place(x=50, y=50, width=25, height=25)"""

        self.erzeuge_schlange()

        self.tasten_funktionen()

        self.aktualisiere()

        self.erzeuge_belohnung()

        

    def erzeuge_schlange(self):
        if self.neues_spiel is True:
            self.schlange_koord.append(Punkt(START_POS_X, START_POS_Y))
            self.schlange.append(self.kopf)
            self.schlange[0].place(x=self.schlange_koord[0].x, y=self.schlange_koord[0].y)
            for i in range(LAENGE_SCHLANGE):
                self.schlange_koord.append(Punkt(START_POS_X-i*25 , START_POS_Y))  # Noch nicht ganz richtig
                self.schlange.append(tk.Label(self.master, bg='black', image=self.koerper_img))
                self.schlange[i+1].place(x=200, y=200)  # Warum -1??   # !!!aendert nichts am GUI!!
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
        self.starten = isinstance(True, bool)

    def bewege_schlange(self):
        if self.neu:  # neu so richtig? siehe Teilaufgabe
            """ Bewegt die Schlange weiter und prüft auf Kollisionen. 3 """

            if self.schlange_fertig:
                self.schlange_koord_old = []
                self.schlange_koord_old = self.schlange_koord

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

            for i in range(len(self.schlange_koord)):
                #x_old =
                #y_old =
                #y_new = y
                print(i)
                print("koord", self.schlange_koord)
                print("koord old", self.schlange_koord_old)
                print("schlange", self.schlange)
                #if i == range(len(self.schlange_koord)):
                   # self.schlange_fertg = True
                    #print("schlange fertig")

                if i == 0:
                    self.schlange_koord[0] = Punkt(x, y)
                    self.schlange[0].place(x=self.schlange_koord[0].x, y=self.schlange_koord[0].y)
                else:
                    #self.schlange[i].place(x=self.schlange_koord_old[i-1].x, y=self.schlange_koord_old[i-1].y)

                    self.schlange_koord[i] = Punkt(kopf_x , kopf_y)   # hier wird fehlerhaft überschriebe
                    self.schlange[i].place(x=self.schlange_koord[i].x, y=self.schlange_koord[i].y)   # muss noch optimiert werden (Geometrisch)

            self.neu = True
            # Methode bei game over verlassen
            if self.pruef_kollision(kopf_x, kopf_y) == True:
                self.message = "Du hast nur " + str(self.punkte) + " Punkte erreicht du Dill"
                messagebox.showinfo("Game over", self.message)  # Punkte anzeigen
                self.master.destroy()
                return  # soll eigentlich Programm anhalten

    def aktualisiere(self):
        """ Aktualisiert das GUI und führt die Spiellogik aus. 4 """
        if self.starten:
            self.bewege_schlange()
            self.pruefe_belohnung()
        self.after(500-self.geschwindigkeit.get(), self.aktualisiere)

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


    def pruef_kollision(self, kopf_x, kopf_y):
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

    def loesche_schlange(self):
            self.schlange = []
            self.schlange_koord = []


    def initialisiere(self):
        self.loesche_schlange()
        self.erzeuge_schlange()

        self.punkte_txt.config(text=self.record)
        self.record_txt.config(text=self.record)
        self.spielzeit_txt.config(text=self.record)

 

