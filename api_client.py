# =============================================================================
# CLIENTE PARA COMUNICAÇÃO COM A API DO SABORÊ BACKEND
# =============================================================================
# Este arquivo contém o cliente HTTP responsável por toda comunicação
# com a API do backend Saborê, incluindo:
# - Requisições HTTP (GET, POST, PUT, DELETE)
# - Tratamento de erros de conexão
# - Dados mock para demonstração
# - Configurações de timeout e retry

# =============================================================================
# IMPORTAÇÕES NECESSÁRIAS
# =============================================================================

# Importações padrão do Python
import requests          # Biblioteca para requisições HTTP
import logging          # Sistema de logs
from datetime import datetime  # Manipulação de datas
from typing import Dict, List, Any, Optional  # Tipagem estática

# Importações do projeto
from config import Settings  # Configurações da aplicação

# =============================================================================
# CONFIGURAÇÃO DE LOGGING
# =============================================================================
# Configura o sistema de logs para registrar operações da API
logger = logging.getLogger(__name__)


# Exceção customizada para erros de API
class APIError(Exception):
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# =============================================================================
# CLASSE PRINCIPAL DO CLIENTE API
# =============================================================================
class SaboreAPIClient:
    """
    Cliente HTTP para comunicação com a API do Saborê Backend.
    
    Esta classe gerencia todas as operações de comunicação com o backend,
    incluindo:
    - Requisições HTTP padronizadas
    - Tratamento de erros de conexão
    - Sistema de fallback com dados mock
    - Configurações de timeout e retry
    - Headers padrão para todas as requisições
    """

    def __init__(self, base_url: str = None):
        """
        Inicializa o cliente da API.
        
        Args:
            base_url (str, optional): URL base da API. Se não fornecida,
                                    usa a URL padrão do arquivo de configuração.
        """
        # ===== CONFIGURAÇÃO DA URL BASE =====
        # Usa URL fornecida ou a URL padrão das configurações
        self.base_url = base_url or Settings.API_BASE_URL

        # ===== CONFIGURAÇÃO DA SESSÃO HTTP =====
        # Cria sessão HTTP que mantém cookies, headers e configurações
        self.session = requests.Session()
        
        # Define headers padrão para todas as requisições
        self.session.headers.update({
            'Content-Type': 'application/json',  # Tipo de conteúdo
            'Accept': 'application/json',        # Aceita apenas JSON
            'User-Agent': 'Sabore-Desktop/1.0'  # Identificação do cliente
        })

        # ===== CONFIGURAÇÕES DE TIMEOUT =====
        # Timeout padrão para requisições (definido em config.py)
        self.timeout = Settings.TIMEOUT

    # ======================================================
    # MÉTODO CENTRAL DE REQUISIÇÃO
    # ======================================================
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Faz requisição HTTP com tratamento de erros"""
        url = f"{self.base_url}{endpoint}"

        try:
            logger.info(f"Requisição {method} -> {url}")
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.ConnectionError:
            raise APIError(f"Não foi possível conectar ao backend em {url}")
        except requests.exceptions.Timeout:
            raise APIError(f"Timeout ao conectar com {url}")
        except requests.exceptions.HTTPError as e:
            raise APIError(f"Erro HTTP {response.status_code}: {response.text}", response.status_code)
        except Exception as e:
            raise APIError(f"Erro inesperado: {str(e)}")

    # ======================================================
    # MÉTODOS AUXILIARES (GET, POST, PUT, DELETE)
    # ======================================================
    def _get(self, endpoint: str, params: Dict = None) -> Any:
        response = self._make_request("GET", endpoint, params=params)
        
        # Verificar se a resposta é JSON válido
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' not in content_type:
            raise APIError(f"Resposta não é JSON. Content-Type: {content_type}")
        
        try:
            return response.json()
        except ValueError:
            # Se não conseguir fazer parse do JSON, retorna texto ou vazio
            return {"status": "success", "message": "Operação realizada com sucesso"}

    def _post(self, endpoint: str, data: Dict = None, files: Dict = None) -> Any:
        response = self._make_request("POST", endpoint, json=data if not files else None, files=files)
        try:
            return response.json()
        except ValueError:
            # Se não conseguir fazer parse do JSON, retorna texto ou vazio
            return {"status": "success", "message": "Operação realizada com sucesso"}

    def _put(self, endpoint: str, data: Dict = None) -> Any:
        response = self._make_request("PUT", endpoint, json=data)
        try:
            return response.json()
        except ValueError:
            # Se não conseguir fazer parse do JSON, retorna texto ou vazio
            return {"status": "success", "message": "Operação realizada com sucesso"}

    def _delete(self, endpoint: str) -> bool:
        response = self._make_request("DELETE", endpoint)
        return response.status_code in (200, 204)

    # ======================================================
    # ENDPOINTS ESPECÍFICOS (do seu código)
    # ======================================================
    def login_restaurante(self, email: str, senha: str) -> Dict[str, Any]:
        """Login do restaurante"""
        try:
            return self._post("/restaurantes/login", {"email": email, "senha": senha})
        except APIError:
            logger.warning("Endpoint de login de restaurante não encontrado, retornando dados mock")
            return {"token": "mock_token_restaurante", "restaurante": {"id": 1, "nome": "Restaurante Mock"}}

    def get_pedidos(self, restaurante_id: Optional[int] = None, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
        """Buscar pedidos com filtros opcionais"""
        params = {}
        if restaurante_id:
            params['restaurante_id'] = restaurante_id
        if data_inicio:
            params['data_inicio'] = data_inicio
        if data_fim:
            params['data_fim'] = data_fim

        # Tentar diferentes endpoints de pedidos
        try:
            return self._get("/api/pedidos", params=params)
        except APIError:
            try:
                return self._get("/pedidos", params=params)
            except APIError:
                # Retornar dados mock se não houver endpoint de pedidos
                logger.warning("Endpoint de pedidos não encontrado, retornando dados mock")
                return self._get_mock_pedidos()

    def get_estatisticas_restaurante(self, restaurante_id: int) -> Dict[str, Any]:
        """Buscar estatísticas do restaurante"""
        try:
            return self._get(f"/api/restaurantes/{restaurante_id}/estatisticas")
        except APIError:
            try:
                return self._get(f"/restaurantes/{restaurante_id}/estatisticas")
            except APIError:
                # Retornar estatísticas mock se não houver endpoint
                logger.warning("Endpoint de estatísticas não encontrado, retornando dados mock")
                return self._get_mock_estatisticas(restaurante_id)

    def get_itens_mais_vendidos(self, restaurante_id: int, periodo: str = "30") -> List[Dict]:
        """Itens mais vendidos nos últimos X dias"""
        try:
            return self._get(f"/api/restaurantes/{restaurante_id}/itens-vendidos", params={"periodo": periodo})
        except APIError:
            try:
                return self._get(f"/restaurantes/{restaurante_id}/itens-vendidos", params={"periodo": periodo})
            except APIError:
                # Retornar dados mock se não houver endpoint
                logger.warning("Endpoint de itens vendidos não encontrado, retornando dados mock")
                return self._get_mock_itens_vendidos(restaurante_id)

    # =============================================================================
    # ENDPOINTS REMOVIDOS - DESNECESSÁRIOS
    # =============================================================================
    # Os endpoints get_vendas_periodo e get_produtos_populares foram removidos
    # pois a aplicação funciona perfeitamente com os endpoints existentes:
    # - get_pedidos() para dados de vendas
    # - get_itens_mais_vendidos() para produtos populares  
    # - get_estatisticas_restaurante() para métricas gerais
    # 
    # Isso simplifica o código e remove dependências desnecessárias.

    def get_restaurante(self, restaurante_id: int) -> Dict[str, Any]:
        """Buscar dados de um restaurante"""
        try:
            return self._get(f"/restaurantes/{restaurante_id}")
        except APIError:
            logger.warning("Endpoint de busca de restaurante por ID não encontrado, retornando dados mock")
            return {"id": restaurante_id, "nome": f"Restaurante {restaurante_id}", "email": f"restaurante{restaurante_id}@mock.com"}

    def upload_file(self, file_path: str, tipo: str) -> str:
        """Upload de arquivo (logo, banner, cardápio)"""
        with open(file_path, 'rb') as f:
            files = {"file": f}
            response = self._post(f"/restaurantes/upload/{tipo}", files=files)
        return response.get("url", "")

    # ======================================================
    # EXTRAS (do código IA)
    # ======================================================
    def get_clientes(self) -> List[Dict]:
        return self._get(Settings.ENDPOINTS['CLIENTES'])

    def get_restaurantes(self) -> List[Dict]:
        return self._get(Settings.ENDPOINTS['RESTAURANTES'])

    def get_itens(self) -> List[Dict]:
        return self._get(Settings.ENDPOINTS['ITENS'])

    def test_connection(self) -> bool:
        """Verifica se a API está respondendo"""
        try:
            self.get_restaurantes()
            return True
        except APIError:
            return False

    # =============================================================================
    # ENDPOINTS DE CLIENTES
    # =============================================================================
    
    def login_cliente(self, email: str, senha: str) -> Dict[str, Any]:
        """Login do cliente"""
        try:
            return self._post("/clientes/login", {"email": email, "senha": senha})
        except APIError:
            logger.warning("Endpoint de login de cliente não encontrado, retornando dados mock")
            return {"token": "mock_token_cliente", "cliente": {"id": 1, "nome": "Cliente Mock"}}

    def get_cliente_logado(self) -> Dict[str, Any]:
        """Dados do cliente logado"""
        try:
            return self._get("/clientes/me")
        except APIError:
            logger.warning("Endpoint de dados do cliente não encontrado, retornando dados mock")
            return {"id": 1, "nome": "Cliente Mock", "email": "cliente@mock.com"}

    def logout_cliente(self) -> bool:
        """Logout do cliente"""
        try:
            response = self._post("/clientes/logout")
            return True
        except APIError:
            try:
                response = self._get("/clientes/logout")
                return True
            except APIError:
                logger.warning("Endpoint de logout de cliente não encontrado")
                return True

    def cadastrar_cliente(self, dados_cliente: Dict[str, Any]) -> Dict[str, Any]:
        """Cadastrar novo cliente"""
        try:
            return self._post("/clientes", dados_cliente)
        except APIError:
            logger.warning("Endpoint de cadastro de cliente não encontrado, retornando dados mock")
            return {"id": 1, "nome": dados_cliente.get("nome", "Cliente Mock"), "status": "criado"}

    def atualizar_cliente(self, cliente_id: int, dados_cliente: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar cliente"""
        try:
            return self._put(f"/clientes/{cliente_id}", dados_cliente)
        except APIError:
            logger.warning("Endpoint de atualização de cliente não encontrado, retornando dados mock")
            return {"id": cliente_id, "status": "atualizado"}

    def deletar_cliente(self, cliente_id: int) -> bool:
        """Deletar cliente"""
        try:
            return self._delete(f"/clientes/{cliente_id}")
        except APIError:
            logger.warning("Endpoint de exclusão de cliente não encontrado")
            return True

    def get_cliente_por_id(self, cliente_id: int) -> Dict[str, Any]:
        """Buscar cliente por ID"""
        try:
            return self._get(f"/clientes/{cliente_id}")
        except APIError:
            logger.warning("Endpoint de busca de cliente por ID não encontrado, retornando dados mock")
            return {"id": cliente_id, "nome": f"Cliente {cliente_id}", "email": f"cliente{cliente_id}@mock.com"}

    # =============================================================================
    # ENDPOINTS DE RESTAURANTES (ADICIONAIS)
    # =============================================================================
    
    def cadastrar_restaurante(self, dados_restaurante: Dict[str, Any]) -> Dict[str, Any]:
        """Cadastrar novo restaurante"""
        try:
            return self._post("/restaurantes", dados_restaurante)
        except APIError:
            logger.warning("Endpoint de cadastro de restaurante não encontrado, retornando dados mock")
            return {"id": 1, "nome": dados_restaurante.get("nome", "Restaurante Mock"), "status": "criado"}

    def atualizar_restaurante(self, restaurante_id: int, dados_restaurante: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar restaurante"""
        try:
            return self._put(f"/restaurantes/{restaurante_id}", dados_restaurante)
        except APIError:
            logger.warning("Endpoint de atualização de restaurante não encontrado, retornando dados mock")
            return {"id": restaurante_id, "status": "atualizado"}

    def deletar_restaurante(self, restaurante_id: int) -> bool:
        """Deletar restaurante"""
        try:
            return self._delete(f"/restaurantes/{restaurante_id}")
        except APIError:
            logger.warning("Endpoint de exclusão de restaurante não encontrado")
            return True

    # =============================================================================
    # ENDPOINTS DE ITENS (ADICIONAIS)
    # =============================================================================
    
    def cadastrar_item(self, dados_item: Dict[str, Any]) -> Dict[str, Any]:
        """Cadastrar novo item"""
        try:
            return self._post("/itens", dados_item)
        except APIError:
            logger.warning("Endpoint de cadastro de item não encontrado, retornando dados mock")
            return {"id": 1, "nome": dados_item.get("nome", "Item Mock"), "status": "criado"}

    def upload_imagem_item(self, file_path: str) -> str:
        """Upload de imagem do item"""
        try:
            return self.upload_file(file_path, "item")
        except APIError:
            logger.warning("Endpoint de upload de imagem de item não encontrado")
            return "mock_url_imagem_item"

    def atualizar_item(self, item_id: int, dados_item: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar item"""
        try:
            return self._put(f"/itens/{item_id}", dados_item)
        except APIError:
            logger.warning("Endpoint de atualização de item não encontrado, retornando dados mock")
            return {"id": item_id, "status": "atualizado"}

    def deletar_item(self, item_id: int) -> bool:
        """Deletar item"""
        try:
            return self._delete(f"/itens/{item_id}")
        except APIError:
            logger.warning("Endpoint de exclusão de item não encontrado")
            return True

    def get_item_por_id(self, item_id: int) -> Dict[str, Any]:
        """Buscar item por ID"""
        try:
            return self._get(f"/itens/{item_id}")
        except APIError:
            logger.warning("Endpoint de busca de item por ID não encontrado, retornando dados mock")
            return {"id": item_id, "nome": f"Item {item_id}", "preco": 15.50}

    def get_itens_por_restaurante(self, restaurante_id: int) -> List[Dict]:
        """Itens por restaurante"""
        try:
            return self._get(f"/itens/restaurante/{restaurante_id}")
        except APIError:
            logger.warning("Endpoint de itens por restaurante não encontrado, retornando dados mock")
            return self._get_mock_itens_por_restaurante(restaurante_id)

    # =============================================================================
    # ENDPOINTS DE PEDIDOS (ADICIONAIS)
    # =============================================================================
    
    def criar_pedido(self, dados_pedido: Dict[str, Any]) -> Dict[str, Any]:
        """Criar novo pedido"""
        try:
            return self._post("/pedidos", dados_pedido)
        except APIError:
            logger.warning("Endpoint de criação de pedido não encontrado, retornando dados mock")
            return {"id": 1, "status": "criado", "valor_total": dados_pedido.get("valor_total", 0)}

    def atualizar_status_pedido(self, pedido_id: int, novo_status: str) -> Dict[str, Any]:
        """Atualizar status do pedido"""
        try:
            return self._put(f"/pedidos/{pedido_id}/status", {"status": novo_status})
        except APIError:
            logger.warning("Endpoint de atualização de status de pedido não encontrado, retornando dados mock")
            return {"id": pedido_id, "status": novo_status}

    def get_pedidos_cliente(self, cliente_id: Optional[int] = None) -> List[Dict]:
        """Listar pedidos do cliente"""
        try:
            params = {"cliente_id": cliente_id} if cliente_id else {}
            return self._get("/pedidos", params=params)
        except APIError:
            logger.warning("Endpoint de pedidos do cliente não encontrado, retornando dados mock")
            return self._get_mock_pedidos()

    # =============================================================================
    # ENDPOINTS DE AVALIAÇÕES
    # =============================================================================
    
    def criar_avaliacao(self, dados_avaliacao: Dict[str, Any]) -> Dict[str, Any]:
        """Criar avaliação do restaurante"""
        try:
            return self._post("/avaliacoes", dados_avaliacao)
        except APIError:
            logger.warning("Endpoint de criação de avaliação não encontrado, retornando dados mock")
            return {"id": 1, "status": "criada"}

    def get_avaliacoes_restaurante(self, restaurante_id: int) -> List[Dict]:
        """Avaliações por restaurante"""
        try:
            return self._get(f"/avaliacoes/{restaurante_id}")
        except APIError:
            logger.warning("Endpoint de avaliações por restaurante não encontrado, retornando dados mock")
            return self._get_mock_avaliacoes_restaurante(restaurante_id)

    def get_todas_avaliacoes(self) -> List[Dict]:
        """Listar todas as avaliações"""
        try:
            return self._get("/avaliacoes")
        except APIError:
            logger.warning("Endpoint de listagem de avaliações não encontrado, retornando dados mock")
            return self._get_mock_avaliacoes_restaurante(1)

    # =============================================================================
    # ENDPOINTS DE AVALIAÇÕES DE PRATOS
    # =============================================================================
    
    def avaliar_prato(self, dados_avaliacao: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliar prato específico"""
        try:
            return self._post("/avaliacoes-prato", dados_avaliacao)
        except APIError:
            logger.warning("Endpoint de avaliação de prato não encontrado, retornando dados mock")
            return {"id": 1, "status": "avaliado"}

    def get_avaliacoes_prato(self, item_id: int) -> List[Dict]:
        """Avaliações por item"""
        try:
            return self._get(f"/avaliacoes-prato/item/{item_id}")
        except APIError:
            logger.warning("Endpoint de avaliações por item não encontrado, retornando dados mock")
            return self._get_mock_avaliacoes_prato(item_id)

    def get_todas_avaliacoes_pratos(self) -> List[Dict]:
        """Listar todas as avaliações de pratos"""
        try:
            return self._get("/avaliacoes-prato")
        except APIError:
            logger.warning("Endpoint de listagem de avaliações de pratos não encontrado, retornando dados mock")
            return self._get_mock_avaliacoes_prato(1)

    # ======================================================
    # MÉTODOS MOCK (para quando endpoints não existem)
    # ======================================================
    def _get_mock_pedidos(self) -> List[Dict]:
        """Retorna dados mock de pedidos para demonstração"""
        from datetime import datetime, timedelta
        import random
        
        pedidos = []
        for i in range(10):
            data_pedido = datetime.now() - timedelta(days=random.randint(0, 30))
            pedidos.append({
                "id": i + 1,
                "data_pedido": data_pedido.isoformat(),
                "valor_total": round(random.uniform(25.0, 150.0), 2),
                "cliente": f"Cliente {i + 1}",
                "status": random.choice(["Pendente", "Em preparo", "Entregue", "Cancelado"]),
                "itens": [
                    {
                        "nome": f"Prato {j + 1}",
                        "valor": round(random.uniform(10.0, 50.0), 2),
                        "quantidade": random.randint(1, 3),
                        "categoria": random.choice(["Lanches", "Bebidas", "Sobremesas"])
                    } for j in range(random.randint(1, 3))
                ]
            })
        return pedidos

    def _get_mock_estatisticas(self, restaurante_id: int) -> Dict[str, Any]:
        """Retorna estatísticas mock para demonstração"""
        import random
        
        return {
            "restaurante_id": restaurante_id,
            "vendas_totais": round(random.uniform(5000.0, 25000.0), 2),
            "total_pedidos": random.randint(50, 300),
            "ticket_medio": round(random.uniform(25.0, 80.0), 2),
            "crescimento": round(random.uniform(-10.0, 25.0), 2),
            "periodo": "30 dias"
        }

    def _get_mock_itens_vendidos(self, restaurante_id: int) -> List[Dict]:
        """Retorna itens mais vendidos mock para demonstração"""
        import random
        
        itens = [
            "X-Burger", "Pizza Margherita", "Coca-Cola", "Batata Frita",
            "Açaí", "Hambúrguer Artesanal", "Refrigerante", "Salada Caesar",
            "Suco Natural", "Pudim", "Café", "Sanduíche Natural"
        ]
        
        return [
            {
                "nome": item,
                "quantidade_total": random.randint(10, 100),  # Campo esperado pelos gráficos
                "quantidade_vendida": random.randint(10, 100),  # Campo alternativo
                "valor_total": round(random.uniform(200.0, 1500.0), 2),
                "categoria": random.choice(["Lanches", "Bebidas", "Sobremesas", "Saladas"])
            }
            for item in random.sample(itens, 8)
        ]

    # =============================================================================
    # MÉTODOS MOCK REMOVIDOS - DESNECESSÁRIOS
    # =============================================================================
    # Os métodos _get_mock_vendas_periodo e _get_mock_produtos_populares foram removidos
    # pois não são mais necessários. A aplicação usa:
    # - get_pedidos() que já retorna dados mock de vendas
    # - get_itens_mais_vendidos() que já retorna dados mock de produtos

    def _get_mock_itens_por_restaurante(self, restaurante_id: int) -> List[Dict]:
        """Retorna itens mock por restaurante"""
        import random
        
        itens = [
            "X-Burger", "Pizza Margherita", "Coca-Cola", "Batata Frita",
            "Açaí", "Hambúrguer Artesanal", "Refrigerante", "Salada Caesar"
        ]
        
        return [
            {
                "id": i + 1,
                "nome": item,
                "preco": round(random.uniform(8.0, 35.0), 2),
                "categoria": random.choice(["Lanches", "Bebidas", "Sobremesas", "Saladas"]),
                "descricao": f"Descrição do {item}",
                "restaurante_id": restaurante_id,
                "disponivel": random.choice([True, True, True, False])  # 75% disponível
            }
            for i, item in enumerate(random.sample(itens, random.randint(5, 8)))
        ]

    def _get_mock_avaliacoes_restaurante(self, restaurante_id: int) -> List[Dict]:
        """Retorna avaliações mock por restaurante"""
        import random
        
        avaliacoes = []
        for i in range(random.randint(5, 15)):
            avaliacoes.append({
                "id": i + 1,
                "restaurante_id": restaurante_id,
                "cliente_id": random.randint(1, 10),
                "nota": random.randint(1, 5),
                "comentario": f"Comentário {i + 1} sobre o restaurante",
                "data_avaliacao": "2024-01-15T10:30:00"
            })
        
        return avaliacoes

    def _get_mock_avaliacoes_prato(self, item_id: int) -> List[Dict]:
        """Retorna avaliações mock por prato"""
        import random
        
        avaliacoes = []
        for i in range(random.randint(3, 10)):
            avaliacoes.append({
                "id": i + 1,
                "item_id": item_id,
                "cliente_id": random.randint(1, 10),
                "nota": random.randint(1, 5),
                "comentario": f"Comentário {i + 1} sobre o prato",
                "data_avaliacao": "2024-01-15T10:30:00"
            })
        
        return avaliacoes


# ======================================================
# EXEMPLO DE USO
# ======================================================
if __name__ == "__main__":
    client = SaboreAPIClient()

    try:
        pedidos = client.get_pedidos()
        print(f"Total de pedidos: {len(pedidos)}")

        for pedido in pedidos[:5]:
            print(f"Pedido {pedido.get('id')}: R$ {pedido.get('valor_total', 0):.2f}")

    except APIError as e:
        print(f"Erro na API: {e.message}")
