from organizer import OrganizadorHandler, DOWNLOADS
from watchdog.observers import Observer
import logging
import threading
import time
import tkinter as tk
from tkinter import filedialog

# Configuração mínima do logging para terminal
logging.basicConfig(level=logging.INFO)

def iniciar_monitoramento(pasta):
  observer = Observer()
  observer.schedule(OrganizadorHandler(pasta), pasta, recursive=False)
  observer.start()
  logging.info(f"Monitorando {pasta}...")

  #Mantém o observador vivo sem travar o thread
  try:
     while True:
        time.sleep(1) #Antigo "pass"
  except KeyboardInterrupt:
     observer.stop()
  except Exception as e:
     logging.error(f"Erro no monitoramente: {e}")

def escolher_pasta_e_iniciar():
    pasta = filedialog.askdirectory()
    if pasta:
        t = threading.Thread(target=iniciar_monitoramento, args=(pasta,))
        t.daemon = True
        t.start()
        logging.info(f"Iniciando monitoramento na pasta: {pasta}")

# GUI
root = tk.Tk()
root.title("Download Organizer")

btn_iniciar = tk.Button(root, text="Escolher Pasta e Iniciar", command=escolher_pasta_e_iniciar)
btn_iniciar.pack(pady=20)

t = threading.Thread(target=iniciar_monitoramento, args=(DOWNLOADS,))
t.daemon = True
t.start()
logging.info(f"Monitoramente automático iniciado na pasta: {DOWNLOADS}")

root.mainloop()
