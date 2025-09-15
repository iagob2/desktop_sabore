# =============================================================================
# WIDGET DE CONFIGURAÇÕES DO SISTEMA
# =============================================================================
# Este arquivo contém a classe responsável por gerenciar as configurações
# da aplicação, incluindo configurações da API, preferências do usuário
# e outras opções do sistema.

# =============================================================================
# IMPORTAÇÕES NECESSÁRIAS
# =============================================================================

# Importações do PyQt5 para interface gráfica
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# =============================================================================
# CLASSE DE CONFIGURAÇÕES DO SISTEMA
# =============================================================================
class ConfiguracoesSaborApp(QWidget):
    """
    Classe responsável por gerenciar as configurações da aplicação.
    
    Esta classe permite ao usuário configurar:
    - URL da API
    - Preferências de interface
    - Configurações de conexão
    - Outras opções do sistema
    
    As configurações são salvas automaticamente usando QSettings
    e persistem entre sessões da aplicação.
    """
    
    def __init__(self, main_app):
        """
        Inicializa o widget de configurações.
        
        Args:
            main_app: Referência para a aplicação principal
        """
        super().__init__()
        
        # ===== CONFIGURAÇÃO INICIAL =====
        self.main_app = main_app  # Armazena referência para a app principal
        self.settings = QSettings('Sabore', 'Dashboard')  # Sistema de configurações persistente
        
        # ===== INICIALIZAÇÃO DA INTERFACE =====
        self.setup_ui()  # Configura todos os elementos da interface

    def setup_ui(self):
        """
        Configura a interface do widget de configurações.
        
        Este método cria:
        1. Layout principal com espaçamento adequado
        2. Título da seção
        3. Área de rolagem para configurações
        4. Grupos de configurações organizados
        5. Campos de entrada e botões de ação
        """
        # ===== LAYOUT PRINCIPAL =====
        # Cria layout vertical para organizar elementos
        layout = QVBoxLayout(self)
        layout.setSpacing(20)           # Espaçamento entre elementos
        layout.setContentsMargins(30, 30, 30, 30)  # Margens externas
        
        # Título principal com melhor contraste
        title = QLabel("⚙️ Configurações do Sistema")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("""
            color: #2c5530; 
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #4a7c59;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Área de rolagem com melhor estrutura
        scroll = QScrollArea()
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #e0e0e0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4a7c59;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3a6b4a;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(25)  # Espaçamento entre grupos
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Grupo de configurações da API com melhor layout
        api_group = QGroupBox("🔗 Configurações da API")
        api_group.setFont(QFont("Segoe UI", 14, QFont.Bold))
        api_group.setStyleSheet("""
            QGroupBox {
                color: #2c5530;
                font-weight: bold;
                border: 2px solid #4a7c59;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: #ffffff;
            }
        """)
        
        api_layout = QVBoxLayout(api_group)
        api_layout.setSpacing(15)  # Espaçamento entre elementos do grupo
        api_layout.setContentsMargins(20, 25, 20, 20)

        # Label da URL com melhor legibilidade
        url_label = QLabel("URL da API:")
        url_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        url_label.setStyleSheet("""
            color: #333333;
            padding: 5px 0px;
        """)
        api_layout.addWidget(url_label)

        # Campo de entrada da URL com melhor estilo
        self.api_url_edit = QLineEdit(self.settings.value('api_url', 'https://api.sabore.com.br'))
        self.api_url_edit.setFont(QFont("Segoe UI", 11))
        self.api_url_edit.setMinimumHeight(45)  # Altura adequada
        self.api_url_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 11pt;
                background-color: #ffffff;
                color: #333333;
                selection-background-color: #4a7c59;
            }
            QLineEdit:focus {
                border-color: #4a7c59;
                background-color: #f8fff8;
            }
            QLineEdit:hover {
                border-color: #6b8e23;
            }
        """)
        api_layout.addWidget(self.api_url_edit)

        # Botão de salvar com melhor design
        save_button = QPushButton("💾 Salvar Configurações")
        save_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        save_button.setMinimumHeight(45)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a7c59;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a6b4a;
            }
            QPushButton:pressed {
                background-color: #2c5530;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        api_layout.addWidget(save_button)

        # Adicionar grupo ao layout de rolagem
        scroll_layout.addWidget(api_group)
        
        # Adicionar espaçador para empurrar conteúdo para o topo
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

    def save_settings(self):
        """
        Salva as configurações do usuário.
        
        Este método:
        1. Armazena as configurações usando QSettings
        2. Exibe mensagem de confirmação
        3. Persiste as configurações entre sessões
        
        As configurações são salvas automaticamente no registro do Windows
        ou em arquivos de configuração no Linux/Mac.
        """
        # ===== SALVAMENTO DAS CONFIGURAÇÕES =====
        # Salva URL da API nas configurações persistentes
        self.settings.setValue('api_url', self.api_url_edit.text())
        
        # ===== CONFIRMAÇÃO PARA O USUÁRIO =====
        # Exibe mensagem de sucesso
        QMessageBox.information(self, "Configurações", "Configurações salvas com sucesso!")