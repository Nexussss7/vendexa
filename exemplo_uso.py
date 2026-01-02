# -*- coding: utf-8 -*-
"""
VENDEXA - Exemplo de Uso
Demonstra como usar o sistema de vendas autônomo
"""

import sys
import os
import json

# Adiciona o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ai_engine import AIEngine
from core.prospector import Prospector
from core.conversation import ConversationManager
from core.sales_closer import SalesCloser
from integrations.email_sender import EmailSender

def exemplo_completo():
    """
    Exemplo completo de uso do VENDEXA:
    1. Adiciona um lead
    2. Inicia conversa
    3. Simula interações
    4. Gera proposta
    5. Fecha venda
    """
    
    print("""
    ██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗██╗  ██╗ █████╗ 
    ██╔══██╗██╔════╝ ██║  ██║██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗
    ██████╔╝█████╗   ██║  ██║██║  ██║█████╗   ╚███╔╝ ███████║
    ██╔══██╗██╔══╝   ██║  ██║██║  ██║██╔══╝    ╚██╔╝  ██╔══██║
    ██║  ██║███████╗╚█████╔╝██████╔╝███████╗   ██║   ██║  ██║
    ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
    
    EXEMPLO DE USO - Sistema de Vendas Autônomo
    """)
    
    # Carrega configurações
    with open('config/api_keys.json', 'r', encoding='utf-8') as f:
        api_keys = json.load(f)
    
    # Inicializa componentes
    print("\n🔧 Inicializando componentes...")
    ai_engine = AIEngine(api_keys['google_gemini']['api_key'])
    prospector = Prospector('data/leads.db')
    conversation_manager = ConversationManager(ai_engine, prospector)
    sales_closer = SalesCloser(prospector, conversation_manager)
    
    print("✅ Componentes inicializados!\n")
    
    # 1. Adiciona um lead
    print("\n👤 PASSO 1: Adicionando novo lead...")
    lead_data = {
        'nome': 'Carlos Mendes',
        'email': 'carlos.mendes@techstart.com',
        'telefone': '11977777777',
        'empresa': 'TechStart Inovação',
        'cargo': 'CTO',
        'interesse': 'Automação de vendas com IA',
        'orcamento': 'R$ 8.000/mês',
        'fonte': 'exemplo'
    }
    
    lead_id = prospector.add_lead(lead_data)
    print(f"✅ Lead criado com ID: {lead_id}")
    print(f"   Nome: {lead_data['nome']}")
    print(f"   Empresa: {lead_data['empresa']}")
    
    # 2. Inicia conversa
    print("\n💬 PASSO 2: Iniciando conversa...")
    mensagem_inicial = conversation_manager.start_conversation(lead_id)
    print(f"\nVENDEXA: {mensagem_inicial}")
    
    # 3. Simula interações
    print("\n🔄 PASSO 3: Simulando conversa...")
    
    mensagens_cliente = [
        "Olá! Estou interessado em saber mais sobre automação de vendas.",
        "Quanto custa e quais são os principais benefícios?",
        "Parece interessante! Gostaria de ver uma proposta."
    ]
    
    for i, mensagem in enumerate(mensagens_cliente, 1):
        print(f"\n--- Interação {i} ---")
        print(f"CLIENTE: {mensagem}")
        
        resultado = conversation_manager.send_message(lead_id, mensagem)
        print(f"\nVENDEXA: {resultado['response']}")
        print(f"\n📊 Análise:")
        print(f"   Intenção: {resultado['intent'].get('intencao', 'N/A')}")
        print(f"   Nível de Interesse: {resultado['intent'].get('nivel_interesse', 'N/A')}")
        print(f"   Score do Lead: {resultado['score']}")
    
    # 4. Gera proposta
    print("\n📝 PASSO 4: Gerando proposta comercial...")
    requirements = "Sistema de automação de vendas com IA para equipe de 5 vendedores"
    proposta = conversation_manager.generate_and_send_proposal(lead_id, requirements)
    print(f"\n✅ Proposta gerada:\n")
    print(proposta[:500] + "...\n")
    
    # 5. Atualiza score
    print("\n⭐ PASSO 5: Calculando score do lead...")
    score = prospector.calculate_lead_score(lead_id)
    print(f"✅ Score calculado: {score}/100")
    
    if score >= 70:
        print("🔥 Este é um HOT LEAD! Pronto para fechamento.")
    
    # 6. Estatísticas
    print("\n📊 PASSO 6: Estatísticas do sistema...")
    stats = sales_closer.get_sales_metrics()
    print(f"\nEstatísticas Gerais:")
    print(f"   Total de Leads: {stats['total_leads']}")
    print(f"   Vendas Fechadas: {stats['won']}")
    print(f"   Leads Perdidos: {stats['lost']}")
    print(f"   Em Andamento: {stats['in_progress']}")
    print(f"   Taxa de Conversão: {stats['conversion_rate']}%")
    
    # 7. Hot Leads
    print("\n🔥 PASSO 7: Identificando hot leads...")
    hot_leads = sales_closer.identify_ready_leads()
    print(f"\n✅ {len(hot_leads)} hot lead(s) identificado(s)")
    
    for lead in hot_leads[:3]:  # Mostra até 3
        print(f"\n   - {lead['nome']} ({lead['empresa']})")
        print(f"     Score: {lead['score']}/100")
        print(f"     Status: {lead['status']}")
    
    print("\n" + "="*60)
    print("✅ EXEMPLO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n🚀 O VENDEXA está pronto para automatizar suas vendas!")
    print("\n📚 Para mais informações, consulte o README.md")
    print("👥 Suporte: ramonrodrigo2708@gmail.com\n")

if __name__ == "__main__":
    try:
        exemplo_completo()
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplo: {e}")
        import traceback
        traceback.print_exc()
