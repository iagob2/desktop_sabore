from typing import List, Dict, Tuple, Any
import statistics
from datetime import datetime, timedelta
import calendar
from data_processor import DataProcessor

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
        crescimento = self.processor.calcular_crescimento_vendas(self.pedidos)
        
        return {
            'vendas_totais': vendas_totais,
            'ticket_medio': ticket_medio,
            'total_pedidos': total_pedidos,
            'crescimento_percentual': crescimento
        }
    
    def horarios_pico(self) -> Dict[int, int]:
        """Identificar horários de pico de pedidos"""
        return self.processor.horarios_pico(self.pedidos)
    
    def dias_semana_performance(self) -> Dict[str, float]:
        """Analisar performance por dia da semana"""
        return self.processor.dias_semana_performance(self.pedidos)
    
    def analise_sazonalidade(self, meses: int = 12) -> Dict[str, float]:
        """Analisar sazonalidade de vendas por mês"""
        return self.processor.analise_sazonalidade(self.pedidos, meses)
    
    def itens_mais_vendidos(self, limite: int = 10) -> List[Dict]:
        """Encontrar itens mais vendidos"""
        return self.processor.itens_mais_populares(self.pedidos, limite)
    
    def vendas_por_periodo(self, tipo_periodo: str = 'dia') -> Dict[str, float]:
        """Agrupar vendas por período"""
        return self.processor.agrupar_por_periodo(self.pedidos, tipo_periodo)
    
    def calcular_estatisticas_avancadas(self) -> Dict[str, Any]:
        """Calcular estatísticas avançadas"""
        if not self.pedidos:
            return {}
        
        # Valores dos pedidos
        valores_pedidos = [pedido.get('valor_total', 0) for pedido in self.pedidos]
        
        # Estatísticas básicas
        media_valor = statistics.mean(valores_pedidos)
        mediana_valor = statistics.median(valores_pedidos)
        desvio_padrao = statistics.stdev(valores_pedidos) if len(valores_pedidos) > 1 else 0
        
        # Pedido com maior valor
        pedido_maior_valor = max(self.pedidos, key=lambda x: x.get('valor_total', 0))
        
        # Pedido com menor valor
        pedido_menor_valor = min(self.pedidos, key=lambda x: x.get('valor_total', 0))
        
        return {
            'media_valor_pedido': media_valor,
            'mediana_valor_pedido': mediana_valor,
            'desvio_padrao_valor': desvio_padrao,
            'maior_pedido': {
                'id': pedido_maior_valor.get('id'),
                'valor': pedido_maior_valor.get('valor_total', 0),
                'data': pedido_maior_valor.get('data_pedido')
            },
            'menor_pedido': {
                'id': pedido_menor_valor.get('id'),
                'valor': pedido_menor_valor.get('valor_total', 0),
                'data': pedido_menor_valor.get('data_pedido')
            }
        }
    
    def analise_tendencia_vendas(self, dias: int = 30) -> Dict[str, Any]:
        """Analisar tendência de vendas"""
        agora = datetime.now()
        data_inicio = agora - timedelta(days=dias)
        
        # Filtrar pedidos do período
        pedidos_periodo = []
        for pedido in self.pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                if isinstance(data_pedido_str, str):
                    data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                else:
                    data_pedido = data_pedido_str
                
                if data_pedido >= data_inicio:
                    pedidos_periodo.append(pedido)
            except:
                continue
        
        if not pedidos_periodo:
            return {'tendencia': 'estavel', 'crescimento_diario': 0.0}
        
        # Agrupar por dia
        vendas_por_dia = self.processor.agrupar_por_periodo(pedidos_periodo, 'dia')
        
        if len(vendas_por_dia) < 2:
            return {'tendencia': 'estavel', 'crescimento_diario': 0.0}
        
        # Calcular tendência linear simples
        valores = list(vendas_por_dia.values())
        dias_lista = list(range(len(valores)))
        
        # Regressão linear simples
        n = len(valores)
        if n > 1:
            media_x = sum(dias_lista) / n
            media_y = sum(valores) / n
            
            numerador = sum((dias_lista[i] - media_x) * (valores[i] - media_y) for i in range(n))
            denominador = sum((dias_lista[i] - media_x) ** 2 for i in range(n))
            
            if denominador != 0:
                inclinacao = numerador / denominador
                
                if inclinacao > 0:
                    tendencia = 'crescente'
                elif inclinacao < 0:
                    tendencia = 'decrescente'
                else:
                    tendencia = 'estavel'
                
                return {
                    'tendencia': tendencia,
                    'crescimento_diario': inclinacao,
                    'inclinacao': inclinacao
                }
        
        return {'tendencia': 'estavel', 'crescimento_diario': 0.0}
    
    def previsao_vendas_simples(self, dias_futuros: int = 7) -> List[float]:
        """Previsão simples de vendas baseada na média móvel"""
        if not self.pedidos:
            return [0.0] * dias_futuros
        
        # Agrupar vendas por dia
        vendas_por_dia = self.processor.agrupar_por_periodo(self.pedidos, 'dia')
        
        if not vendas_por_dia:
            return [0.0] * dias_futuros
        
        # Calcular média móvel dos últimos 7 dias
        valores = list(vendas_por_dia.values())
        if len(valores) >= 7:
            media_movel = sum(valores[-7:]) / 7
        else:
            media_movel = sum(valores) / len(valores)
        
        # Previsão simples: usar a média móvel
        previsoes = [media_movel] * dias_futuros
        
        return previsoes
    
    def gerar_relatorio_completo(self) -> Dict[str, Any]:
        """Gerar relatório completo de análises"""
        metricas = self.calcular_metricas_principais()
        estatisticas_avancadas = self.calcular_estatisticas_avancadas()
        tendencia = self.analise_tendencia_vendas()
        previsao = self.previsao_vendas_simples()
        
        return {
            'metricas_principais': metricas,
            'estatisticas_avancadas': estatisticas_avancadas,
            'tendencia_vendas': tendencia,
            'previsao_vendas': previsao,
            'horarios_pico': self.horarios_pico(),
            'dias_semana_performance': self.dias_semana_performance(),
            'itens_mais_vendidos': self.itens_mais_vendidos(),
            'vendas_por_dia': self.vendas_por_periodo('dia'),
            'vendas_por_semana': self.vendas_por_periodo('semana'),
            'vendas_por_mes': self.vendas_por_periodo('mes'),
            'data_geracao': datetime.now().isoformat()
        }

# Exemplo de uso
def gerar_relatorio_estatistico():
    """Exemplo de como gerar relatório completo"""
    # Buscar dados
    from api_client import SaboreAPIClient
    client = SaboreAPIClient()
    pedidos = client.get_pedidos()
    
    if not pedidos:
        print("Nenhum pedido encontrado")
        return
    
    # Análises
    analytics = SaboreAnalytics(pedidos)
    relatorio = analytics.gerar_relatorio_completo()
    
    print("=== RELATÓRIO DE VENDAS SABORÊ ===")
    print()
    
    # Métricas principais
    metricas = relatorio['metricas_principais']
    print(f"💰 Vendas Totais: R$ {metricas['vendas_totais']:,.2f}")
    print(f"🛒 Total de Pedidos: {metricas['total_pedidos']}")
    print(f"🎯 Ticket Médio: R$ {metricas['ticket_medio']:,.2f}")
    print(f"📈 Crescimento: {metricas['crescimento_percentual']:+.1f}%")
    print()
    
    # Horários de pico
    horarios = relatorio['horarios_pico']
    print("🕐 HORÁRIOS DE PICO:")
    for hora, qtd in sorted(horarios.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {hora}h: {qtd} pedidos")
    print()
    
    # Performance por dia da semana
    dias_performance = relatorio['dias_semana_performance']
    print("📅 PERFORMANCE POR DIA DA SEMANA:")
    for dia, vendas in sorted(dias_performance.items(), key=lambda x: x[1], reverse=True):
        print(f"   {dia}: R$ {vendas:,.2f}")
    print()
    
    # Itens mais vendidos
    itens_populares = relatorio['itens_mais_vendidos']
    print("🍕 ITENS MAIS VENDIDOS:")
    for i, item in enumerate(itens_populares[:5], 1):
        print(f"   {i}. {item['nome']}: {item['quantidade_total']} unidades")
    print()
    
    # Tendência
    tendencia = relatorio['tendencia_vendas']
    print(f"📊 TENDÊNCIA: {tendencia['tendencia'].upper()}")
    if tendencia['crescimento_diario'] != 0:
        print(f"   Crescimento diário: R$ {tendencia['crescimento_diario']:,.2f}")
    
    return relatorio

if __name__ == "__main__":
    gerar_relatorio_estatistico()
