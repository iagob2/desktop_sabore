# 📋 Instruções de Uso - Saborê Desktop

## 🚀 Início Rápido

### 1. Instalação Automática (Recomendado)
```bash
# Execute o instalador automático
python install.py
```

### 2. Instalação Manual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Executar Aplicação

#### Modo Normal (com backend)
```bash
python main.py
```

#### Modo Demonstração (sem backend)
```bash
python main_demo.py
```

---

## 📱 Interface da Aplicação

### Dashboard Principal
O dashboard mostra as métricas principais do seu restaurante:

- **💰 Vendas Hoje**: Total de vendas do dia atual
- **🛒 Pedidos Hoje**: Número de pedidos do dia
- **🎯 Ticket Médio**: Valor médio por pedido
- **📈 Crescimento**: Percentual de crescimento comparado ao período anterior

### Aba de Vendas
- **Filtros**: Selecione período e tipo de agrupamento
- **Tabela**: Visualize todos os pedidos com detalhes
- **Exportação**: Exporte dados para Excel

### Aba de Produtos
- **Gráfico**: Produtos mais vendidos em formato visual
- **Tabela**: Análise detalhada de cada produto
- **Métricas**: Quantidade vendida, valor total e ticket médio

### Aba de Relatórios
- **Geração**: Crie diferentes tipos de relatórios
- **Exportação**: Salve relatórios em PDF
- **Visualização**: Preview dos relatórios gerados

---

## 🔧 Configuração

### Arquivo de Configuração
Edite `config.py` para personalizar:

```python
class Settings:
    API_BASE_URL = "http://localhost:8080"  # URL do seu backend
    APP_NAME = "Saborê Desktop"
    APP_VERSION = "1.0.0"
    
    # Tamanho da janela
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
```

### Variáveis de Ambiente
Crie um arquivo `.env`:
```env
API_BASE_URL=http://localhost:8080
```

---

## 📊 Funcionalidades Detalhadas

### Análises Disponíveis

#### 1. Métricas Principais
- **Vendas Totais**: Soma de todas as vendas
- **Total de Pedidos**: Quantidade de pedidos realizados
- **Ticket Médio**: Vendas totais ÷ Total de pedidos
- **Crescimento**: Comparação com período anterior

#### 2. Análise Temporal
- **Vendas por Dia**: Agrupamento diário
- **Vendas por Semana**: Agrupamento semanal
- **Vendas por Mês**: Agrupamento mensal
- **Tendências**: Análise de crescimento/queda

#### 3. Análise de Produtos
- **Itens Mais Vendidos**: Ranking por quantidade
- **Performance por Categoria**: Análise por tipo de produto
- **Ticket Médio por Produto**: Valor médio de cada item

#### 4. Análise de Horários
- **Horários de Pico**: Momentos de maior movimento
- **Performance por Dia da Semana**: Análise semanal
- **Padrões de Consumo**: Comportamento dos clientes

### Gráficos Disponíveis

#### 1. Gráfico de Linha
- **Uso**: Vendas ao longo do tempo
- **Dados**: Valores por período (dia/semana/mês)
- **Interação**: Hover para ver valores detalhados

#### 2. Gráfico de Barras
- **Uso**: Produtos mais vendidos
- **Dados**: Quantidade vendida por produto
- **Interação**: Ordenação por quantidade

#### 3. Gráfico de Pizza
- **Uso**: Distribuição por categoria
- **Dados**: Percentual de cada categoria
- **Interação**: Clique para destacar

#### 4. Dashboard Múltiplo
- **Uso**: Visão geral com 4 gráficos
- **Layout**: 2x2 com diferentes análises
- **Interação**: Cada gráfico independente

---

## 🔌 Integração com Backend

### Endpoints Utilizados
A aplicação se conecta aos seguintes endpoints:

- `GET /api/pedidos` - Lista de pedidos
- `GET /api/restaurantes/{id}/estatisticas` - Estatísticas do restaurante
- `GET /api/restaurantes/{id}/itens-vendidos` - Itens mais vendidos

### Formato dos Dados
A aplicação espera dados no seguinte formato:

```json
{
  "id": 1,
  "data_pedido": "2024-01-15T12:30:00Z",
  "valor_total": 45.90,
  "itens": [
    {
      "nome": "X-Burger",
      "valor": 25.90,
      "quantidade": 1,
      "categoria": "Lanches"
    }
  ],
  "cliente": "João Silva",
  "status": "Entregue"
}
```

### Tratamento de Erros
A aplicação trata automaticamente:
- Conexão perdida com backend
- Dados indisponíveis
- Timeout de requisições
- Validação de dados

---

## 📄 Exportação de Dados

### Exportar para Excel
1. Vá para a aba "Vendas"
2. Configure os filtros desejados
3. Clique em "📤 Exportar Excel"
4. Escolha o local para salvar

### Exportar Relatório PDF
1. Vá para a aba "Relatórios"
2. Selecione o tipo de relatório
3. Clique em "📊 Gerar Relatório"
4. Clique em "📄 Exportar PDF"
5. Escolha o local para salvar

---

## 🧪 Modo Demonstração

### Quando Usar
- Testar a aplicação sem backend
- Demonstrar funcionalidades
- Desenvolvimento e testes
- Apresentações

### Como Ativar
```bash
python main_demo.py
```

### Dados de Demonstração
O modo demo inclui:
- 30 dias de pedidos simulados
- 12 produtos diferentes
- Padrões realistas de vendas
- Variação por dia da semana

---

## 🐛 Solução de Problemas

### Erro: "Módulo não encontrado"
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Conexão recusada"
- Verifique se o backend está rodando
- Confirme a URL em `config.py`
- Teste: `curl http://localhost:8080`

### Erro: "PyQt5 não encontrado"
```bash
# Windows
pip install PyQt5

# Linux
sudo apt-get install python3-pyqt5

# macOS
brew install pyqt5
```

### Performance Lenta
- Reduza o período de análise
- Use filtros mais específicos
- Verifique a conexão com o backend
- Feche outras aplicações

### Gráficos Não Aparecem
- Verifique se matplotlib está instalado
- Reinicie a aplicação
- Verifique os logs em `sabore_desktop.log`

---

## 📈 Dicas de Uso

### 1. Filtros Eficientes
- Use períodos específicos para análises rápidas
- Combine filtros para insights precisos
- Salve configurações frequentes

### 2. Interpretação de Dados
- Compare períodos similares
- Observe tendências ao longo do tempo
- Identifique padrões sazonais

### 3. Tomada de Decisão
- Use métricas para planejamento
- Identifique produtos de sucesso
- Otimize horários de funcionamento

### 4. Relatórios Regulares
- Gere relatórios semanais
- Compare com períodos anteriores
- Documente insights importantes

---

## 🔄 Atualizações

### Verificar Atualizações
A aplicação verifica automaticamente:
- Dependências instaladas
- Conexão com backend
- Configurações válidas

### Atualizar Dados
- Clique em "🔄 Atualizar Dados"
- Aguarde o carregamento
- Verifique o status da conexão

---

## 📞 Suporte

### Logs da Aplicação
- `sabore_desktop.log` - Log principal
- `sabore_desktop_demo.log` - Log do modo demo

### Informações do Sistema
A aplicação mostra:
- Versão do Python
- Dependências instaladas
- Status da conexão
- Configurações ativas

### Contato
- **Email**: suporte@sabore.com
- **Documentação**: README.md
- **Issues**: GitHub Issues

---

**🍽️ Aproveite ao máximo o Saborê Desktop para impulsionar seu negócio!**
