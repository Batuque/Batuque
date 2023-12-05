import tkinter as tk
from tkinter import PhotoImage
import os
import subprocess
import sys

def tocar():
    # Subprocess para executar o script Batuque.py
    script_path = os.path.abspath("Batuque.py")
    python_path = sys.executable
    result = subprocess.run([python_path, script_path], capture_output=True)
    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))

# Criar a janela principal
root = tk.Tk()
root.title("Batuque")

# Configurar a tela cheia
largura = root.winfo_screenwidth()
altura = root.winfo_screenheight()
root.geometry(f"{largura}x{altura}+0+0")

# Carregar as imagens
background_image = PhotoImage(file="Images/tela inicial/imagem_de_fundo.png")

# Carregar a imagem da logo com fundo transparente
logo_image = PhotoImage(file="Images/tela inicial/logo.png")

# Configurar a imagem de fundo
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Configurar o logo no meio da tela
logo_label = tk.Label(root, image=logo_image, bg="#000000")  # Configurar a cor de fundo como transparente
logo_label.place(relx=0.5, rely=0.3, anchor="center")

# Carregar a imagem do botão com fundo transparente
button_image = PhotoImage(file="Images/tela inicial/button.png")

# Configurar o botão
button = tk.Button(
    root,
    image=button_image,
    text="Tocar",
    compound="center",
    command=tocar,
    fg="white",
    highlightthickness=0,  # Remover a borda ao redor do botão
    bd=0,  # Remover a borda ao redor do botão (versões mais antigas do Tkinter)
    bg="#000000",  # Configurar a cor de fundo como transparente
    font=("Montserrat", 20, "bold")  # Fonte em negrito e tamanho 20
)
button.place(relx=0.5, rely=0.65, anchor="center")

# Executar o loop principal
root.mainloop()
