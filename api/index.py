# VENDEXA - Versão Serverless para Vercel
from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import google.generativeai as genai

app = Flask(__name__)

# Configurar Gemini
GEMINI_API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY', 'AIzaSyBMoWhLcOz3lg4ffJ0TtNBUXUuUMdyuiaE')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Banco de dados em memória (para demo)
leads_db = []
conversations_db = []
sales_db = []

# HTML do painel admin
ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>VENDEXA - Painel Admin</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px; }
        h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 1.1em; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .stat-card h3 { color: #667eea; font-size: 0.9em; text-transform: uppercase; margin-bottom: 10px; }
        .stat-card .number { font-size: 2.5em; font-weight: bold; color: #333; }
        .section { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .section h2 { color: #667eea; margin-bottom: 20px; }
        .btn { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 1em; font-weight: bold; }
        .btn:hover { background: #5568d3; }
        .lead-item { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #667eea; }
        .status { display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }
        .status.novo { background: #e3f2fd; color: #1976d2; }
        .status.conversando { background: #fff3e0; color: #f57c00; }
        .status.vendido { background: #e8f5e9; color: #388e3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 VENDEXA</h1>
            <p class="subtitle">Sistema Autônomo de Vendas com IA</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total de Leads</h3>
                <div class="number" id="total-leads">0</div>
            </div>
            <div class="stat-card">
                <h3>Conversas Ativas</h3>
                <div class="number" id="total-conversations">0</div>
            </div>
            <div class="stat-card">
                <h3>Vendas Realizadas</h3>
                <div class="number" id="total-sales">0</div>
            </div>
            <div class="stat-card">
                <h3>Receita Total</h3>
                <div class="number" id="total-revenue">R$ 0</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Iniciar Prospecção Automática</h2>
            <button class="btn" onclick="startProspecting()">Prospectar Novos Clientes</button>
            <button class="btn" onclick="startConversation()" style="background: #764ba2; margin-left: 10px;">Iniciar Conversas</button>
            <button class="btn" onclick="closeSales()" style="background: #28a745; margin-left: 10px;">Fechar Vendas</button>
        </div>
        
        <div class="section">
            <h2>📊 Leads Recentes</h2>
            <div id="leads-list"></div>
        </div>
        
        <div class="section">
            <h2>💬 Conversas em Andamento</h2>
            <div id="conversations-list"></div>
        </div>
        
        <div class="section">
            <h2>✅ Vendas Concluídas</h2>
            <div id="sales-list"></div>
        </div>
    </div>
    
    <script>
        function updateDashboard() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-leads').textContent = data.total_leads;
                    document.getElementById('total-conversations').textContent = data.total_conversations;
                    document.getElementById('total-sales').textContent = data.total_sales;
                    document.getElementById('total-revenue').textContent = 'R$ ' + data.total_revenue.toLocaleString('pt-BR');
                    
                    // Atualizar listas
                    updateLeadsList(data.leads);
                    updateConversationsList(data.conversations);
                    updateSalesList(data.sales);
                });
        }
        
        function updateLeadsList(leads) {
            const list = document.getElementById('leads-list');
            if (leads.length === 0) {
                list.innerHTML = '<p style="color: #999;">Nenhum lead ainda. Clique em "Prospectar Novos Clientes"</p>';
                return;
            }
            list.innerHTML = leads.map(lead => `
                <div class="lead-item">
                    <strong>${lead.company}</strong> - ${lead.contact_name}<br>
                    <small>${lead.email} | ${lead.phone}</small><br>
                    <span class="status ${lead.status}">${lead.status}</span>
                </div>
            `).join('');
        }
        
        function updateConversationsList(conversations) {
            const list = document.getElementById('conversations-list');
            if (conversations.length === 0) {
                list.innerHTML = '<p style="color: #999;">Nenhuma conversa ativa</p>';
                return;
            }
            list.innerHTML = conversations.map(conv => `
                <div class="lead-item">
                    <strong>${conv.lead_name}</strong><br>
                    <small>Última mensagem: ${conv.last_message}</small><br>
                    <span class="status conversando">Em andamento</span>
                </div>
            `).join('');
        }
        
        function updateSalesList(sales) {
            const list = document.getElementById('sales-list');
            if (sales.length === 0) {
                list.innerHTML = '<p style="color: #999;">Nenhuma venda realizada ainda</p>';
                return;
            }
            list.innerHTML = sales.map(sale => `
                <div class="lead-item">
                    <strong>${sale.company}</strong> - ${sale.plan}<br>
                    <small>Valor: R$ ${sale.value.toLocaleString('pt-BR')}</small><br>
                    <span class="status vendido">✅ Vendido</span>
                </div>
            `).join('');
        }
        
        function startProspecting() {
            fetch('/api/prospect', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert('✅ ' + data.message + '\n\nNovos leads: ' + data.new_leads);
                    updateDashboard();
                });
        }
        
        function startConversation() {
            fetch('/api/start-conversations', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert('✅ ' + data.message + '\n\nConversas iniciadas: ' + data.conversations_started);
                    updateDashboard();
                });
        }
        
        function closeSales() {
            fetch('/api/close-sales', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert('✅ ' + data.message + '\n\nVendas fechadas: ' + data.sales_closed + '\nReceita: R$ ' + data.revenue.toLocaleString('pt-BR'));
                    updateDashboard();
                });
        }
        
        // Atualizar a cada 5 segundos
        setInterval(updateDashboard, 5000);
        updateDashboard();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return ADMIN_HTML

@app.route('/api/stats')
def get_stats():
    total_revenue = sum(sale['value'] for sale in sales_db)
    return jsonify({
        'total_leads': len(leads_db),
        'total_conversations': len(conversations_db),
        'total_sales': len(sales_db),
        'total_revenue': total_revenue,
        'leads': leads_db[-10:],  # Últimos 10
        'conversations': conversations_db[-10:],
        'sales': sales_db[-10:]
    })

@app.route('/api/prospect', methods=['POST'])
def prospect():
    # Simular prospecção de leads
    new_leads = [
        {
            'id': len(leads_db) + 1,
            'company': 'Tech Solutions Ltda',
            'contact_name': 'Carlos Silva',
            'email': 'carlos@techsolutions.com.br',
            'phone': '(11) 98765-4321',
            'status': 'novo',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': len(leads_db) + 2,
            'company': 'Inovação Digital',
            'contact_name': 'Maria Santos',
            'email': 'maria@inovacaodigital.com.br',
            'phone': '(21) 97654-3210',
            'status': 'novo',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': len(leads_db) + 3,
            'company': 'StartUp Brasil',
            'contact_name': 'João Oliveira',
            'email': 'joao@startupbrasil.com',
            'phone': '(11) 96543-2109',
            'status': 'novo',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    leads_db.extend(new_leads)
    
    return jsonify({
        'success': True,
        'message': 'Prospecção realizada com sucesso!',
        'new_leads': len(new_leads)
    })

@app.route('/api/start-conversations', methods=['POST'])
def start_conversations():
    # Iniciar conversas com leads novos
    new_leads = [lead for lead in leads_db if lead['status'] == 'novo']
    
    for lead in new_leads:
        # IA gera mensagem personalizada
        prompt = f"""Você é um vendedor expert da VENDEXA, um sistema de vendas autônomo com IA.
        
Crie uma mensagem de primeiro contato para {lead['contact_name']} da empresa {lead['company']}.
        
A mensagem deve:
        - Ser profissional e amigável
        - Apresentar a VENDEXA brevemente
        - Despertar interesse
        - Ter no máximo 3 parágrafos
        
Não use saudações genéricas. Seja direto e relevante."""
        
        try:
            response = model.generate_content(prompt)
            message = response.text
        except:
            message = f"Olá {lead['contact_name']}, sou da VENDEXA e tenho uma solução que pode revolucionar as vendas da {lead['company']}!"
        
        conversation = {
            'id': len(conversations_db) + 1,
            'lead_id': lead['id'],
            'lead_name': f"{lead['contact_name']} - {lead['company']}",
            'last_message': message[:100] + '...',
            'full_message': message,
            'status': 'ativa',
            'created_at': datetime.now().isoformat()
        }
        
        conversations_db.append(conversation)
        lead['status'] = 'conversando'
    
    return jsonify({
        'success': True,
        'message': 'Conversas iniciadas com sucesso!',
        'conversations_started': len(new_leads)
    })

@app.route('/api/close-sales', methods=['POST'])
def close_sales():
    # Fechar vendas com leads em conversa
    active_conversations = [conv for conv in conversations_db if conv['status'] == 'ativa']
    
    sales_closed = 0
    total_revenue = 0
    
    plans = [
        {'name': 'Starter', 'value': 297},
        {'name': 'Professional', 'value': 697},
        {'name': 'Enterprise', 'value': 1497}
    ]
    
    for conv in active_conversations:
        # Simular fechamento (70% de taxa de conversão)
        import random
        if random.random() < 0.7:
            lead = next((l for l in leads_db if l['id'] == conv['lead_id']), None)
            if lead:
                plan = random.choice(plans)
                
                sale = {
                    'id': len(sales_db) + 1,
                    'lead_id': lead['id'],
                    'company': lead['company'],
                    'contact_name': lead['contact_name'],
                    'plan': plan['name'],
                    'value': plan['value'],
                    'status': 'pago',
                    'created_at': datetime.now().isoformat()
                }
                
                sales_db.append(sale)
                lead['status'] = 'vendido'
                conv['status'] = 'fechada'
                
                sales_closed += 1
                total_revenue += plan['value']
    
    return jsonify({
        'success': True,
        'message': 'Vendas fechadas com sucesso!',
        'sales_closed': sales_closed,
        'revenue': total_revenue
    })

# Para Vercel
if __name__ == '__main__':
    app.run(debug=True)
