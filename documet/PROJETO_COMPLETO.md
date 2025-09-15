# 🍽️ Saborê Desktop - Projeto Completo

## 📋 Resumo do Projeto

O **Saborê Desktop** é uma aplicação complementar ao sistema Saborê, desenvolvida em Python com PyQt5, focada em fornecer **relatórios avançados e análises estatísticas** para gestores de restaurantes. A aplicação se conecta ao backend Java existente para extrair dados e apresentar insights valiosos sobre o negócio.

---

## 🎯 Objetivos Alcançados

### ✅ Funcionalidades Implementadas

1. **📊 Dashboard Interativo**
   - Cards de métricas principais (vendas, pedidos, ticket médio, crescimento)
   - Gráficos em tempo real com matplotlib
   - Status de conectividade com backend

2. **💰 Análise de Vendas**
   - Filtros por período (dia, semana, mês)
   - Tabela detalhada de vendas
   - Exportação para Excel

3. **🍕 Performance de Produtos**
   - Gráfico de produtos mais vendidos
   - Análise por categoria
   - Métricas por produto

4. **📈 Relatórios Avançados**
   - Geração de relatórios personalizados
   - Exportação para PDF
   - Visualização de dados

5. **🔄 Integração com Backend**
   - Cliente API robusto com tratamento de erros
   - Conexão automática com backend Java
   - Modo demonstração para testes

---

## 🛠️ Tecnologias Utilizadas

### Core Technologies
- **Python 3.8+** - Linguagem principal
- **PyQt5** - Interface gráfica desktop
- **matplotlib** - Geração de gráficos
- **seaborn** - Estilização de gráficos
- **requests** - Comunicação HTTP
- **pandas** - Manipulação de dados
- **numpy** - Computação numérica

### Bibliotecas Adicionais
- **reportlab** - Geração de PDFs
- **openpyxl** - Exportação Excel
- **python-dotenv** - Gerenciamento de configurações

---

## 📁 Estrutura do Projeto

```
Desktop/
├── 📄 main.py                 # Aplicação principal
├── 📄 main_demo.py           # Versão com dados demo
├── 📄 main_window.py         # Interface gráfica
├── 📄 api_client.py          # Cliente da API
├── 📄 analytics.py           # Análises estatísticas
├── 📄 charts.py             # Geração de gráficos
├── 📄 data_processor.py     # Processamento de dados
├── 📄 config.py             # Configurações
├── 📄 demo_data.py          # Dados de demonstração
├── 📄 install.py            # Instalador automático
├── 📄 requirements.txt      # Dependências
├── 📄 README.md            # Documentação principal
├── 📄 INSTRUCOES.md        # Instruções detalhadas
└── 📄 PROJETO_COMPLETO.md  # Este arquivo
```

---

## 🔧 Arquivos Principais

### 1. `main.py` - Aplicação Principal
- **Função**: Ponto de entrada da aplicação
- **Recursos**: Verificação de dependências, conexão com backend, tratamento de erros
- **Características**: Logging completo, verificações automáticas

### 2. `main_window.py` - Interface Gráfica
- **Função**: Interface principal com PyQt5
- **Recursos**: Dashboard, abas de vendas/produtos/relatórios, gráficos interativos
- **Características**: Design responsivo, múltiplas abas, atualização em tempo real

### 3. `api_client.py` - Cliente API
- **Função**: Comunicação com backend Java
- **Recursos**: Endpoints para pedidos, estatísticas, itens vendidos
- **Características**: Tratamento de erros, timeout, validação de dados

### 4. `analytics.py` - Análises Estatísticas
- **Função**: Cálculos e análises avançadas
- **Recursos**: Métricas principais, tendências, previsões
- **Características**: Análises temporais, estatísticas descritivas

### 5. `charts.py` - Geração de Gráficos
- **Função**: Visualizações com matplotlib
- **Recursos**: Gráficos de linha, barras, pizza, dashboard múltiplo
- **Características**: Gráficos interativos, estilização personalizada

### 6. `data_processor.py` - Processamento de Dados
- **Função**: Manipulação e agregação de dados
- **Recursos**: Agrupamento por período, cálculos de métricas
- **Características**: Processamento eficiente, validação de dados

---

## 📊 Funcionalidades Detalhadas

### Dashboard Principal
- **Cards de Métricas**: 4 cards principais com valores em tempo real
- **Gráfico Dashboard**: 4 gráficos em layout 2x2
- **Status de Conexão**: Indicador visual de conectividade
- **Botão de Atualização**: Atualização manual dos dados

### Análise de Vendas
- **Filtros Avançados**: Data início/fim, tipo de agrupamento
- **Tabela Detalhada**: Lista completa de pedidos
- **Exportação Excel**: Dados exportáveis
- **Visualização Temporal**: Vendas ao longo do tempo

### Análise de Produtos
- **Gráfico de Popularidade**: Produtos mais vendidos
- **Tabela Comparativa**: Métricas por produto
- **Análise por Categoria**: Agrupamento por tipo
- **Ticket Médio**: Valor médio por produto

### Relatórios
- **Tipos de Relatório**: Completo, vendas, produtos, performance
- **Exportação PDF**: Relatórios profissionais
- **Preview**: Visualização antes da exportação
- **Personalização**: Configurações de relatório

---

## 🔌 Integração com Backend

### Endpoints Utilizados
```python
GET /api/pedidos                    # Lista de pedidos
GET /api/restaurantes/{id}/estatisticas  # Estatísticas
GET /api/restaurantes/{id}/itens-vendidos # Itens vendidos
```

### Formato de Dados Esperado
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
- **Conexão Perdida**: Reconexão automática
- **Dados Indisponíveis**: Mensagens informativas
- **Timeout**: Configurável
- **Validação**: Verificação de formato

---

## 🧪 Modo Demonstração

### Características
- **Dados Simulados**: 30 dias de pedidos realistas
- **12 Produtos**: Variedade de categorias
- **Padrões Realistas**: Variação por dia da semana
- **Sem Backend**: Funciona independentemente

### Uso
```bash
python main_demo.py
```

### Benefícios
- Teste sem backend
- Demonstração de funcionalidades
- Desenvolvimento e testes
- Apresentações

---

## 📦 Instalação e Configuração

### Instalação Automática
```bash
python install.py
```

### Instalação Manual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Configuração
```python
# config.py
class Settings:
    API_BASE_URL = "http://localhost:8080"
    APP_NAME = "Saborê Desktop"
    APP_VERSION = "1.0.0"
```

---

## 🚀 Como Executar

### Modo Normal (com backend)
```bash
python main.py
```

### Modo Demonstração (sem backend)
```bash
python main_demo.py
```

### Script de Execução
```bash
# Windows
run_sabore_desktop.bat

# Linux/macOS
./run_sabore_desktop.sh
```

---

## 📈 Análises Implementadas

### Métricas Principais
- **Vendas Totais**: Soma de todas as vendas
- **Total de Pedidos**: Quantidade de pedidos
- **Ticket Médio**: Vendas ÷ Pedidos
- **Crescimento**: Comparação com período anterior

### Análises Temporais
- **Vendas por Dia**: Agrupamento diário
- **Vendas por Semana**: Agrupamento semanal
- **Vendas por Mês**: Agrupamento mensal
- **Tendências**: Análise de crescimento/queda

### Análises de Produtos
- **Itens Mais Vendidos**: Ranking por quantidade
- **Performance por Categoria**: Análise por tipo
- **Ticket Médio por Produto**: Valor médio de cada item

### Análises de Horários
- **Horários de Pico**: Momentos de maior movimento
- **Performance por Dia da Semana**: Análise semanal
- **Padrões de Consumo**: Comportamento dos clientes

---

## 📊 Gráficos Disponíveis

### 1. Gráfico de Linha
- **Uso**: Vendas ao longo do tempo
- **Interação**: Hover para valores
- **Personalização**: Cores, marcadores, grid

### 2. Gráfico de Barras
- **Uso**: Produtos mais vendidos
- **Interação**: Ordenação por quantidade
- **Estilo**: Cores gradientes

### 3. Gráfico de Pizza
- **Uso**: Distribuição por categoria
- **Interação**: Clique para destacar
- **Estilo**: Cores personalizadas

### 4. Dashboard Múltiplo
- **Uso**: Visão geral com 4 gráficos
- **Layout**: 2x2 responsivo
- **Interação**: Cada gráfico independente

---

## 🔄 Funcionalidades Avançadas

### Exportação de Dados
- **Excel**: Dados tabulares completos
- **PDF**: Relatórios profissionais
- **Formatação**: Estilos personalizados

### Filtros Avançados
- **Período**: Data início/fim
- **Agrupamento**: Dia/semana/mês
- **Produtos**: Por categoria
- **Status**: Por estado do pedido

### Atualização em Tempo Real
- **Threading**: Carregamento em background
- **Status**: Indicadores visuais
- **Erro Handling**: Tratamento robusto

---

## 🐛 Tratamento de Erros

### Tipos de Erro Tratados
- **Conexão**: Perda de conectividade
- **Dados**: Formato inválido
- **Sistema**: Dependências faltando
- **Interface**: Problemas de UI

### Estratégias de Recuperação
- **Reconexão**: Automática
- **Fallback**: Dados demo
- **Logging**: Registro completo
- **Usuário**: Mensagens informativas

---

## 📈 Próximas Funcionalidades

### Planejadas
- [ ] **Notificações em Tempo Real**
- [ ] **Relatórios Automáticos**
- [ ] **Comparação entre Períodos**
- [ ] **Previsões de Vendas**
- [ ] **Análise de Clientes**
- [ ] **Integração com Sistemas de Pagamento**
- [ ] **Backup Automático de Dados**
- [ ] **Temas Personalizáveis**

### Melhorias Técnicas
- [ ] **Cache Local**: SQLite para dados
- [ ] **Performance**: Otimização de queries
- [ ] **Segurança**: Autenticação robusta
- [ ] **Testes**: Cobertura completa

---

## 📞 Suporte e Manutenção

### Logs
- `sabore_desktop.log` - Log principal
- `sabore_desktop_demo.log` - Log demo

### Documentação
- `README.md` - Guia completo
- `INSTRUCOES.md` - Instruções detalhadas
- `PROJETO_COMPLETO.md` - Este resumo

### Contato
- **Email**: suporte@sabore.com
- **Issues**: GitHub Issues
- **Documentação**: README.md

---

## 🎉 Conclusão

O **Saborê Desktop** foi desenvolvido com sucesso, oferecendo uma solução completa para análise de dados de restaurantes. A aplicação combina:

- **Interface Intuitiva**: PyQt5 com design moderno
- **Análises Avançadas**: Estatísticas robustas
- **Visualizações Profissionais**: Gráficos interativos
- **Integração Perfeita**: Conectividade com backend
- **Flexibilidade**: Modo demo para testes
- **Documentação Completa**: Guias detalhados

A aplicação está pronta para uso em produção e pode ser facilmente expandida com novas funcionalidades conforme necessário.

---

**🍽️ Projeto desenvolvido com sucesso seguindo as melhores práticas de desenvolvimento Python e PyQt5!**
