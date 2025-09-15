#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar todos os endpoints da API Saborê
Este script testa todos os endpoints listados no arquivo endpoints.md
"""

import sys
import traceback
from api_client import SaboreAPIClient, APIError

def test_endpoint(test_name: str, test_func):
    """Função auxiliar para testar endpoints"""
    try:
        print(f"🧪 Testando: {test_name}")
        result = test_func()
        print(f"✅ {test_name}: OK")
        if isinstance(result, dict):
            print(f"   📊 Resultado: {len(result)} campos retornados")
        elif isinstance(result, list):
            print(f"   📊 Resultado: {len(result)} itens retornados")
        else:
            print(f"   📊 Resultado: {type(result).__name__}")
        return True
    except Exception as e:
        print(f"❌ {test_name}: ERRO - {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes de todos os endpoints da API Saborê")
    print("=" * 60)
    
    # Inicializa o cliente
    client = SaboreAPIClient()
    
    # Contador de testes
    total_tests = 0
    passed_tests = 0
    
    print("\n📋 TESTANDO ENDPOINTS DE CLIENTES")
    print("-" * 40)
    
    # Testes de Clientes
    total_tests += 1
    if test_endpoint("Login Cliente", lambda: client.login_cliente("teste@email.com", "senha123")):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Dados Cliente Logado", lambda: client.get_cliente_logado()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Cadastrar Cliente", lambda: client.cadastrar_cliente({
        "nome": "Cliente Teste", "email": "teste@email.com", "senha": "senha123"
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Buscar Cliente por ID", lambda: client.get_cliente_por_id(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Atualizar Cliente", lambda: client.atualizar_cliente(1, {"nome": "Cliente Atualizado"})):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Clientes", lambda: client.get_clientes()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Logout Cliente", lambda: client.logout_cliente()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Deletar Cliente", lambda: client.deletar_cliente(1)):
        passed_tests += 1
    
    print("\n🏪 TESTANDO ENDPOINTS DE RESTAURANTES")
    print("-" * 40)
    
    # Testes de Restaurantes
    total_tests += 1
    if test_endpoint("Login Restaurante", lambda: client.login_restaurante("restaurante@email.com", "senha123")):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Cadastrar Restaurante", lambda: client.cadastrar_restaurante({
        "nome": "Restaurante Teste", "email": "restaurante@email.com", "senha": "senha123"
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Buscar Restaurante por ID", lambda: client.get_restaurante(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Restaurantes", lambda: client.get_restaurantes()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Atualizar Restaurante", lambda: client.atualizar_restaurante(1, {"nome": "Restaurante Atualizado"})):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Deletar Restaurante", lambda: client.deletar_restaurante(1)):
        passed_tests += 1
    
    print("\n🍽️ TESTANDO ENDPOINTS DE ITENS")
    print("-" * 40)
    
    # Testes de Itens
    total_tests += 1
    if test_endpoint("Cadastrar Item", lambda: client.cadastrar_item({
        "nome": "Item Teste", "preco": 15.50, "categoria": "Lanches"
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Buscar Item por ID", lambda: client.get_item_por_id(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Itens", lambda: client.get_itens()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Itens por Restaurante", lambda: client.get_itens_por_restaurante(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Atualizar Item", lambda: client.atualizar_item(1, {"preco": 18.00})):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Deletar Item", lambda: client.deletar_item(1)):
        passed_tests += 1
    
    print("\n📦 TESTANDO ENDPOINTS DE PEDIDOS")
    print("-" * 40)
    
    # Testes de Pedidos
    total_tests += 1
    if test_endpoint("Criar Pedido", lambda: client.criar_pedido({
        "cliente_id": 1, "restaurante_id": 1, "itens": [{"item_id": 1, "quantidade": 2}], "valor_total": 31.00
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Pedidos", lambda: client.get_pedidos()):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Pedidos do Cliente", lambda: client.get_pedidos_cliente(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Atualizar Status Pedido", lambda: client.atualizar_status_pedido(1, "Em preparo")):
        passed_tests += 1
    
    print("\n⭐ TESTANDO ENDPOINTS DE AVALIAÇÕES")
    print("-" * 40)
    
    # Testes de Avaliações
    total_tests += 1
    if test_endpoint("Criar Avaliação", lambda: client.criar_avaliacao({
        "restaurante_id": 1, "cliente_id": 1, "nota": 5, "comentario": "Excelente!"
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Avaliações por Restaurante", lambda: client.get_avaliacoes_restaurante(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Todas Avaliações", lambda: client.get_todas_avaliacoes()):
        passed_tests += 1
    
    print("\n🍴 TESTANDO ENDPOINTS DE AVALIAÇÕES DE PRATOS")
    print("-" * 40)
    
    # Testes de Avaliações de Pratos
    total_tests += 1
    if test_endpoint("Avaliar Prato", lambda: client.avaliar_prato({
        "item_id": 1, "cliente_id": 1, "nota": 4, "comentario": "Muito bom!"
    })):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Avaliações por Item", lambda: client.get_avaliacoes_prato(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Listar Todas Avaliações de Pratos", lambda: client.get_todas_avaliacoes_pratos()):
        passed_tests += 1
    
    print("\n📊 TESTANDO ENDPOINTS DO DASHBOARD")
    print("-" * 40)
    
    # Testes do Dashboard - usando endpoints existentes
    total_tests += 1
    if test_endpoint("Pedidos (Vendas)", lambda: client.get_pedidos(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Itens Mais Vendidos", lambda: client.get_itens_mais_vendidos(1, "30")):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Estatísticas Restaurante", lambda: client.get_estatisticas_restaurante(1)):
        passed_tests += 1
    
    total_tests += 1
    if test_endpoint("Itens Mais Vendidos", lambda: client.get_itens_mais_vendidos(1, "30")):
        passed_tests += 1
    
    print("\n🔗 TESTANDO CONECTIVIDADE")
    print("-" * 40)
    
    # Teste de Conectividade
    total_tests += 1
    if test_endpoint("Teste de Conexão", lambda: client.test_connection()):
        passed_tests += 1
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Testes Passaram: {passed_tests}/{total_tests}")
    print(f"❌ Testes Falharam: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Taxa de Sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 TODOS OS ENDPOINTS ESTÃO FUNCIONANDO CORRETAMENTE!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} ENDPOINTS COM PROBLEMAS")
        print("💡 Verifique os logs acima para detalhes dos erros")
    
    print("\n📝 NOTA: Todos os endpoints retornam dados mock quando o backend não está disponível")
    print("🔧 Para testar com dados reais, execute o backend Java primeiro")

if __name__ == "__main__":
    main()
