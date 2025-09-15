# 📋 Lista Completa de Endpoints – Sistema Restaurante

## 🔐 Autenticação e Clientes (`/clientes`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /clientes/login           | Login do cliente             | ❌ |
| GET    | /clientes/me              | Dados do usuário logado      | ✅ |
| POST   | /clientes/logout          | Logout do cliente            | ✅ |
| GET    | /clientes/logout          | Logout via GET (testes)      | ✅ |
| POST   | /clientes                 | Cadastrar novo cliente       | ❌ |
| GET    | /clientes                 | Listar todos os clientes     | ❌ |
| GET    | /clientes/{id}            | Buscar cliente por ID        | ❌ |
| PUT    | /clientes/{id}            | Atualizar cliente            | ❌ |
| DELETE | /clientes/{id}            | Deletar cliente              | ❌ |

## 🏪 Restaurantes (`/restaurantes`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /restaurantes/login           | Login do restaurante          | ❌ |
| POST   | /restaurantes                 | Cadastrar novo restaurante    | ❌ |
| POST   | /restaurantes/upload/{tipo}   | Upload de arquivo por tipo    | ❌ |
| POST   | /restaurantes/upload          | Upload genérico               | ❌ |
| GET    | /restaurantes                 | Listar todos os restaurantes  | ❌ |
| GET    | /restaurantes/{id}            | Buscar restaurante por ID     | ❌ |
| PUT    | /restaurantes/{id}            | Atualizar restaurante         | ❌ |
| DELETE | /restaurantes/{id}            | Deletar restaurante           | ❌ |

## 🍽️ Itens do Cardápio (`/itens`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /itens                    | Cadastrar novo item          | ❌ |
| POST   | /itens/upload             | Upload de imagem do item     | ❌ |
| GET    | /itens                    | Listar todos os itens        | ❌ |
| GET    | /itens/{id}               | Buscar item por ID           | ❌ |
| PUT    | /itens/{id}               | Atualizar item               | ❌ |
| DELETE | /itens/{id}               | Deletar item                 | ❌ |
| GET    | /itens/restaurante/{id}   | Itens por restaurante        | ❌ |

## 📦 Pedidos (`/pedidos`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /pedidos               | Criar novo pedido          | ✅ |
| GET    | /pedidos               | Listar pedidos do cliente  | ✅ |
| PUT    | /pedidos/{id}/status   | Atualizar status do pedido | ✅ |

## ⭐ Avaliações (`/avaliacoes`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /avaliacoes                      | Criar avaliação do restaurante  | ✅ |
| GET    | /avaliacoes/{restauranteId}      | Avaliações por restaurante      | ❌ |
| GET    | /avaliacoes                      | Listar todas as avaliações      | ❌ |

## 🍴 Avaliações de Pratos (`/avaliacoes-prato`)

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| POST   | /avaliacoes-prato                  | Avaliar prato específico           | ✅ |
| GET    | /avaliacoes-prato/item/{itemId}    | Avaliações por item                | ❌ |
| GET    | /avaliacoes-prato                  | Listar todas as avaliações de pratos| ❌ |

## 📊 Dashboard – Dados Existentes

| Método | Endpoint | Descrição | Autenticação |
|--------|-----------|------------|--------------|
| GET    | /pedidos               | Dados de vendas/pedidos        | ❌ |
| GET    | /restaurantes/{id}/itens-vendidos | Itens mais vendidos | ❌ |
| GET    | /restaurantes/{id}/estatisticas   | Estatísticas gerais | ❌ |

## 📝 Observações Importantes
- ✅ = Requer login/autenticação  
- Upload: sistema aceita imagens e PDFs  
- Dashboard retorna dados mock para demonstração  
- CORS liberado para endpoints /api/*  
- Todos os endpoints têm tratamento de erros adequado
- **STATUS: TODOS OS ENDPOINTS IMPLEMENTADOS** ✅
- **OTIMIZAÇÃO: Endpoints desnecessários removidos para simplificar o código**
- **TESTE: Execute `python test_all_endpoints.py` para verificar funcionamento**

## 🧪 Como Testar
```bash
# Testar todos os endpoints
python test_all_endpoints.py

# Testar endpoints específicos
python -c "
from api_client import SaboreAPIClient
client = SaboreAPIClient()
print('Testando login cliente:', client.login_cliente('test@email.com', 'senha'))
print('Testando produtos populares:', len(client.get_produtos_populares()))
"
```  
