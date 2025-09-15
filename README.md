# 🍽️ Saborê Desktop

> Aplicação desktop para relatórios e estatísticas do Saborê - Sistema de Gestão para Restaurantes

## 📋 Sobre o Projeto

O **Saborê Desktop** é uma aplicação complementar ao app mobile do Saborê, focada em fornecer **relatórios avançados e análises estatísticas** para gestores de restaurantes. A aplicação se conecta ao backend Java existente para extrair dados e apresentar insights valiosos sobre o negócio.

### 🎯 Funcionalidades Principais

- **📊 Dashboard Interativo** - Visão geral das métricas principais
- **💰 Análise de Vendas** - Relatórios detalhados de vendas por período
- **🍕 Performance de Produtos** - Itens mais vendidos e análise de popularidade
- **📈 Gráficos e Visualizações** - Gráficos interativos com matplotlib
- **📄 Exportação de Relatórios** - Exportação para Excel e PDF
- **🔄 Atualização em Tempo Real** - Dados sempre atualizados

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **PyQt5** - Interface gráfica desktop
- **matplotlib** - Geração de gráficos e visualizações
- **seaborn** - Estilização de gráficos
- **requests** - Comunicação com API REST
- **pandas** - Manipulação e análise de dados
- **reportlab** - Geração de relatórios PDF
- **openpyxl** - Exportação para Excel

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Backend Java do Saborê rodando (opcional para testes)

### Passo a Passo

1. **Clonar o projeto**
```bash
git clone <url-do-repositorio>
cd sabore/Desktop
```

2. **Criar ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Configurar conexão com backend** (opcional)
```bash
# Editar config.py se necessário
# URL padrão: http://localhost:8080
```

---

## 🚀 Como Executar

### Execução Simples
```bash
python main.py
```

### Execução com Verificações
```bash
# O script verifica automaticamente:
# - Dependências instaladas
# - Conexão com backend
# - Configurações

python main.py
```

---

## 📱 Interface da Aplicação

### Dashboard Principal
- **Cards de Métricas**: Vendas totais, pedidos, ticket médio, crescimento
- **Gráficos Interativos**: Visualização de dados em tempo real
- **Status de Conexão**: Indicador de conectividade com o backend

### Aba de Vendas
- **Filtros Avançados**: Por período, tipo de agrupamento
- **Tabela Detalhada**: Lista completa de vendas
- **Exportação**: Dados exportáveis para Excel

### Aba de Produtos
- **Gráfico de Popularidade**: Produtos mais vendidos
- **Análise de Performance**: Métricas por produto
- **Tabela Comparativa**: Comparação entre produtos

### Aba de Relatórios
- **Geração de Relatórios**: Diferentes tipos de análise
- **Exportação PDF**: Relatórios profissionais
- **Visualização**: Preview dos relatórios

---

## 🔧 Configuração

### Arquivo de Configuração (`config.py`)

```python
class Settings:
    API_BASE_URL = "http://localhost:8080"  # URL do backend
    APP_NAME = "Saborê Desktop"
    APP_VERSION = "1.0.0"
    
    # Configurações de interface
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
API_BASE_URL=http://localhost:8080
```

---

## 📊 Funcionalidades Detalhadas

### Análises Disponíveis

1. **Métricas Principais**
   - Vendas totais
   - Número de pedidos
   - Ticket médio
   - Crescimento percentual

2. **Análise Temporal**
   - Vendas por dia/semana/mês
   - Tendências de crescimento
   - Sazonalidade

3. **Análise de Produtos**
   - Itens mais vendidos
   - Performance por categoria
   - Ticket médio por produto

4. **Análise de Horários**
   - Horários de pico
   - Performance por dia da semana
   - Padrões de consumo

### Gráficos Disponíveis

- **Gráfico de Linha**: Vendas ao longo do tempo
- **Gráfico de Barras**: Produtos mais vendidos
- **Gráfico de Pizza**: Distribuição por categoria
- **Dashboard Multiplo**: Visão geral com 4 gráficos

---

## 🔌 Integração com Backend

### Endpoints Utilizados

- `GET /api/pedidos` - Lista de pedidos
- `GET /api/restaurantes/{id}/estatisticas` - Estatísticas do restaurante
- `GET /api/restaurantes/{id}/itens-vendidos` - Itens mais vendidos

### Tratamento de Erros

- Conexão perdida com backend
- Dados indisponíveis
- Timeout de requisições
- Validação de dados

---

## 📁 Estrutura do Projeto

```
Desktop/
├── main.py              # Arquivo principal
├── main_window.py       # Interface principal
├── api_client.py        # Cliente da API
├── analytics.py         # Análises estatísticas
├── charts.py           # Geração de gráficos
├── data_processor.py   # Processamento de dados
├── config.py           # Configurações
├── requirements.txt    # Dependências
└── README.md          # Este arquivo
```

---

## 🧪 Testes

### Teste de Conexão
```bash
python -c "from api_client import SaboreAPIClient; client = SaboreAPIClient(); print('Conexão OK')"
```

### Teste de Análises
```bash
python analytics.py
```

### Teste de Gráficos
```bash
python charts.py
```

---

## 🐛 Solução de Problemas

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "Conexão recusada"
- Verifique se o backend Java está rodando
- Confirme a URL em `config.py`
- Teste a conectividade: `curl http://localhost:8080`

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

---

## 📈 Próximas Funcionalidades

- [ ] **Notificações em Tempo Real**
- [ ] **Relatórios Automáticos**
- [ ] **Comparação entre Períodos**
- [ ] **Previsões de Vendas**
- [ ] **Análise de Clientes**
- [ ] **Integração com Sistemas de Pagamento**
- [ ] **Backup Automático de Dados**
- [ ] **Temas Personalizáveis**

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📞 Suporte

- **Email**: suporte@sabore.com
- **Documentação**: [docs.sabore.com](https://docs.sabore.com)
- **Issues**: [GitHub Issues](https://github.com/sabore/desktop/issues)

---

**🍽️ Desenvolvido com ❤️ pela equipe Saborê**
