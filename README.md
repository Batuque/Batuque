# Batuque

O projeto Batuque é uma aplicação que utiliza visão computacional para detectar cores em tempo real através da câmera e reproduzir sons de instrumentos de percussão com base nas cores detectadas. A interface gráfica é gerenciada com a biblioteca Pygame, proporcionando uma tela inicial interativa e menus de configuração.

## 🔨 Funcionalidades do Projeto

- **Detecção de Cores:** Detecta cores específicas na imagem da câmera usando o espaço de cor HSV e aplica máscaras para identificar essas cores.
- **Reprodução de Sons:** Toca sons de instrumentos de percussão quando a cor correspondente é detectada em regiões de interesse (ROIs) pré-definidas.
- **Sobreposição de Imagens:** Exibe imagens transparentes sobre as regiões detectadas para representar visualmente os instrumentos.
- **Interface Gráfica:** Oferece uma tela inicial com botões de controle, um menu de configurações, e uma tela de carregamento.
- **Controle de Volume e Resolução:** Permite ajustar o volume da música e a resolução da tela através do menu de configurações.

### Exemplo Visual do Projeto
![Screenshot 2024-08-11 211550](https://github.com/user-attachments/assets/a8d3dca2-70ed-4246-8350-34b1ec0b187b)
![Screenshot 2024-08-11 225320](https://github.com/user-attachments/assets/e3ebd3e8-0319-49c8-b83f-d77ef9b7bf95)
![image](https://github.com/user-attachments/assets/c1a1b929-dbf9-4468-a144-8868e009d5ed)

## ✔️ Técnicas e Tecnologias Utilizadas

- **OpenCV:** Para captura de vídeo e processamento de imagens, incluindo a detecção de cores e a sobreposição de imagens.
- **Pygame:** Para criar a interface gráfica, gerenciar eventos e reproduzir sons.
- **Python:** Linguagem de programação usada para desenvolver a aplicação.

## 📁 Estrutura do Projeto

- `screens/`
    - `menu_resolucao.py`: Script para configurar a resolução da tela.
    - `menu_volume.py`: Script para ajustar o volume do áudio.
    - `telaLogin.py`: Script para a tela de login.
    - `telaRegistro.py`: Script para a tela de registro.
- `src/`
    - `Images/`: Contém as imagens utilizadas na interface gráfica.
    - `sounds/`: Contém os arquivos de áudio para os instrumentos.
    - `batuque.py`: Script principal que realiza a detecção de cores e a reprodução de sons.
    - `interface.py`: Gerencia a interface gráfica com Pygame, incluindo a tela inicial e menus.
- `.gitignore`: Arquivo que especifica quais arquivos e diretórios devem ser ignorados pelo Git.
- `LICENSE`: Arquivo de licença do projeto.
- `README.md`: Documentação do projeto.
- `requirements.txt`: Lista as dependências do projeto.
- `rodar_batuque.py`: Script para rodar o projeto Batuque.
- `teste_cor_alvo.py`: Script para testar a detecção de cores.

## 🌐 Deploy

Para executar o projeto localmente, siga os passos abaixo:

1. **Instale as Dependências:**
   Execute o comando `pip install -r requirements.txt` para instalar as dependências necessárias.

2. **Prepare os Recursos:**
   Certifique-se de que as imagens e os sons estão no diretório `src/Images` e `src/sounds`, respectivamente.

3. **Execute o Projeto:**
   Execute o script `interface.py` para iniciar a aplicação.
