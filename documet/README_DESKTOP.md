---

## 🛠️ Como você pode criar a versão Desktop em Python

A versão desktop do Sabore é focada em **relatórios e estatísticas** para gestores de restaurantes, complementando o app mobile. Ela não replicará funcionalidades básicas como cadastro e upload, mas sim oferecerá análises avançadas dos dados.

### Passo 1 – Preparar ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar todas as dependências necessárias
pip install requests PyQt5 matplotlib reportlab openpyxl
```

**Explicação das bibliotecas:**
- `requests` - Para comunicação com a API Java
- `PyQt5` - Interface gráfica desktop
- `matplotlib` - Geração de gráficos e visualizações
- `reportlab` - Criação de relatórios em PDF
- `openpyxl` - Exportação de dados para Excel

### Passo 2 – Conectar ao backend Java

#### 2.1 Configuração da conexão com API
```python
# api/client.py
import requests
import json
from typing import Dict, List, Any

class SaboreAPIClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def get_pedidos(self, restaurante_id: int = None, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
        """Buscar todos os pedidos com filtros opcionais"""
        url = f"{self.base_url}/api/pedidos"
        params = {}
        
        if restaurante_id:
            params['restaurante_id'] = restaurante_id
        if data_inicio:
            params['data_inicio'] = data_inicio
        if data_fim:
            params['data_fim'] = data_fim
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar pedidos: {e}")
            return []
    
    def get_estatisticas_restaurante(self, restaurante_id: int) -> Dict[str, Any]:
        """Buscar estatísticas específicas do restaurante"""
        url = f"{self.base_url}/api/restaurantes/{restaurante_id}/estatisticas"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}
    
    def get_itens_mais_vendidos(self, restaurante_id: int, periodo: str = "30") -> List[Dict]:
        """Buscar itens mais vendidos nos últimos X dias"""
        url = f"{self.base_url}/api/restaurantes/{restaurante_id}/itens-vendidos"
        params = {'periodo': periodo}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar itens mais vendidos: {e}")
            return []

# Exemplo de uso:
client = SaboreAPIClient()
pedidos = client.get_pedidos()

if pedidos:
    print(f"Total de pedidos encontrados: {len(pedidos)}")
    for pedido in pedidos[:5]:  # Mostrar apenas os primeiros 5
        print(f"Pedido {pedido.get('id')}: R$ {pedido.get('valor_total', 0):.2f}")
```

#### 2.2 Tratamento de dados da API
```python
# utils/data_processor.py
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class DataProcessor:
    @staticmethod
    def calcular_vendas_totais(pedidos: List[Dict]) -> float:
        """Calcular total de vendas"""
        total = 0.0
        for pedido in pedidos:
            # Somar valor de cada item do pedido
            if 'itens' in pedido:
                for item in pedido['itens']:
                    total += item.get('valor', 0) * item.get('quantidade', 1)
            else:
                total += pedido.get('valor_total', 0)
        return total
    
    @staticmethod
    def agrupar_por_periodo(pedidos: List[Dict], tipo_periodo: str = 'dia') -> Dict[str, float]:
        """Agrupar vendas por período (dia, semana, mês)"""
        vendas_por_periodo = {}
        
        for pedido in pedidos:
            data_pedido = pedido.get('data_pedido')
            if not data_pedido:
                continue
                
            # Converter string para datetime
            try:
                if isinstance(data_pedido, str):
                    data = datetime.fromisoformat(data_pedido.replace('Z', '+00:00'))
                else:
                    data = data_pedido
                
                # Formatar chave baseada no tipo de período
                if tipo_periodo == 'dia':
                    chave = data.strftime('%Y-%m-%d')
                elif tipo_periodo == 'semana':
                    chave = f"{data.year}-S{data.isocalendar()[1]}"
                elif tipo_periodo == 'mes':
                    chave = data.strftime('%Y-%m')
                else:
                    chave = data.strftime('%Y-%m-%d')
                
                if chave not in vendas_por_periodo:
                    vendas_por_periodo[chave] = 0.0
                
                vendas_por_periodo[chave] += pedido.get('valor_total', 0)
                
            except Exception as e:
                print(f"Erro ao processar data: {e}")
                continue
        
        return dict(sorted(vendas_por_periodo.items()))
    
    @staticmethod
    def itens_mais_populares(pedidos: List[Dict], limite: int = 10) -> List[Dict]:
        """Encontrar itens mais vendidos"""
        contador_itens = {}
        
        for pedido in pedidos:
            if 'itens' in pedido:
                for item in pedido['itens']:
                    nome = item.get('nome', 'Item sem nome')
                    quantidade = item.get('quantidade', 1)
                    valor = item.get('valor', 0)
                    
                    if nome not in contador_itens:
                        contador_itens[nome] = {
                            'quantidade_total': 0,
                            'valor_total': 0,
                            'nome': nome
                        }
                    
                    contador_itens[nome]['quantidade_total'] += quantidade
                    contador_itens[nome]['valor_total'] += valor * quantidade
        
        # Ordenar por quantidade total e pegar os top N
        itens_ordenados = sorted(
            contador_itens.values(), 
            key=lambda x: x['quantidade_total'], 
            reverse=True
        )
        
        return itens_ordenados[:limite]
```

### Passo 3 – Criar interface desktop (PyQt5)

#### 3.1 Janela principal com abas
```python
# ui/main_window.py
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import sys

class SaboreDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.api_client = SaboreAPIClient()
        self.data_processor = DataProcessor()
        
    def initUI(self):
        self.setWindowTitle("Saborê - Relatórios e Estatísticas")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Header com título
        header = self.create_header()
        layout.addWidget(header)
        
        # Tabs para diferentes seções
        tabs = QTabWidget()
        
        # Aba 1: Dashboard
        dashboard_tab = self.create_dashboard_tab()
        tabs.addTab(dashboard_tab, "📊 Dashboard")
        
        # Aba 2: Vendas
        vendas_tab = self.create_vendas_tab()
        tabs.addTab(vendas_tab, "💰 Vendas")
        
        # Aba 3: Produtos
        produtos_tab = self.create_produtos_tab()
        tabs.addTab(produtos_tab, "🍕 Produtos")
        
        # Aba 4: Relatórios
        relatorios_tab = self.create_relatorios_tab()
        tabs.addTab(relatorios_tab, "📈 Relatórios")
        
        layout.addWidget(tabs)
        
        # Aplicar estilo
        self.apply_style()
    
    def create_header(self):
        """Criar header da aplicação"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Logo e título
        title_label = QLabel("🍽️ Saborê Desktop")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # Botão de atualização
        refresh_btn = QPushButton("🔄 Atualizar Dados")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        return header_widget
    
    def create_dashboard_tab(self):
        """Criar aba do dashboard principal"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Cards de estatísticas
        cards_layout = QHBoxLayout()
        
        # Card de vendas totais
        vendas_card = self.create_stat_card("Vendas Hoje", "R$ 0,00", "#e74c3c")
        cards_layout.addWidget(vendas_card)
        
        # Card de pedidos
        pedidos_card = self.create_stat_card("Pedidos Hoje", "0", "#f39c12")
        cards_layout.addWidget(pedidos_card)
        
        # Card de ticket médio
        ticket_card = self.create_stat_card("Ticket Médio", "R$ 0,00", "#27ae60")
        cards_layout.addWidget(ticket_card)
        
        # Card de crescimento
        crescimento_card = self.create_stat_card("Crescimento", "+0%", "#8e44ad")
        cards_layout.addWidget(crescimento_card)
        
        layout.addLayout(cards_layout)
        
        # Área para gráfico
        grafico_label = QLabel("📊 Gráfico de vendas será exibido aqui")
        grafico_label.setAlignment(Qt.AlignCenter)
        grafico_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #bdc3c7;
                border-radius: 10px;
                padding: 50px;
                margin: 20px;
                color: #7f8c8d;
                font-size: 16px;
            }
        """)
        layout.addWidget(grafico_label)
        
        return widget
    
    def create_stat_card(self, titulo: str, valor: str, cor: str):
        """Criar card de estatística"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {cor};
                border-radius: 10px;
                margin: 5px;
            }}
            QLabel {{
                color: white;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Arial", 12))
        titulo_label.setAlignment(Qt.AlignCenter)
        
        valor_label = QLabel(valor)
        valor_label.setFont(QFont("Arial", 20, QFont.Bold))
        valor_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(titulo_label)
        layout.addWidget(valor_label)
        
        return card
    
    def create_vendas_tab(self):
        """Criar aba de vendas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Controles de filtro
        filtros_layout = QHBoxLayout()
        
        filtro_periodo_btn = QPushButton("📅 Filtrar por Período")
        filtro_periodo_btn.clicked.connect(self.filtrar_periodo)
        
        exportar_btn = QPushButton("📤 Exportar Excel")
        exportar_btn.clicked.connect(self.exportar_vendas_excel)
        
        filtros_layout.addWidget(filtro_periodo_btn)
        filtros_layout.addWidget(exportar_btn)
        filtros_layout.addStretch()
        
        layout.addLayout(filtros_layout)
        
        # Tabela de vendas
        self.tabela_vendas = QTableWidget()
        self.tabela_vendas.setColumnCount(5)
        self.tabela_vendas.setHorizontalHeaderLabels([
            "Data", "Pedido", "Cliente", "Itens", "Valor Total"
        ])
        self.tabela_vendas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabela_vendas)
        
        return widget
    
    def refresh_data(self):
        """Atualizar dados da aplicação"""
        # Implementar lógica de atualização
        print("Atualizando dados...")
        self.carregar_dados_vendas()
    
    def filtrar_periodo(self):
        """Abrir diálogo de filtro por período"""
        print("Filtrar por período...")
    
    def exportar_vendas_excel(self):
        """Exportar dados de vendas para Excel"""
        print("Exportando para Excel...")

# Execução da aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SaboreDesktopApp()
    window.show()
    sys.exit(app.exec_())
```

### Passo 4 – Criar relatórios estatísticos

#### 4.1 Classe para cálculos estatísticos
```python
# analytics/statistics.py
from typing import List, Dict, Tuple
import statistics
from datetime import datetime, timedelta
import calendar

class SaboreAnalytics:
    def __init__(self, pedidos: List[Dict]):
        self.pedidos = pedidos
        self.processor = DataProcessor()
    
    def calcular_metricas_principais(self) -> Dict[str, float]:
        """Calcular métricas principais do negócio"""
        if not self.pedidos:
            return {
                'vendas_totais': 0.0,
                'ticket_medio': 0.0,
                'total_pedidos': 0,
                'crescimento_percentual': 0.0
            }
        
        vendas_totais = self.processor.calcular_vendas_totais(self.pedidos)
        total_pedidos = len(self.pedidos)
        ticket_medio = vendas_totais / total_pedidos if total_pedidos > 0 else 0.0
        
        # Calcular crescimento (comparar com período anterior)
        crescimento = self.calcular_crescimento_vendas()
        
        return {
            'vendas_totais': vendas_totais,
            'ticket_medio': ticket_medio,
            'total_pedidos': total_pedidos,
            'crescimento_percentual': crescimento
        }
    
    def calcular_crescimento_vendas(self, dias: int = 30) -> float:
        """Calcular crescimento de vendas comparado ao período anterior"""
        agora = datetime.now()
        periodo_atual = agora - timedelta(days=dias)
        periodo_anterior = periodo_atual - timedelta(days=dias)
        
        # Filtrar pedidos por período
        vendas_atual = []
        vendas_anterior = []
        
        for pedido in self.pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                
                if data_pedido >= periodo_atual:
                    vendas_atual.append(pedido)
                elif data_pedido >= periodo_anterior and data_pedido < periodo_atual:
                    vendas_anterior.append(pedido)
            except:
                continue
        
        total_atual = self.processor.calcular_vendas_totais(vendas_atual)
        total_anterior = self.processor.calcular_vendas_totais(vendas_anterior)
        
        if total_anterior == 0:
            return 100.0 if total_atual > 0 else 0.0
        
        crescimento = ((total_atual - total_anterior) / total_anterior) * 100
        return round(crescimento, 2)
    
    def horarios_pico(self) -> Dict[int, int]:
        """Identificar horários de pico de pedidos"""
        contador_horarios = {}
        
        for pedido in self.pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                hora = data_pedido.hour
                
                if hora not in contador_horarios:
                    contador_horarios[hora] = 0
                contador_horarios[hora] += 1
            except:
                continue
        
        return dict(sorted(contador_horarios.items()))
    
    def dias_semana_performance(self) -> Dict[str, float]:
        """Analisar performance por dia da semana"""
        vendas_por_dia = {}
        
        for pedido in self.pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                dia_semana = calendar.day_name[data_pedido.weekday()]
                
                if dia_semana not in vendas_por_dia:
                    vendas_por_dia[dia_semana] = 0.0
                
                vendas_por_dia[dia_semana] += pedido.get('valor_total', 0)
            except:
                continue
        
        return vendas_por_dia
    
    def analise_sazonalidade(self, meses: int = 12) -> Dict[str, float]:
        """Analisar sazonalidade de vendas por mês"""
        vendas_por_mes = {}
        
        for pedido in self.pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                mes_nome = calendar.month_name[data_pedido.month]
                
                if mes_nome not in vendas_por_mes:
                    vendas_por_mes[mes_nome] = 0.0
                
                vendas_por_mes[mes_nome] += pedido.get('valor_total', 0)
            except:
                continue
        
        return vendas_por_mes

# Exemplo de uso
def gerar_relatorio_estatistico():
    """Exemplo de como gerar relatório completo"""
    # Buscar dados
    client = SaboreAPIClient()
    pedidos = client.get_pedidos()
    
    if not pedidos:
        print("Nenhum pedido encontrado")
        return
    
    # Análises
    analytics = SaboreAnalytics(pedidos)
    
    print("=== RELATÓRIO DE VENDAS ===")
    print()
    
    # Métricas principais
    metricas = analytics.calcular_metricas_principais()
    print(f"💰 Vendas Totais: R$ {metricas['vendas_totais']:,.2f}")
    print(f"🛒 Total de Pedidos: {metricas['total_pedidos']}")
    print(f"🎯 Ticket Médio: R$ {metricas['ticket_medio']:,.2f}")
    print(f"📈 Crescimento: {metricas['crescimento_percentual']:+.1f}%")
    print()
    
    # Horários de pico
    horarios = analytics.horarios_pico()
    print("🕐 HORÁRIOS DE PICO:")
    for hora, qtd in sorted(horarios.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {hora}h: {qtd} pedidos")
    print()
    
    # Performance por dia da semana
    dias_performance = analytics.dias_semana_performance()
    print("📅 PERFORMANCE POR DIA DA SEMANA:")
    for dia, vendas in sorted(dias_performance.items(), key=lambda x: x[1], reverse=True):
        print(f"   {dia}: R$ {vendas:,.2f}")

if __name__ == "__main__":
    gerar_relatorio_estatistico()
```

### Passo 5 – Gerar gráficos com matplotlib

#### 5.1 Classe para visualizações
```python
# visualization/charts.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from datetime import datetime
import numpy as np
from typing import List, Dict

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SaboreCharts:
    def __init__(self):
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
    
    def criar_grafico_vendas_tempo(self, vendas_por_periodo: Dict[str, float], titulo: str = "Vendas ao Longo do Tempo"):
        """Criar gráfico de linha das vendas ao longo do tempo"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Preparar dados
        datas = list(vendas_por_periodo.keys())
        valores = list(vendas_por_periodo.values())
        
        # Converter strings de data para datetime
        datas_dt = []
        for data_str in datas:
            try:
                datas_dt.append(datetime.strptime(data_str, '%Y-%m-%d'))
            except:
                # Se falhar, usar a string original
                datas_dt.append(data_str)
        
        # Criar gráfico
        ax.plot(datas_dt, valores, marker='o', linewidth=2, markersize=6, color='#2ecc71')
        ax.fill_between(datas_dt, valores, alpha=0.3, color='#2ecc71')
        
        # Formatação
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Vendas (R$)', fontsize=12)
        
        # Formatar eixo X para datas
        if isinstance(datas_dt[0], datetime):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(datas)//10)))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Grid
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        # Adicionar valores nos pontos
        for i, (data, valor) in enumerate(zip(datas_dt, valores)):
            if i % max(1, len(valores)//5) == 0:  # Mostrar apenas alguns valores
                ax.annotate(f'R$ {valor:,.0f}', (data, valor), 
                          textcoords="offset points", xytext=(0,10), ha='center',
                          fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_grafico_barras_produtos(self, itens_populares: List[Dict], titulo: str = "Produtos Mais Vendidos"):
        """Criar gráfico de barras dos produtos mais vendidos"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Preparar dados
        nomes = [item['nome'][:20] + '...' if len(item['nome']) > 20 else item['nome'] 
                for item in itens_populares[:10]]  # Top 10
        quantidades = [item['quantidade_total'] for item in itens_populares[:10]]
        
        # Criar gráfico de barras horizontal
        bars = ax.barh(range(len(nomes)), quantidades, color=plt.cm.viridis(np.linspace(0, 1, len(nomes))))
        
        # Formatação
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Quantidade Vendida', fontsize=12)
        ax.set_ylabel('Produtos', fontsize=12)
        ax.set_yticks(range(len(nomes)))
        ax.set_yticklabels(nomes)
        
        # Adicionar valores nas barras
        for i, (bar, quantidade) in enumerate(zip(bars, quantidades)):
            ax.text(bar.get_width() + max(quantidades) * 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{quantidade}', ha='left', va='center', fontweight='bold')
        
        # Inverter ordem (maior no topo)
        ax.invert_yaxis()
        
        # Grid
        ax.grid(True, axis='x', alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_grafico_pizza_categorias(self, dados_categoria: Dict[str, float], titulo: str = "Vendas por Categoria"):
        """Criar gráfico de pizza para categorias"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Preparar dados
        labels = list(dados_categoria.keys())
        values = list(dados_categoria.values())
        
        # Cores personalizadas
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        # Criar gráfico de pizza
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                         colors=colors, startangle=90,
                                         explode=[0.05 if i == 0 else 0 for i in range(len(values))])
        
        # Formatação
        ax.set_## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **PyQt5** - Interface gráfica
- **requests** - Comunicação com API
- **matplotlib** - Geração de gráficos e estatísticas
- **reportlab** - Exportação de relatórios em PDF
- **openpyxl** - Exportação de planilhas Excel
- **Pillow (PIL)** - Manipulação de imagens
- **PyPDF2** - Manipulação de PDFs
- **sqlite3** - Cache local (opcional)