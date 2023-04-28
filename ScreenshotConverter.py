import os
import shutil
import pytesseract
import spacy
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

app = QApplication([])
app.setStyle('Fusion')

# Selecionar a pasta de origem
origem_dir = QFileDialog.getExistingDirectory(None, 'Selecione a pasta de origem')

# Selecionar a pasta de destino
destino_dir = QFileDialog.getExistingDirectory(None, 'Selecione a pasta de destino')

# Load a pre-trained spaCy model for Portuguese
nlp = spacy.load('pt_core_news_sm')

# Loop pelos arquivos na pasta de origem
for arquivo in os.listdir(origem_dir):
    # Verificar se é uma imagem
    if arquivo.endswith('.jpg') or arquivo.endswith('.jpeg') or arquivo.endswith('.png'):
        # Caminho completo para a imagem
        caminho_imagem = os.path.join(origem_dir, arquivo)
        
        # Realizar transcrição do texto da imagem em português brasileiro
        texto = pytesseract.image_to_string(caminho_imagem, lang='por')
        
        # Criar o nome do arquivo de texto
        nome_texto = os.path.splitext(arquivo)[0] + '.txt'
        
        # Caminho completo para o arquivo de texto
        caminho_texto = os.path.join(destino_dir, nome_texto)
        
        # Salvar o arquivo de texto com codificação utf-8
        with open(caminho_texto, 'w', encoding='utf-8') as arquivo_texto:
            arquivo_texto.write(texto)
        
        # Copiar a imagem para a pasta de destino
        caminho_imagem_destino = os.path.join(destino_dir, arquivo)
        shutil.copy2(caminho_imagem, caminho_imagem_destino)
        
        # Renomear a imagem
        caminho_imagem_renomeada = os.path.join(destino_dir, nome_texto.replace('.txt', '.jpg'))
        os.rename(caminho_imagem_destino, caminho_imagem_renomeada)

# Loop through the text files in the destination directory
for arquivo in os.listdir(destino_dir):
    # Check if it is a text file
    if arquivo.endswith('.txt'):
        # Full path to the text file
        caminho_texto = os.path.join(destino_dir, arquivo)
        
        # Read the text from the file with utf-8 encoding
        with open(caminho_texto, 'r', encoding='utf-8') as arquivo_texto:
            texto = arquivo_texto.read()
        
        # Process the text with spaCy
        doc = nlp(texto)
        
        # Extract named entities
        entidades = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Print the named entities
        print(f'Named entities in {arquivo}:')
        print(entidades)

# Exibir mensagem de conclusão
msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setWindowTitle('Concluído')
msg.setText('Processo concluído com sucesso!')
msg.exec_()
