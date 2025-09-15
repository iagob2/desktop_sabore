# =============================================================================
# IMPORTAÇÕES E CONFIGURAÇÕES
# =============================================================================

# Importações do PyQt5 para interface gráfica
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Importações para gráficos e visualizações
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from datetime import datetime
import numpy as np
from typing import List, Dict

# =============================================================================
# CONFIGURAÇÃO DE ESTILO DOS GRÁFICOS
# =============================================================================
# Define o estilo visual padrão para todos os gráficos
plt.style.use('seaborn-v0_8')  # Tema moderno e limpo
sns.set_palette("husl")        # Paleta de cores vibrantes

# =============================================================================
# CLASSE PRINCIPAL PARA CRIAÇÃO DE GRÁFICOS
# =============================================================================
class SaboreCharts:
    """
    Classe responsável por criar e gerenciar todos os gráficos do dashboard.
    
    Esta classe utiliza matplotlib e seaborn para criar visualizações interativas
    que são integradas ao PyQt5. Cada método cria um tipo específico de gráfico.
    """
    
    def __init__(self):
        """
        Inicializa a classe criando uma figura matplotlib e seu canvas PyQt5.
        
        A figura é configurada com tamanho padrão de 12x8 polegadas e 100 DPI
        para garantir boa qualidade de visualização.
        """
        # Cria a figura matplotlib com tamanho reduzido para melhor visualização
        self.figure = Figure(figsize=(8, 5), dpi=100)
        
        # Cria o canvas PyQt5 que permite integrar matplotlib com PyQt5
        self.canvas = FigureCanvas(self.figure)
    
    # =============================================================================
    # MÉTODOS PARA CRIAÇÃO DE GRÁFICOS ESPECÍFICOS
    # =============================================================================
    
    def criar_grafico_vendas_tempo(self, vendas_por_periodo: Dict[str, float], titulo: str = "Vendas ao Longo do Tempo"):
        """
        Cria um gráfico de linha mostrando a evolução das vendas ao longo do tempo.
        
        Args:
            vendas_por_periodo (Dict[str, float]): Dicionário com datas como chaves e valores de venda
            titulo (str): Título do gráfico
            
        Este método é ideal para mostrar tendências e padrões temporais nas vendas.
        """
        # Limpa a figura anterior para criar um novo gráfico
        self.figure.clear()
        
        # Cria um subplot que ocupa toda a área da figura
        ax = self.figure.add_subplot(111)
        
        # ===== PREPARAÇÃO DOS DADOS =====
        # Extrai as datas e valores do dicionário recebido
        datas = list(vendas_por_periodo.keys())
        valores = list(vendas_por_periodo.values())
        
        # ===== CONVERSÃO DE DATAS =====
        # Converte strings de data para objetos datetime do Python
        datas_dt = []
        for data_str in datas:
            try:
                # Tenta converter string no formato 'YYYY-MM-DD' para datetime
                datas_dt.append(datetime.strptime(data_str, '%Y-%m-%d'))
            except:
                # Se falhar na conversão, mantém a string original
                datas_dt.append(data_str)
        
        # ===== CRIAÇÃO DO GRÁFICO =====
        # Cria linha principal com marcadores nos pontos de dados
        ax.plot(datas_dt, valores, marker='o', linewidth=2, markersize=6, color='#2ecc71')
        
        # Adiciona área preenchida abaixo da linha para melhor visualização
        ax.fill_between(datas_dt, valores, alpha=0.3, color='#2ecc71')
        
        # ===== FORMATAÇÃO DO GRÁFICO =====
        # Define título, labels dos eixos e estilos
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Vendas (R$)', fontsize=12)
        
        # ===== FORMATAÇÃO DO EIXO X PARA DATAS =====
        if isinstance(datas_dt[0], datetime):
            # Formata datas no eixo X como DD/MM
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            # Define intervalo entre marcas do eixo X (máximo 10 marcas)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(datas)//10)))
            # Rotaciona labels do eixo X em 45 graus para melhor legibilidade
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # ===== ESTILO VISUAL =====
        # Adiciona grid sutil para facilitar leitura
        ax.grid(True, alpha=0.3)
        # Define cor de fundo suave
        ax.set_facecolor('#fafafa')
        
        # ===== ANOTAÇÕES NOS PONTOS =====
        # Adiciona valores monetários em alguns pontos do gráfico
        for i, (data, valor) in enumerate(zip(datas_dt, valores)):
            # Mostra apenas alguns valores para não poluir o gráfico
            if i % max(1, len(valores)//5) == 0:
                ax.annotate(f'R$ {valor:,.0f}', (data, valor), 
                          textcoords="offset points", xytext=(0,10), ha='center',
                          fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # ===== FINALIZAÇÃO =====
        # Ajusta layout automaticamente e renderiza o gráfico
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_grafico_barras_produtos(self, itens_populares: List[Dict], titulo: str = "Produtos Mais Vendidos"):
        """
        Cria um gráfico de barras horizontais mostrando os produtos mais vendidos.
        
        Args:
            itens_populares (List[Dict]): Lista de dicionários com dados dos produtos
            titulo (str): Título do gráfico
            
        Este gráfico é ideal para comparar volumes de vendas entre diferentes produtos.
        """
        # Limpa a figura anterior
        self.figure.clear()
        
        # Cria um subplot que ocupa toda a área da figura
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
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        
        # Melhorar aparência dos textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_grafico_horarios_pico(self, horarios: Dict[int, int], titulo: str = "Horários de Pico"):
        """Criar gráfico de barras para horários de pico"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Preparar dados
        horas = list(horarios.keys())
        quantidades = list(horarios.values())
        
        # Criar gráfico de barras
        bars = ax.bar(horas, quantidades, color='#3498db', alpha=0.7)
        
        # Formatação
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Hora do Dia', fontsize=12)
        ax.set_ylabel('Quantidade de Pedidos', fontsize=12)
        ax.set_xticks(horas)
        ax.set_xticklabels([f'{h}h' for h in horas])
        
        # Adicionar valores nas barras
        for bar, quantidade in zip(bars, quantidades):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(quantidades) * 0.01,
                   f'{quantidade}', ha='center', va='bottom', fontweight='bold')
        
        # Grid
        ax.grid(True, axis='y', alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_grafico_dias_semana(self, dias_performance: Dict[str, float], titulo: str = "Performance por Dia da Semana"):
        """Criar gráfico de barras para performance por dia da semana"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Preparar dados
        dias = list(dias_performance.keys())
        vendas = list(dias_performance.values())
        
        # Criar gráfico de barras
        bars = ax.bar(dias, vendas, color='#e74c3c', alpha=0.7)
        
        # Formatação
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Dia da Semana', fontsize=12)
        ax.set_ylabel('Vendas (R$)', fontsize=12)
        
        # Rotacionar labels do eixo X
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Adicionar valores nas barras
        for bar, venda in zip(bars, vendas):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(vendas) * 0.01,
                   f'R$ {venda:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Grid
        ax.grid(True, axis='y', alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def criar_dashboard_multiplos_graficos(self, dados: Dict):
        """Criar dashboard com múltiplos gráficos"""
        self.figure.clear()
        
        # Layout 2x2
        ax1 = self.figure.add_subplot(2, 2, 1)  # Vendas por tempo
        ax2 = self.figure.add_subplot(2, 2, 2)  # Produtos mais vendidos
        ax3 = self.figure.add_subplot(2, 2, 3)  # Horários de pico
        ax4 = self.figure.add_subplot(2, 2, 4)  # Dias da semana
        
        # Gráfico 1: Vendas por tempo
        if 'vendas_por_dia' in dados and dados['vendas_por_dia']:
            vendas_dia = dados['vendas_por_dia']
            datas = list(vendas_dia.keys())[-10:]  # Últimos 10 dias
            valores = [vendas_dia[d] for d in datas]
            ax1.plot(datas, valores, marker='o', color='#2ecc71')
            ax1.set_title('Vendas dos Últimos 10 Dias')
            ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Produtos mais vendidos
        if 'itens_mais_vendidos' in dados and dados['itens_mais_vendidos']:
            itens = dados['itens_mais_vendidos'][:5]  # Top 5
            nomes = [item['nome'][:15] + '...' if len(item['nome']) > 15 else item['nome'] for item in itens]
            quantidades = [item['quantidade_total'] for item in itens]
            ax2.barh(range(len(nomes)), quantidades, color='#3498db')
            ax2.set_yticks(range(len(nomes)))
            ax2.set_yticklabels(nomes)
            ax2.set_title('Top 5 Produtos')
            ax2.invert_yaxis()
        
        # Gráfico 3: Horários de pico
        if 'horarios_pico' in dados and dados['horarios_pico']:
            horarios = dados['horarios_pico']
            horas = list(horarios.keys())
            quantidades = list(horarios.values())
            ax3.bar(horas, quantidades, color='#e74c3c')
            ax3.set_title('Horários de Pico')
            ax3.set_xlabel('Hora')
            ax3.set_ylabel('Pedidos')
        
        # Gráfico 4: Dias da semana
        if 'dias_semana_performance' in dados and dados['dias_semana_performance']:
            dias_perf = dados['dias_semana_performance']
            dias = list(dias_perf.keys())
            vendas = list(dias_perf.values())
            ax4.bar(dias, vendas, color='#f39c12')
            ax4.set_title('Vendas por Dia da Semana')
            ax4.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def salvar_grafico(self, filename: str, dpi: int = 300):
        """Salvar gráfico como imagem"""
        self.figure.savefig(filename, dpi=dpi, bbox_inches='tight')
    
    def get_canvas(self):
        """Retornar o canvas do matplotlib"""
        return self.canvas

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    vendas_exemplo = {
        '2024-01-01': 1500.0,
        '2024-01-02': 1800.0,
        '2024-01-03': 2200.0,
        '2024-01-04': 1900.0,
        '2024-01-05': 2500.0
    }
    
    itens_exemplo = [
        {'nome': 'X-Burger', 'quantidade_total': 45},
        {'nome': 'Pizza Margherita', 'quantidade_total': 38},
        {'nome': 'Batata Frita', 'quantidade_total': 32},
        {'nome': 'Refrigerante', 'quantidade_total': 28},
        {'nome': 'Sorvete', 'quantidade_total': 25}
    ]
    
    # Criar gráficos
    charts = SaboreCharts()
    
    # Gráfico de vendas
    charts.criar_grafico_vendas_tempo(vendas_exemplo, "Vendas da Semana")
    charts.salvar_grafico('vendas_semana.png')
    
    # Gráfico de produtos
    charts.criar_grafico_barras_produtos(itens_exemplo, "Produtos Mais Vendidos")
    charts.salvar_grafico('produtos_vendidos.png')
    
    print("Gráficos salvos com sucesso!")

# =============================================================================
# CLASSE PARA CARTÕES DE MÉTRICAS ANIMADOS
# =============================================================================
class AnimatedCard(QWidget):
    """
    Classe responsável por criar cartões visuais para exibir métricas importantes.
    
    Cada cartão exibe:
    - Um ícone representativo
    - Um título descritivo
    - O valor principal da métrica
    - Informação adicional (opcional)
    
    Os cartões possuem gradientes coloridos e são usados no dashboard principal
    para mostrar KPIs como faturamento, pedidos, ticket médio, etc.
    """
    
    def __init__(self, titulo: str, valor: str, icone: str, gradiente_cores: list, info_extra: str = ""):
        """
        Inicializa um cartão de métrica.
        
        Args:
            titulo (str): Título do cartão (ex: "Faturamento Hoje")
            valor (str): Valor principal a ser exibido (ex: "R$ 1.500,00")
            icone (str): Emoji ou símbolo representativo (ex: "💰")
            gradiente_cores (list): Lista com duas cores para o gradiente de fundo
            info_extra (str): Informação adicional opcional (ex: "vs. ontem")
        """
        super().__init__()
        
        # ===== CONFIGURAÇÃO INICIAL DO CARTÃO =====
        # Define altura e largura para layout lado a lado
        self.setFixedHeight(180)  # Altura reduzida para melhor visualização
        self.setMinimumWidth(180)  # Largura reduzida para melhor distribuição
        
        # ===== ESTILO VISUAL DO CARTÃO =====
        # Aplica gradiente de fundo, bordas arredondadas e margens
        self.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2=1, stop:0 {gradiente_cores[0]}, stop:1 {gradiente_cores[1]});
            margin: 8px;
        """)
        
        # ===== CONFIGURAÇÃO DO LAYOUT =====
        # Cria layout vertical para organizar os elementos do cartão
        layout = QVBoxLayout(self)
        layout.setSpacing(3)           # Espaçamento reduzido entre elementos
        layout.setContentsMargins(15, 10, 15, 10)  # Margens internas reduzidas

        # ===== CABEÇALHO DO CARTÃO (ÍCONE + TÍTULO) =====
        # Cria layout horizontal para ícone e título lado a lado
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)  # Espaçamento entre ícone e título
        
        # ===== ÍCONE =====
        # Cria label para o ícone/emoji
        icone_label = QLabel(icone)
        icone_label.setFont(QFont("Segoe UI Emoji", 23))  # Fonte maior para melhor visibilidade
        icone_label.setStyleSheet("""
            color: white;  # Cor branca para melhor contraste
            padding: 2px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
        """)
        
        # ===== TÍTULO =====
        # Cria label para o título do cartão
        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Segoe UI", 12, QFont.Bold))  # Fonte maior e em negrito
        titulo_label.setStyleSheet("""
            color: white;  # Cor branca para contraste no fundo colorido
            padding: 4px 0px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        """)
        titulo_label.setWordWrap(True)  # Permite quebra de linha se necessário
        
        # ===== MONTAGEM DO CABEÇALHO =====
        # Adiciona ícone e título ao layout horizontal
        header_layout.addWidget(icone_label)
        header_layout.addWidget(titulo_label)
        header_layout.addStretch()  # Empurra elementos para a esquerda
        layout.addLayout(header_layout)

        # ===== VALOR PRINCIPAL =====
        # Cria label para o valor principal da métrica (ex: "R$ 1.500,00")
        self.valor_label = QLabel(valor)
        self.valor_label.setFont(QFont("Segoe UI", 20, QFont.Bold))  # Fonte muito maior para destaque
        self.valor_label.setStyleSheet("""
            color: white;  # Cor branca para destaque
            padding: 8px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            border: 2px solid rgba(255, 255, 255, 0.5);
        """)
        self.valor_label.setAlignment(Qt.AlignCenter)  # Centraliza o texto
        self.valor_label.setWordWrap(True)  # Permite quebra de linha se necessário
        layout.addWidget(self.valor_label)

        # ===== INFORMAÇÃO ADICIONAL =====
        # Adiciona informação extra se fornecida (ex: "vs. ontem")
        if info_extra:
            info_label = QLabel(info_extra)
            info_label.setFont(QFont("Segoe UI", 11, QFont.Normal))  # Fonte um pouco maior
            info_label.setStyleSheet("""
                color: white;  # Cor branca para contraste
                padding: 6px;
                font-weight: normal;
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 6px;
            """)
            info_label.setAlignment(Qt.AlignCenter)  # Centraliza o texto
            info_label.setWordWrap(True)  # Permite quebra de linha se necessário
            layout.addWidget(info_label)

        # ===== FINALIZAÇÃO DO LAYOUT =====
        # Adiciona espaçador para empurrar conteúdo para o topo
        layout.addStretch()

    def update_valor(self, novo_valor: str):
        """
        Atualiza o valor principal exibido no cartão.
        
        Args:
            novo_valor (str): Novo valor a ser exibido (ex: "R$ 2.000,00")
            
        Este método permite atualizar dinamicamente os valores dos cartões
        quando novos dados são carregados.
        """
        self.valor_label.setText(novo_valor)