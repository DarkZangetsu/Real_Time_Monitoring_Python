import tkinter as tk
from tkinter import ttk
import psutil
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation


def update_data():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory().percent
        current_time = time.strftime("%H:%M:%S", time.localtime())

        # Ajout des nouvelles données aux listes
        x_data.append(current_time)
        y_cpu_data.append(cpu_percent)
        y_mem_data.append(memory_info)

        # Limiter la taille des listes pour ne pas surcharger la mémoire
        if len(x_data) > 20:
            x_data.pop(0)
            y_cpu_data.pop(0)
            y_mem_data.pop(0)

        time.sleep(1)

def animate(i):
    ax1.clear()
    ax2.clear()

    ax1.plot(x_data, y_cpu_data, label='CPU Usage (%)')
    ax2.plot(x_data, y_mem_data, label='Memory Usage (%)')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left')

    ax1.set_title('CPU Usage Over Time')
    ax2.set_title('Memory Usage Over Time')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('CPU Usage (%)')

    ax2.set_xlabel('Time')
    ax2.set_ylabel('Memory Usage (%)')

# Initialisation des listes de données
x_data = []
y_cpu_data = []
y_mem_data = []

# Création de la fenêtre principale
root = tk.Tk()
root.title("Real-Time System Monitoring")

# Création de la figure matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Création du widget Canvas pour afficher les graphiques
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Démarrage du thread de mise à jour des données
threading.Thread(target=update_data, daemon=True).start()

# Configuration de l'animation
ani = animation.FuncAnimation(fig, animate, interval=1000)

root.mainloop()
