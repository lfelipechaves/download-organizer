import os #Biblioteca para trabalhar com arquivos e pastas
import time #Controle de Tempo das Ações
import shutil #Manipulação de Arquivos
from watchdog.observers import Observer #Observa as pastas em tempo real
from watchdog.events import FileSystemEventHandler
from threading import Lock
import logging

lock = Lock() #Para executar um processo por vez

#Configuração Básica LOG
logging.basicConfig(
  filename='download_organizer.log',
  level=logging.DEBUG, 
  format='%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'
)

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

  def __init__(self, pasta_alvo):
        self.pasta_alvo = pasta_alvo

  def on_created(self, event):
    if event.is_directory:
      return
    
    time.sleep(1) #Espera 1 segundo
    self.organizar(event.src_path) #Organiza o Arquivo

    
#Organização
  def organizar(self, caminho_arquivo):

    def caminho_Arquivo_comeca(caminho, pasta):
     caminho = os.path.normpath(caminho)
     pasta = os.path.normpath(pasta)
     return caminho.startswith(pasta)
    
    if not caminho_Arquivo_comeca(caminho_arquivo, self.pasta_alvo):
       return

    _, extensao = os.path.splitext(caminho_arquivo)
    extensao = extensao.lower()

    # Ignora arquivos temporários
    if extensao in [".crdownload", ".tmp", ".part"]:
        return logging.debug(f"Arquivos Temporários Ignorados: {caminho_arquivo}")

    destino = None  # sempre definido

    #POR EXTENSÃO
    for pasta, extensoes in DESTINOS.items():
        if extensao in extensoes:
            destino = os.path.join(self.pasta_alvo, pasta)
            break

    #POR IA
    if destino is None:
        nome_arquivo = os.path.basename(caminho_arquivo)
        categoria_sugerida = sugerir_categoria(nome_arquivo)

        if categoria_sugerida:
            destino = os.path.join(self.pasta_alvo, categoria_sugerida)
            logging.info(f"Categoria sugerida por IA: {categoria_sugerida} para {nome_arquivo}")

    #OUTROS
    if destino is None:
        destino = os.path.join(self.pasta_alvo, "Outros")
        logging.info(f"Arquivo enviado para 'Outros': {caminho_arquivo}")

    #Evitar mover arquivo de já foi movido
    if not os.path.exists(caminho_arquivo):
      return
    
    #MOVE (UM ÚNICO PONTO)
    os.makedirs(destino, exist_ok=True) #Ação de criar pasta se não existir

    with lock: # garante 1 arquivo por vez
      nome_arquivo = os.path.basename(caminho_arquivo)
      destino_final = gerar_destino_unico(destino, nome_arquivo)
      shutil.move(caminho_arquivo, destino_final)

    logging.info(f"Movido para {os.path.basename(destino)}")

def gerar_destino_unico(destino, nome_arquivo): #Evitando Arquivos Repetidos
    base, ext = os.path.splitext(nome_arquivo)
    contador = 1
    destino_final = os.path.join(destino, nome_arquivo)

    while os.path.exists(destino_final):
        destino_final = os.path.join(destino, f"{base}_{contador}{ext}")
        contador += 1

    return destino_final