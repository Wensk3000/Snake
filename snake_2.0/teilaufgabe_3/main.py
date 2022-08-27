import tkinter as tk
import snake_ta3 as sn

app = tk.Tk() # Erzeugt ein neues "GUI"-Objekt vom Typ Tk
app.geometry('465x660') # Definiert die Abmaße des Hauptfensters
app.resizable(0, 0) # Sperrt die Abmaße des Hauptfensters
app.title('Snake') # Schreibt einen Title in die Statuszeile
spiel = sn.Spiel(app, 435, 435)#Erzeugt ein Objekt vom Typ Spiel
tk.mainloop() # Zeigt das GUI auf dem Bildschirm an