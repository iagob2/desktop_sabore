# 📁 Arquivos Essenciais - Saborê Desktop

## 🎯 Arquivos Principais (OBRIGATÓRIOS)

### 1. **main.py** - Ponto de Entrada
- **Função**: Arquivo principal que inicia a aplicação
- **Responsabilidade**: Verificar dependências, conexão com backend e iniciar interface gráfica
- **Status**: ✅ ESSENCIAL

### 2. **main_window.py** - Interface Gráfica
- **Função**: Janela principal da aplicação com todas as abas e funcionalidades
- **Responsabilidade**: Dashboard, vendas, produtos, relatórios e gráficos
- **Status**: ✅ ESSENCIAL

### 3. **api_client.py** - Cliente da API
- **Função**: Comunicação com o backend Java
- **Responsabilidade**: Login, buscar pedidos, estatísticas, upload de arquivos
- **Status**: ✅ ESSENCIAL

### 4. **config.py** - Configurações
- **Função**: Configurações da aplicação (URL da API, tamanhos de janela, etc.)
- **Responsabilidade**: Centralizar todas as configurações
- **Status**: ✅ ESSENCIAL

### 5. **analytics.py** - Análise de Dados
- **Função**: Processamento e análise dos dados de vendas
- **Responsabilidade**: Métricas, estatísticas, tendências
- **Status**: ✅ ESSENCIAL

### 6. **charts.py** - Gráficos
- **Função**: Criação de gráficos e visualizações
- **Responsabilidade**: Gráficos de vendas, produtos, relatórios visuais
- **Status**: ✅ ESSENCIAL

### 7. **data_processor.py** - Processamento de Dados
- **Função**: Processamento e agrupamento de dados
- **Responsabilidade**: Cálculos, filtros, agregações
- **Status**: ✅ ESSENCIAL

### 8. **requirements.txt** - Dependências
- **Função**: Lista de pacotes Python necessários
- **Responsabilidade**: PyQt5, matplotlib, seaborn, numpy, pandas, etc.
- **Status**: ✅ ESSENCIAL

## 🗑️ Arquivos de Teste/Demo (PODEM SER REMOVIDOS)

### ❌ **demo_data.py** - Dados de Demonstração
- **Função**: Gerar dados fictícios para testes
- **Status**: ❌ REMOVER

### ❌ **main_demo.py** - Versão Demo
- **Função**: Versão alternativa com dados fictícios
- **Status**: ❌ REMOVER

### ❌ **sabore_desktop_demo.log** - Log de Demo
- **Função**: Arquivo de log da versão demo
- **Status**: ❌ REMOVER

## 📋 Resumo dos Arquivos Essenciais

```
Desktop/
├── main.py              # ✅ Ponto de entrada
├── main_window.py       # ✅ Interface gráfica
├── api_client.py        # ✅ Cliente da API
├── config.py            # ✅ Configurações
├── analytics.py         # ✅ Análise de dados
├── charts.py            # ✅ Gráficos
├── data_processor.py    # ✅ Processamento
└── requirements.txt     # ✅ Dependências
```

## 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar backend:**
   - Editar `config.py` se necessário
   - Garantir que o backend Java esteja rodando

3. **Executar aplicação:**
   ```bash
   python main.py
   ```

## ⚠️ Observações

- **Backend obrigatório**: A aplicação precisa do backend Java rodando
- **Python 3.11+**: Versão recomendada do Python
- **Dependências**: Todas listadas no `requirements.txt`
- **Logs**: Aplicação gera logs automaticamente
