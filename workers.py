# workers.py
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, timedelta

class DataWorker(QThread):
    data_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, api_client, restaurante_id=None):
        super().__init__()
        self.api_client = api_client
        self.restaurante_id = restaurante_id

    def run(self):
        try:
            # Usar endpoints existentes que funcionam perfeitamente
            vendas_detalhadas = self.api_client.get_pedidos(self.restaurante_id)
            produtos_populares = self.api_client.get_itens_mais_vendidos(self.restaurante_id or 1, "30")

            mock_data = {
                'vendas_detalhadas': vendas_detalhadas,
                'itens_mais_vendidos': produtos_populares,
                'last_update': datetime.now().isoformat()
            }

            # Simula delay de rede
            self.msleep(2000)

            self.data_loaded.emit(mock_data)

        except Exception as e:
            self.error_occurred.emit(f"Erro ao carregar dados: {str(e)}")