import os #Biblioteca para trabalhar com arquivos e pastas
import time #Controle de Tempo das Ações
import shutil #Manipulação de Arquivos
from watchdog.observers import Observer #Observa as pastas em tempo real
from watchdog.events import FileSystemEventHandler
from threading import Lock

lock = Lock() #Para executar um processo por vez

#Definindo a pasta monitorada
DOWNLOADS = os.path.expanduser("~/Downloads")

#Mapa de Decisão
DESTINOS = {
  "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
  "Imagens": [".jpg", ".jpeg", ".png", ".gif"],
  "Compactados": [".zip", ".rar", ".7z"],
}

#IA
def sugerir_categoria(nome_arquivo):
  nome = nome_arquivo.lower()
  if "boleto" in nome or "nota" in nome:
    return "Documentos"
  elif "foto" in nome or "print" in nome:
    return "Imagens"
  else:
    return None

#Classe que executa eventos + Função que ignora pastas + Organização
class OrganizadorHandler(FileSystemEventHandler):

  def on_created(self, event):
    if event.is_directory:
      return
    
    time.sleep(1) #Espera 1 segundo
    self.organizar(event.src_path) #Organiza o Arquivo
    
#Organização
  def organizar(self, caminho_arquivo):
    # Ignora eventos fora de Downloads
    if not caminho_arquivo.startswith(DOWNLOADS):
        return

    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()

    # Ignora arquivos temporários
    if extensao in [".crdownload", ".tmp", ".part"]:
        return

    destino = None  # sempre definido

    #POR EXTENSÃO
    for pasta, extensoes in DESTINOS.items():
        if extensao in extensoes:
            destino = os.path.join(DOWNLOADS, pasta)
            break

    #POR IA
    if destino is None:
        nome_arquivo = os.path.basename(caminho_arquivo)
        categoria_sugerida = sugerir_categoria(nome_arquivo)

        if categoria_sugerida:
            destino = os.path.join(DOWNLOADS, categoria_sugerida)

    #OUTROS
    if destino is None:
        destino = os.path.join(DOWNLOADS, "Outros")

    #Evitar mover arquivo de já foi movido
    if not os.path.exists(caminho_arquivo):
      return
    #MOVE (UM ÚNICO PONTO)
    os.makedirs(destino, exist_ok=True) #Ação de criar pasta se não existir

    with lock: # garante 1 arquivo por vez
      nome_arquivo = os.path.basename(caminho_arquivo)
      destino_final = gerar_destino_unico(destino, nome_arquivo)
      shutil.move(caminho_arquivo, destino_final)

    print(f"Movido para {os.path.basename(destino)}")

def gerar_destino_unico(destino, nome_arquivo): #Evitando Arquivos Repetidos
    base, ext = os.path.splitext(nome_arquivo)
    contador = 1
    destino_final = os.path.join(destino, nome_arquivo)

    while os.path.exists(destino_final):
        destino_final = os.path.join(destino, f"{base}_{contador}{ext}")
        contador += 1

    return destino_final

#Iniciando o Observador

if __name__ == "__main__":
  observer = Observer()
  observer.schedule(OrganizadorHandler(), DOWNLOADS, recursive=False)
  observer.start()
  print("📂 Monitorando Downloads...")

try:
  while True:
    time.sleep(5)
except KeyboardInterrupt:
  observer.stop()

observer.join()
