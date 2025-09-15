# =============================================================================
# ARQUIVO PRINCIPAL DA APLICAÇÃO - DASHBOARD SABORÊ
# =============================================================================
# Este arquivo contém a classe principal da aplicação que gerencia toda a
# interface gráfica do dashboard, incluindo navegação, layout e integração
# com os componentes de gráficos, analytics e configurações.

# =============================================================================
# IMPORTAÇÕES NECESSÁRIAS
# =============================================================================

# Importações do PyQt5 para interface gráfica
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Importações dos módulos customizados do projeto
from charts import SaboreCharts, AnimatedCard          # Gráficos e cartões
from analytics import SaboreAnalytics                  # Análises de dados
from config_widget import ConfiguracoesSaborApp       # Widget de configurações
from api_client import SaboreAPIClient                # Cliente da API
from workers import DataWorker                        # Worker para carregamento assíncrono

# Importações padrão do Python
from datetime import datetime
import pandas as pd


# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =============================================================================
class ModernSaboreApp(QMainWindow):
    """
    Classe principal da aplicação Saborê Dashboard.
    
    Esta classe herda de QMainWindow e gerencia toda a interface do dashboard,
    incluindo:
    - Sidebar de navegação
    - Área de conteúdo principal
    - Cartões de métricas
    - Gráficos interativos
    - Sistema de abas
    - Carregamento de dados
    
    A aplicação é dividida em seções principais:
    1. Dashboard - Visão geral com métricas e gráficos
    2. Vendas - Gestão de vendas
    3. Produtos - Análise de produtos
    4. Analytics - Analytics avançado
    5. Configurações - Configurações do sistema
    """
    
    def __init__(self, api_client: SaboreAPIClient):
        """
        Inicializa a aplicação principal.
        
        Args:
            api_client (SaboreAPIClient): Cliente para comunicação com a API
        """
        super().__init__()
        
        # ===== CONFIGURAÇÃO INICIAL DA JANELA =====
        self.api_client = api_client  # Armazena referência ao cliente da API
        self.setWindowTitle("Saborê Dashboard - Gestão Inteligente")
        self.setGeometry(100, 100, 1200, 700)  # Define posição e tamanho da janela (reduzido)
        
        # ===== INICIALIZAÇÃO DA INTERFACE =====
        self.setup_ui()        # Configura todos os elementos da interface
        self.load_initial_data()  # Carrega dados iniciais do dashboard

    # =============================================================================
    # CONFIGURAÇÃO DA INTERFACE DO USUÁRIO (UI)
    # =============================================================================
    
    def setup_ui(self):
        """
        Configura toda a interface do usuário da aplicação.
        
        Este método é responsável por:
        1. Criar o widget central da janela
        2. Configurar o layout principal (horizontal)
        3. Criar a sidebar de navegação
        4. Criar a área de conteúdo principal
        5. Aplicar o tema visual da aplicação
        """
        # ===== WIDGET CENTRAL =====
        # Cria o widget principal que ocupará toda a área da janela
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # ===== LAYOUT PRINCIPAL =====
        # Cria layout horizontal para dividir sidebar (esquerda) e conteúdo (direita)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margens externas
        self.main_layout.setSpacing(0)                    # Remove espaçamento entre elementos
        
        # ===== CONFIGURAÇÃO DOS COMPONENTES =====
        self.setup_sidebar()      # Configura barra lateral de navegação
        self.setup_content_area() # Configura área principal de conteúdo
        self.apply_sabore_theme() # Aplica tema visual personalizado

    def setup_sidebar(self):
        """
        Configura a barra lateral de navegação da aplicação.
        
        A sidebar contém:
        - Logo da aplicação
        - Menu de navegação com ícones
        - Informações de versão
        
        Cor padrão: #D29A3A (dourado/âmbar)
        """
        # ===== CONFIGURAÇÃO BÁSICA DA SIDEBAR =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)  # Largura reduzida para dar mais espaço aos gráficos
        self.sidebar.setStyleSheet("background-color: #2c5530; border-right: none;")  # Cor dourada
        
        # ===== LAYOUT DA SIDEBAR =====
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)  # Margens internas
        sidebar_layout.setSpacing(10)                       # Espaçamento entre elementos

        # ===== LOGO DA APLICAÇÃO =====
        # Cria layout horizontal para ícone e texto do logo
        logo_layout = QHBoxLayout()
        
        # Ícone do coco (emoji)
        logo_icon = QLabel("🍽️")
        logo_icon.setFont(QFont("Segoe UI Emoji", 32))
        
        # Texto "Saborê"
        logo_text = QLabel("Saborê")
        logo_text.setFont(QFont("Segoe UI", 20, QFont.Bold))
        logo_text.setStyleSheet("color: white;")  # Texto branco para contraste
        
        # Monta o logo
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()  # Empurra elementos para a esquerda
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacing(40)  # Espaço entre logo e menu

        # ===== MENU DE NAVEGAÇÃO =====
        # Dicionário para armazenar referências dos botões de navegação
        self.nav_buttons = {}
        
        # Define opções do menu com ícones e textos
        nav_options = {
            "dashboard": ("🏠", "Dashboard"),      # Página principal
            "vendas": ("💰", "Vendas"),           # Gestão de vendas
            "produtos": ("🍕", "Produtos"),       # Análise de produtos
            "analytics": ("📊", "Analytics"),     # Analytics avançado
            "config": ("⚙️", "Configurações")     # Configurações do sistema
        }
        
        # Cria botões de navegação
        for key, (icon, text) in nav_options.items():
            btn = QPushButton(f"{icon}  {text}")  # Combina ícone e texto
            btn.setStyleSheet(self.get_nav_button_style())  # Aplica estilo
            btn.clicked.connect(lambda _, k=key: self.switch_content(k))  # Conecta ação
            sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn  # Armazena referência

        # ===== INFORMAÇÕES DE VERSÃO =====
        sidebar_layout.addStretch()  # Empurra versão para o final
        version_label = QLabel("v2.0.0\nSistema Operacional")
        version_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 11px;")  # Texto semi-transparente
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        # ===== FINALIZAÇÃO DA SIDEBAR =====
        self.main_layout.addWidget(self.sidebar)  # Adiciona sidebar ao layout principal

    def setup_content_area(self):
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header melhorado com melhor legibilidade
        header = QFrame()
        header.setFixedHeight(80)  # Altura aumentada
        header.setStyleSheet("""
            background-color: #FFFFFF; 
            border-bottom: 2px solid #E0E0E0;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 15, 30, 15)  # Margens aumentadas

        # Título da página com melhor estilo
        self.page_title = QLabel("Dashboard")
        self.page_title.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Fonte maior
        self.page_title.setStyleSheet("""
            color: #2c5530;
            padding: 8px 0px;
        """)

        # Status de conexão com melhor contraste
        self.connection_status = QLabel("🟢 Online")
        self.connection_status.setFont(QFont("Segoe UI", 11, QFont.Bold))  # Fonte maior
        self.connection_status.setStyleSheet("""
            color: #4a7c59;
            padding: 8px 12px;
            background-color: #f0f8f0;
            border-radius: 20px;
            border: 1px solid #4a7c59;
        """)

        # Botão de atualizar com melhor design
        self.refresh_btn = QPushButton("↻ Atualizar")
        self.refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.refresh_btn.setMinimumHeight(40)  # Altura adequada
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7c59;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #3a6b4a;
            }
            QPushButton:pressed {
                background-color: #2c5530;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_data)

        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        header_layout.addWidget(self.connection_status)
        header_layout.addSpacing(20)  # Espaçamento aumentado
        header_layout.addWidget(self.refresh_btn)
        content_layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            background-color: #F8F9FA; 
            border: none;
        """)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content_stack = QWidget()
        self.content_stack.setStyleSheet("background-color: #F8F9FA;")
        content_stack_layout = QVBoxLayout(self.content_stack)
        content_stack_layout.setContentsMargins(15, 15, 15, 15)  # Margens reduzidas
        content_stack_layout.setSpacing(15)  # Espaçamento reduzido entre elementos

        self.dashboard_widget = self.create_dashboard_content()
        self.vendas_widget = self.create_vendas_content()
        self.produtos_widget = self.create_produtos_content()
        self.analytics_widget = self.create_analytics_content()
        self.config_widget = ConfiguracoesSaborApp(self)

        content_stack_layout.addWidget(self.dashboard_widget)
        content_stack_layout.addWidget(self.vendas_widget)
        content_stack_layout.addWidget(self.produtos_widget)
        content_stack_layout.addWidget(self.analytics_widget)
        content_stack_layout.addWidget(self.config_widget)

        self.vendas_widget.hide()
        self.produtos_widget.hide()
        self.analytics_widget.hide()
        self.config_widget.hide()

        scroll_area.setWidget(self.content_stack)
        content_layout.addWidget(scroll_area)
        self.main_layout.addWidget(content_container)

    # ---------- ESTILOS ----------
    def get_nav_button_style(self):
        return """
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """

    def get_action_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """

    def apply_sabore_theme(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

    def switch_content(self, section):
        pages = {
            "dashboard": "Dashboard",
            "vendas": "Gestão de Vendas",
            "produtos": "Análise de Produtos",
            "analytics": "Analytics Avançado",
            "config": "Configurações"
        }
        self.page_title.setText(pages.get(section, "Dashboard"))

        widgets = {
            "dashboard": self.dashboard_widget,
            "vendas": self.vendas_widget,
            "produtos": self.produtos_widget,
            "analytics": self.analytics_widget,
            "config": self.config_widget
        }

        for w in widgets.values():
            w.hide()
        if section in widgets:
            widgets[section].show()

        for key, btn in self.nav_buttons.items():
            btn.setStyleSheet(self.get_nav_button_style() + (
                "QPushButton { background: rgba(255, 255, 255, 0.2); }" if key == section else ""))

    # ---------- CONTEÚDO ----------
    def create_dashboard_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # ===== LAYOUT HORIZONTAL PARA CARDS LADO A LADO =====
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(8)  # Espaçamento reduzido entre cards
        metrics_layout.setContentsMargins(5, 5, 5, 5)  # Margens reduzidas

        # ===== CARDS COM TEXTO CORRIGIDO (SEM "DE HOJE") =====
        self.revenue_card = AnimatedCard("Faturamento Total", "R$ 0,00", "💰", ["#4a7c59", "#6b8e23"], "soma de todas as vendas")
        self.orders_card = AnimatedCard("Total de Pedidos", "0", "📋", ["#ff8c00", "#ffa500"], "pedidos realizados")
        self.avg_ticket_card = AnimatedCard("Ticket Médio", "R$ 0,00", "🎯", ["#8b4513", "#cd853f"], "valor médio por pedido")
        self.growth_card = AnimatedCard("Crescimento", "0%", "📈", ["#2e8b57", "#3cb371"], "vs. período anterior")

        # ===== ADICIONA CARDS LADO A LADO =====
        metrics_layout.addWidget(self.revenue_card)
        metrics_layout.addWidget(self.orders_card)
        metrics_layout.addWidget(self.avg_ticket_card)
        metrics_layout.addWidget(self.growth_card)
        layout.addLayout(metrics_layout)

        charts_container = QFrame()
        charts_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
                border: 2px solid #e0e0e0;
            }
        """)
        charts_layout = QVBoxLayout(charts_container)
        charts_layout.setContentsMargins(15, 15, 15, 15)  # Margens reduzidas
        charts_layout.setSpacing(10)  # Espaçamento reduzido entre elementos

        self.charts_tabs = QTabWidget()
        self.charts_tabs.setFont(QFont("Segoe UI", 11, QFont.Bold))  # Fonte melhorada
        self.charts_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                color: #666666;
                padding: 12px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #4a7c59;
                border-bottom: 2px solid #4a7c59;
            }
            QTabBar::tab:hover {
                background-color: #e8f5e8;
                color: #4a7c59;
            }
        """)
        
        self.vendas_chart = SaboreCharts()
        self.produtos_chart = SaboreCharts()
        self.categorias_chart = SaboreCharts()

        # Aba Vendas
        vendas_widget = QWidget()
        vv = QVBoxLayout(vendas_widget)
        vv.setContentsMargins(10, 10, 10, 10)  # Margens adequadas
        vv.addWidget(self.vendas_chart.canvas)
        self.charts_tabs.addTab(vendas_widget, "📈 Vendas")

        # Aba Produtos
        produtos_widget = QWidget()
        pv = QVBoxLayout(produtos_widget)
        pv.setContentsMargins(10, 10, 10, 10)  # Margens adequadas
        pv.addWidget(self.produtos_chart.canvas)
        self.charts_tabs.addTab(produtos_widget, "🍕 Produtos")

        # Aba Categorias
        categorias_widget = QWidget()
        cv = QVBoxLayout(categorias_widget)
        cv.setContentsMargins(10, 10, 10, 10)  # Margens adequadas
        cv.addWidget(self.categorias_chart.canvas)
        self.charts_tabs.addTab(categorias_widget, "🏷️ Categorias")

        charts_layout.addWidget(self.charts_tabs)
        layout.addWidget(charts_container)

        return widget

    def create_vendas_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        title = QLabel("💰 Gestão de Vendas")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #4a7c59; margin-bottom: 20px;")
        layout.addWidget(title)

        self.vendas_table = QTableWidget()
        self.vendas_table.setColumnCount(6)
        self.vendas_table.setHorizontalHeaderLabels(["Data", "Pedido #", "Cliente", "Produtos", "Status", "Valor"])
        self.vendas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vendas_table.setMinimumHeight(400)
        layout.addWidget(self.vendas_table)

        return widget

    def create_produtos_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        title = QLabel("🍕 Análise de Produtos")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #4a7c59; margin-bottom: 20px;")
        layout.addWidget(title)

        self.produtos_main_chart = SaboreCharts()
        layout.addWidget(self.produtos_main_chart.canvas)  # ✅ CORRETO

        return widget

    def create_analytics_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        title = QLabel("📊 Analytics Avançado")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #4a7c59; margin-bottom: 20px;")
        layout.addWidget(title)

        self.temporal_chart = SaboreCharts()
        layout.addWidget(self.temporal_chart.canvas)  # ✅ CORRETO

        return widget

    # ---------- DADOS ----------
    def load_initial_data(self):
        self.connection_status.setText("🟡 Carregando...")
        self.refresh_btn.setEnabled(False)
        self.worker = DataWorker(self.api_client)
        self.worker.data_loaded.connect(self.on_data_loaded)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

    def refresh_data(self):
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("↻ Carregando...")
        self.connection_status.setText("🟡 Atualizando...")
        self.load_initial_data()

    def on_data_loaded(self, data):
        self.current_data = data
        vendas_data = data.get('vendas_detalhadas', [])
        self.analytics = SaboreAnalytics(vendas_data)
        self.update_dashboard_metrics(data)
        self.update_charts(data)
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("↻ Atualizar")
        self.connection_status.setText("🟢 Online")

    def on_error(self, error):
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("↻ Tentar Novamente")
        self.connection_status.setText("🔴 Erro")
        QMessageBox.warning(self, "Erro de Conexão", f"Não foi possível carregar os dados:\n{error}")

    def update_dashboard_metrics(self, data):
        if self.analytics:
            metricas = self.analytics.calcular_metricas_principais()
        else:
            metricas = data.get('metricas_principais', {})

        vendas_total = metricas.get('vendas_totais', 0)
        self.revenue_card.update_valor(f"R$ {vendas_total:,.2f}")

        total_pedidos = metricas.get('total_pedidos', 0)
        self.orders_card.update_valor(str(total_pedidos))

        ticket_medio = metricas.get('ticket_medio', 0)
        self.avg_ticket_card.update_valor(f"R$ {ticket_medio:,.2f}")

        crescimento = metricas.get('crescimento_percentual', 0)
        self.growth_card.update_valor(f"{crescimento:.1f}%")

    def update_charts(self, data):
        try:
            if self.analytics:
                vendas_por_dia = self.analytics.vendas_por_periodo('dia')
            else:
                vendas_por_dia = data.get('vendas_por_dia', {})

            # Criar gráfico de vendas por tempo
            if vendas_por_dia:
                self.vendas_chart.criar_grafico_vendas_tempo(vendas_por_dia, "Evolução de Vendas")

            produtos = data.get('itens_mais_vendidos', [])
            if produtos:
                self.produtos_chart.criar_grafico_barras_produtos(produtos, "Top Produtos")
                
                # Criar dados de categorias para o gráfico de pizza
                categorias = {}
                for produto in produtos:
                    categoria = produto.get('categoria', 'Outros')
                    if categoria not in categorias:
                        categorias[categoria] = 0
                    categorias[categoria] += produto.get('quantidade_vendida', produto.get('quantidade_total', 0))
                
                if categorias:
                    self.categorias_chart.criar_grafico_pizza_categorias(categorias, "Vendas por Categoria")
        except Exception as e:
            print(f"Erro ao atualizar gráficos: {e}")