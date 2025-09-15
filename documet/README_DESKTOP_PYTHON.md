# 🍕 Sabore Desktop - Versão Python com PyQt5

> Versão desktop do aplicativo Sabore desenvolvida em Python com PyQt5, focada na gestão de empresas (restaurantes).

## 📋 Funcionalidades Implementadas

### ✅ Funcionalidades Principais
- **Cadastro de empresas (restaurantes)**
- **Visualização de restaurantes na página inicial**
- **Cadastro de pedidos no cardápio**
- **Upload de PDF do cardápio**
- **Upload de imagem do cardápio**
- **Edição de dados (restaurante e cardápio)**
- **Integração com backend Java existente**

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **PyQt5** - Interface gráfica
- **requests** - Comunicação com API
- **Pillow (PIL)** - Manipulação de imagens
- **PyPDF2** - Manipulação de PDFs
- **sqlite3** - Cache local (opcional)

---

## 📦 Instalação e Configuração

### 1. Pré-requisitos
```bash
# Instalar Python 3.8+ (se não tiver)
# Windows: https://www.python.org/downloads/
# Linux: sudo apt-get install python3 python3-pip
# macOS: brew install python3

# Verificar versão
python --version
```

### 2. Instalar Dependências
```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install PyQt5 requests Pillow PyPDF2
```

### 3. Configuração do Backend
```bash
# Criar arquivo .env na raiz do projeto
echo "API_BASE_URL=http://localhost:8080" > .env
```

---

## 🏗️ Estrutura do Projeto

```
sabore-desktop/
├── main.py                 # Arquivo principal
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configurações da aplicação
│   └── database.py         # Configuração de banco local
├── api/
│   ├── __init__.py
│   ├── client.py           # Cliente HTTP para API
│   ├── restaurante.py      # API de restaurantes
│   └── item_restaurante.py # API de itens do cardápio
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Janela principal
│   ├── login_window.py     # Tela de login
│   ├── cadastro_window.py  # Tela de cadastro
│   ├── dashboard_window.py # Dashboard da empresa
│   └── components/         # Componentes reutilizáveis
│       ├── __init__.py
│       ├── file_upload.py  # Componente de upload
│       └── item_card.py    # Card de item do cardápio
├── utils/
│   ├── __init__.py
│   ├── file_handler.py     # Manipulação de arquivos
│   └── validators.py       # Validações
├── assets/
│   ├── icons/              # Ícones da aplicação
│   └── styles/             # Estilos CSS
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

---

## 🚀 Como Executar

### 1. Preparar o Ambiente
```bash
# Clonar ou criar o projeto
mkdir sabore-desktop
cd sabore-desktop

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Backend
```bash
# Certifique-se que o backend Java está rodando
# URL padrão: http://localhost:8080
```

### 3. Executar Aplicação
```bash
# Executar aplicação principal
python main.py
```

---

## 📱 Telas e Funcionalidades

### 1. Tela de Login
- **Arquivo:** `ui/login_window.py`
- **Funcionalidades:**
  - Login com email e senha
  - Validação de campos
  - Integração com API `/restaurantes/login`
  - Redirecionamento para dashboard

### 2. Tela de Cadastro
- **Arquivo:** `ui/cadastro_window.py`
- **Funcionalidades:**
  - Cadastro completo de restaurante
  - Validação de CNPJ
  - Upload de logo e banner
  - Integração com API `/restaurantes`

### 3. Dashboard Principal
- **Arquivo:** `ui/dashboard_window.py`
- **Funcionalidades:**
  - Visualização de dados do restaurante
  - Gestão de itens do cardápio
  - Upload de PDF do cardápio
  - Edição de informações

### 4. Gestão de Cardápio
- **Arquivo:** `ui/cardapio_window.py`
- **Funcionalidades:**
  - Adicionar/editar/remover itens
  - Upload de imagens dos pratos
  - Definição de preços
  - Categorização de itens

---

## 🔧 Configuração Detalhada

### 1. Arquivo de Configuração (`config/settings.py`)
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
    APP_NAME = "Sabore Desktop"
    APP_VERSION = "1.0.0"
    
    # Configurações de upload
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.gif']
    ALLOWED_PDF_TYPES = ['.pdf']
    
    # Configurações de interface
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600
```

### 2. Cliente API (`api/client.py`)
```python
import requests
import json
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Sabore-Desktop/1.0'
        })
    
    def login(self, email: str, senha: str) -> Dict[str, Any]:
        """Login do restaurante"""
        url = f"{self.base_url}/restaurantes/login"
        data = {"email": email, "senha": senha}
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def upload_file(self, file_path: str, tipo: str) -> str:
        """Upload de arquivo (logo, banner, cardápio)"""
        url = f"{self.base_url}/restaurantes/upload/{tipo}"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        
        response.raise_for_status()
        return response.json()['url']
```

### 3. Janela Principal (`ui/main_window.py`)
```python
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from .login_window import LoginWindow
from .dashboard_window import DashboardWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sabore Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central com navegação
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Inicializar telas
        self.login_window = LoginWindow(self)
        self.dashboard_window = DashboardWindow(self)
        
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.dashboard_window)
        
        # Mostrar tela de login inicialmente
        self.show_login()
    
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)
    
    def show_dashboard(self, restaurante_data):
        self.dashboard_window.load_data(restaurante_data)
        self.stacked_widget.setCurrentWidget(self.dashboard_window)
```

---

## 📁 Gestão de Arquivos

### 1. Upload de Imagens
```python
# ui/components/file_upload.py
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
import os

class FileUploadWidget(QWidget):
    file_selected = pyqtSignal(str)  # Sinal emitido quando arquivo é selecionado
    
    def __init__(self, title="Selecionar Arquivo", file_types="Imagens (*.jpg *.png)"):
        super().__init__()
        self.file_types = file_types
        self.selected_file = None
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)
        
        self.select_button = QPushButton("Escolher Arquivo")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)
        
        self.file_label = QLabel("Nenhum arquivo selecionado")
        layout.addWidget(self.file_label)
        
        self.preview_label = QLabel()
        layout.addWidget(self.preview_label)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo", "", self.file_types
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.file_selected.emit(file_path)
            
            # Preview para imagens
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
                self.preview_label.setPixmap(scaled_pixmap)
```

### 2. Upload de PDF
```python
# utils/file_handler.py
import PyPDF2
import os
from typing import Optional

class PDFHandler:
    @staticmethod
    def validate_pdf(file_path: str) -> bool:
        """Valida se o arquivo é um PDF válido"""
        try:
            with open(file_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_pdf_info(file_path: str) -> Optional[dict]:
        """Obtém informações do PDF"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return {
                    'pages': len(reader.pages),
                    'size': os.path.getsize(file_path),
                    'filename': os.path.basename(file_path)
                }
        except Exception:
            return None
```

---

## 🔌 Integração com API

### 1. Endpoints Utilizados

#### Restaurantes
```python
# Login
POST /restaurantes/login
{
    "email": "restaurante@email.com",
    "senha": "senha123"
}

# Cadastro
POST /restaurantes
{
    "nome": "Restaurante Exemplo",
    "cnpj": "12.345.678/0001-90",
    "email": "restaurante@email.com",
    "senha": "senha123",
    "telefone": "(11) 99999-9999",
    "rua": "Rua Exemplo",
    "numero": 123,
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01234-567",
    "descricao": "Restaurante especializado em...",
    "horario": "Seg-Sex: 11h-22h",
    "lotacao": 50,
    "site": "https://restaurante.com",
    "aceitaComunicacao": true,
    "aceitaMarketing": true,
    "aceitaProtecaoDados": true
}

# Buscar restaurante
GET /restaurantes/{id}

# Atualizar restaurante
PUT /restaurantes/{id}

# Upload de arquivos
POST /restaurantes/upload/{tipo}  # tipo: logo, banner, cardapio
```

#### Itens do Cardápio
```python
# Cadastrar item
POST /itens
{
    "nome": "X-Burger",
    "descricao": "Hambúrguer com queijo, alface e tomate",
    "preco": 25.90,
    "restaurante": {"id": 1}
}

# Listar itens por restaurante
GET /itens/restaurante/{restauranteId}

# Atualizar item
PUT /itens/{id}

# Deletar item
DELETE /itens/{id}

# Upload de imagem do item
POST /itens/upload
```

### 2. Tratamento de Erros
```python
# api/client.py
import requests
from typing import Dict, Any, Optional

class APIError(Exception):
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class APIClient:
    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Trata respostas da API"""
        try:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise APIError("Credenciais inválidas", 401)
            elif response.status_code == 403:
                raise APIError("Acesso negado", 403)
            elif response.status_code == 404:
                raise APIError("Recurso não encontrado", 404)
            elif response.status_code == 422:
                data = response.json()
                error_msg = data.get('message', 'Dados inválidos')
                raise APIError(error_msg, 422)
            else:
                raise APIError(f"Erro {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Erro de conexão: {str(e)}")
```

---

## 🎨 Interface e UX

### 1. Estilo da Aplicação
```python
# assets/styles/main.qss
QMainWindow {
    background-color: #f8f9fa;
}

QPushButton {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #218838;
}

QPushButton:pressed {
    background-color: #1e7e34;
}

QLineEdit {
    padding: 8px;
    border: 2px solid #dee2e6;
    border-radius: 5px;
    font-size: 14px;
}

QLineEdit:focus {
    border-color: #28a745;
}

QLabel {
    color: #495057;
    font-size: 14px;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
```

### 2. Componentes Reutilizáveis
```python
# ui/components/item_card.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class ItemCard(QWidget):
    edit_clicked = pyqtSignal(int)  # ID do item
    delete_clicked = pyqtSignal(int)  # ID do item
    
    def __init__(self, item_data: dict):
        super().__init__()
        self.item_data = item_data
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Imagem do item
        if self.item_data.get('imagemUrl'):
            image_label = QLabel()
            pixmap = QPixmap(self.item_data['imagemUrl'])
            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
        
        # Nome do item
        name_label = QLabel(self.item_data['nome'])
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(name_label)
        
        # Descrição
        if self.item_data.get('descricao'):
            desc_label = QLabel(self.item_data['descricao'])
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Preço
        price_label = QLabel(f"R$ {self.item_data['preco']:.2f}")
        price_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 18px;")
        layout.addWidget(price_label)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Editar")
        edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.item_data['id']))
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Excluir")
        delete_btn.setStyleSheet("background-color: #dc3545;")
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.item_data['id']))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        # Estilo do card
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
```

---

## 🧪 Testes e Validação

### 1. Validações de Entrada
```python
# utils/validators.py
import re
from typing import Tuple, bool

class Validators:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Email inválido"
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> Tuple[bool, str]:
        """Valida CNPJ"""
        # Remove caracteres especiais
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        if len(cnpj) != 14:
            return False, "CNPJ deve ter 14 dígitos"
        
        # Validação do algoritmo de CNPJ
        if cnpj == cnpj[0] * 14:
            return False, "CNPJ inválido"
        
        # Validação dos dígitos verificadores
        soma = 0
        peso = 2
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        
        soma = 0
        peso = 2
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = peso + 1 if peso < 9 else 2
        
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        
        if int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2:
            return True, ""
        else:
            return False, "CNPJ inválido"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Valida telefone brasileiro"""
        phone = re.sub(r'[^0-9]', '', phone)
        
        if len(phone) < 10 or len(phone) > 11:
            return False, "Telefone deve ter 10 ou 11 dígitos"
        
        return True, ""
    
    @staticmethod
    def validate_cep(cep: str) -> Tuple[bool, str]:
        """Valida CEP"""
        cep = re.sub(r'[^0-9]', '', cep)
        
        if len(cep) != 8:
            return False, "CEP deve ter 8 dígitos"
        
        return True, ""
```

### 2. Testes Unitários
```python
# tests/test_validators.py
import unittest
from utils.validators import Validators

class TestValidators(unittest.TestCase):
    def test_validate_email(self):
        # Emails válidos
        self.assertTrue(Validators.validate_email("teste@email.com")[0])
        self.assertTrue(Validators.validate_email("usuario.teste@dominio.com.br")[0])
        
        # Emails inválidos
        self.assertFalse(Validators.validate_email("email_invalido")[0])
        self.assertFalse(Validators.validate_email("@email.com")[0])
        self.assertFalse(Validators.validate_email("email@")[0])
    
    def test_validate_cnpj(self):
        # CNPJ válido (exemplo)
        cnpj_valido = "11.222.333/0001-81"
        self.assertTrue(Validators.validate_cnpj(cnpj_valido)[0])
        
        # CNPJ inválido
        cnpj_invalido = "11.111.111/1111-11"
        self.assertFalse(Validators.validate_cnpj(cnpj_invalido)[0])

if __name__ == '__main__':
    unittest.main()
```

---

## 📦 Build e Distribuição

### 1. Arquivo requirements.txt
```
PyQt5==5.15.9
requests==2.31.0
Pillow==10.0.0
PyPDF2==3.0.1
python-dotenv==1.0.0
```

### 2. Script de Build (Windows)
```batch
@echo off
REM build.bat

echo Criando executável...

REM Instalar PyInstaller se não estiver instalado
pip install pyinstaller

REM Criar executável
pyinstaller --onefile --windowed --name "SaboreDesktop" main.py

echo Executável criado em dist/SaboreDesktop.exe
pause
```

### 3. Script de Build (Linux/macOS)
```bash
#!/bin/bash
# build.sh

echo "Criando executável..."

# Instalar PyInstaller se não estiver instalado
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed --name "SaboreDesktop" main.py

echo "Executável criado em dist/SaboreDesktop"
```

---

## 🔧 Configuração de Desenvolvimento

### 1. Estrutura de Desenvolvimento
```bash
# Criar estrutura de pastas
mkdir -p sabore-desktop/{config,api,ui,ui/components,utils,assets,assets/icons,assets/styles,tests}

# Criar arquivos principais
touch sabore-desktop/main.py
touch sabore-desktop/requirements.txt
touch sabore-desktop/.env
touch sabore-desktop/README.md

# Criar arquivos de configuração
touch sabore-desktop/config/__init__.py
touch sabore-desktop/config/settings.py

# Criar arquivos da API
touch sabore-desktop/api/__init__.py
touch sabore-desktop/api/client.py
touch sabore-desktop/api/restaurante.py
touch sabore-desktop/api/item_restaurante.py

# Criar arquivos da interface
touch sabore-desktop/ui/__init__.py
touch sabore-desktop/ui/main_window.py
touch sabore-desktop/ui/login_window.py
touch sabore-desktop/ui/dashboard_window.py
touch sabore-desktop/ui/cadastro_window.py
touch sabore-desktop/ui/components/__init__.py
touch sabore-desktop/ui/components/file_upload.py
touch sabore-desktop/ui/components/item_card.py

# Criar arquivos utilitários
touch sabore-desktop/utils/__init__.py
touch sabore-desktop/utils/file_handler.py
touch sabore-desktop/utils/validators.py

# Criar arquivos de teste
touch sabore-desktop/tests/__init__.py
touch sabore-desktop/tests/test_validators.py
```

### 2. Ambiente de Desenvolvimento
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install pytest  # Para testes
pip install black   # Para formatação de código
pip install flake8  # Para linting

# Configurar pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

---

## 🚀 Deploy e Distribuição

### 1. Preparar para Distribuição
```bash
# Limpar cache e arquivos temporários
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Testar aplicação
python -m pytest tests/

# Criar executável
python build.py
```

### 2. Distribuição
```bash
# Windows
# O executável será criado em dist/SaboreDesktop.exe
# Criar instalador com Inno Setup ou similar

# Linux
# O executável será criado em dist/SaboreDesktop
# Criar pacote .deb ou .rpm

# macOS
# O executável será criado em dist/SaboreDesktop
# Criar .dmg com create-dmg
```

---

## 📞 Suporte e Manutenção

### 1. Logs e Debug
```python
# config/settings.py
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sabore_desktop.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2. Tratamento de Erros
```python
# main.py
import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

def exception_hook(exctype, value, traceback_obj):
    """Hook para capturar exceções não tratadas"""
    error_msg = ''.join(traceback.format_exception(exctype, value, traceback_obj))
    
    # Salvar no log
    logging.error(f"Exceção não tratada: {error_msg}")
    
    # Mostrar mensagem para o usuário
    QMessageBox.critical(None, "Erro", 
                        "Ocorreu um erro inesperado. Verifique o log para mais detalhes.")

# Configurar hook de exceção
sys.excepthook = exception_hook
```

---

## 🎯 Próximos Passos

### 1. Melhorias Futuras
- [ ] Sistema de notificações
- [ ] Backup automático de dados
- [ ] Relatórios e estatísticas
- [ ] Integração com sistemas de pagamento
- [ ] Modo offline com sincronização
- [ ] Temas personalizáveis
- [ ] Atalhos de teclado
- [ ] Suporte a múltiplos idiomas

### 2. Otimizações
- [ ] Cache de imagens
- [ ] Lazy loading de componentes
- [ ] Compressão de uploads
- [ ] Validação em tempo real
- [ ] Autocomplete de endereços

---

## 📚 Recursos Adicionais

### Links Úteis
- [Documentação PyQt5](https://doc.qt.io/qtforpython/)
- [Tutorial PyQt5](https://www.pythonguis.com/tutorials/)
- [Requests Library](https://requests.readthedocs.io/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

### Comunidade
- [PyQt Forum](https://forum.qt.io/category/39/pyqt)
- [Stack Overflow - PyQt](https://stackoverflow.com/questions/tagged/pyqt5)
- [GitHub - PyQt Examples](https://github.com/topics/pyqt5)

---

**🎉 Agora você tem um guia completo para criar a versão desktop do Sabore em Python com PyQt5!**
