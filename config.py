import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configurações da aplicação"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
    APP_NAME = "Saborê Desktop"
    APP_VERSION = "1.0.0"
    
    # URL base do backend Spring Boot
    # API_BASE_URL = "http://localhost:8080"

    # Configurações de upload
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.gif']
    ALLOWED_PDF_TYPES = ['.pdf']
    
    # Configurações de interface
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600
    
    # Endpoints da API
    ENDPOINTS = {
        # Clientes
        'CLIENTES': '/clientes',
        'CLIENTES_BY_ID': '/clientes/{id}',
        
        # Restaurantes
        'RESTAURANTES': '/restaurantes',
        'RESTAURANTES_BY_ID': '/restaurantes/{id}',
        
        # Itens/Pratos
        'ITENS': '/itens',
        'ITENS_BY_ID': '/itens/{id}',
        
        # Avaliações
        'AVALIACOES': '/avaliacoes',
        'AVALIACOES_PRATO': '/avaliacoes-prato',
        
        # Pedidos (se existir endpoint)
        'PEDIDOS': '/pedidos',
        'PEDIDOS_BY_ID': '/pedidos/{id}',
        
        # Login/Auth (se necessário)
        'LOGIN': '/login',
        'LOGOUT': '/logout'
    }
    
    # Configurações de conexão
    TIMEOUT = 30  # segundos
    RETRY_ATTEMPTS = 3
    
    # Configurações de relatórios
    REPORTS_DIR = "relatorios"
    EXPORT_DIR = "exportacoes"
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "sabore_desktop.log"
    
    @classmethod
    def get_full_url(cls, endpoint_key, **kwargs):
        """Retorna a URL completa para um endpoint"""
        endpoint = cls.ENDPOINTS.get(endpoint_key)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_key}' não encontrado")
        
        # Substituir placeholders como {id}
        endpoint = endpoint.format(**kwargs)
        
        return f"{cls.API_BASE_URL}{endpoint}"
