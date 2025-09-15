from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json
import calendar

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
                    valor = item.get('preco_unitario', item.get('valor', 0))
                    
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
    
    @staticmethod
    def calcular_ticket_medio(pedidos: List[Dict]) -> float:
        """Calcular ticket médio dos pedidos"""
        if not pedidos:
            return 0.0
        
        total_vendas = DataProcessor.calcular_vendas_totais(pedidos)
        return total_vendas / len(pedidos)
    
    @staticmethod
    def horarios_pico(pedidos: List[Dict]) -> Dict[int, int]:
        """Identificar horários de pico de pedidos"""
        contador_horarios = {}
        
        for pedido in pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                if isinstance(data_pedido_str, str):
                    data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                else:
                    data_pedido = data_pedido_str
                
                hora = data_pedido.hour
                
                if hora not in contador_horarios:
                    contador_horarios[hora] = 0
                contador_horarios[hora] += 1
            except Exception as e:
                print(f"Erro ao processar horário: {e}")
                continue
        
        return dict(sorted(contador_horarios.items()))
    
    @staticmethod
    def dias_semana_performance(pedidos: List[Dict]) -> Dict[str, float]:
        """Analisar performance por dia da semana"""
        vendas_por_dia = {}
        
        for pedido in pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                if isinstance(data_pedido_str, str):
                    data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                else:
                    data_pedido = data_pedido_str
                
                dia_semana = calendar.day_name[data_pedido.weekday()]
                
                if dia_semana not in vendas_por_dia:
                    vendas_por_dia[dia_semana] = 0.0
                
                vendas_por_dia[dia_semana] += pedido.get('valor_total', 0)
            except Exception as e:
                print(f"Erro ao processar dia da semana: {e}")
                continue
        
        return vendas_por_dia
    
    @staticmethod
    def analise_sazonalidade(pedidos: List[Dict], meses: int = 12) -> Dict[str, float]:
        """Analisar sazonalidade de vendas por mês"""
        vendas_por_mes = {}
        
        for pedido in pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                if isinstance(data_pedido_str, str):
                    data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                else:
                    data_pedido = data_pedido_str
                
                mes_nome = calendar.month_name[data_pedido.month]
                
                if mes_nome not in vendas_por_mes:
                    vendas_por_mes[mes_nome] = 0.0
                
                vendas_por_mes[mes_nome] += pedido.get('valor_total', 0)
            except Exception as e:
                print(f"Erro ao processar mês: {e}")
                continue
        
        return vendas_por_mes
    
    @staticmethod
    def calcular_crescimento_vendas(pedidos: List[Dict], dias: int = 30) -> float:
        """Calcular crescimento de vendas comparado ao período anterior"""
        agora = datetime.now()
        periodo_atual = agora - timedelta(days=dias)
        periodo_anterior = periodo_atual - timedelta(days=dias)
        
        # Filtrar pedidos por período
        vendas_atual = []
        vendas_anterior = []
        
        for pedido in pedidos:
            data_pedido_str = pedido.get('data_pedido')
            if not data_pedido_str:
                continue
                
            try:
                if isinstance(data_pedido_str, str):
                    data_pedido = datetime.fromisoformat(data_pedido_str.replace('Z', '+00:00'))
                else:
                    data_pedido = data_pedido_str
                
                if data_pedido >= periodo_atual:
                    vendas_atual.append(pedido)
                elif data_pedido >= periodo_anterior and data_pedido < periodo_atual:
                    vendas_anterior.append(pedido)
            except Exception as e:
                print(f"Erro ao processar crescimento: {e}")
                continue
        
        total_atual = DataProcessor.calcular_vendas_totais(vendas_atual)
        total_anterior = DataProcessor.calcular_vendas_totais(vendas_anterior)
        
        if total_anterior == 0:
            return 100.0 if total_atual > 0 else 0.0
        
        crescimento = ((total_atual - total_anterior) / total_anterior) * 100
        return round(crescimento, 2)
