# -*- coding: utf-8 -*-
"""
VENDEXA - API Web
Interface web para gerenciar o sistema
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sys
import os
import json
import secrets

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ai_engine import AIEngine
from core.prospector import Prospector
from core.conversation import ConversationManager
from core.sales_closer import SalesCloser
from integrations.email_sender import EmailSender

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Registra blueprint do admin
from web.admin_panel import admin_bp
app.register_blueprint(admin_bp)

# Configurações
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
API_KEYS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'api_keys.json')
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'leads.db')

# Carrega configurações
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

with open(API_KEYS_PATH, 'r', encoding='utf-8') as f:
    api_keys = json.load(f)

# Inicializa componentes
ai_engine = AIEngine(api_keys['google_gemini']['api_key'])
prospector = Prospector(DB_PATH)
conversation_manager = ConversationManager(ai_engine, prospector)
sales_closer = SalesCloser(prospector, conversation_manager)
email_sender = EmailSender()

@app.route('/')
def index():
    """Página inicial"""
    return jsonify({
        'sistema': 'VENDEXA',
        'versao': config['sistema']['versao'],
        'status': 'online',
        'mensagem': 'Sistema de Vendas Autônomo Operacional'
    })

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Lista todos os leads"""
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leads ORDER BY data_criacao DESC')
        leads = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'leads': leads})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leads', methods=['POST'])
def create_lead():
    """Cria um novo lead"""
    try:
        data = request.json
        lead_id = prospector.add_lead(data)
        
        if lead_id:
            # Envia email de boas-vindas
            lead = prospector.get_lead(lead_id)
            email_sender.send_welcome_email(lead)
            
            return jsonify({
                'success': True,
                'lead_id': lead_id,
                'message': 'Lead criado com sucesso!'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Email já cadastrado'
            }), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Busca um lead específico"""
    try:
        lead = prospector.get_lead(lead_id)
        if lead:
            return jsonify({'success': True, 'lead': lead})
        else:
            return jsonify({'success': False, 'error': 'Lead não encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/conversation/start/<int:lead_id>', methods=['POST'])
def start_conversation(lead_id):
    """Inicia uma conversa com um lead"""
    try:
        message = conversation_manager.start_conversation(lead_id)
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/conversation/message/<int:lead_id>', methods=['POST'])
def send_message(lead_id):
    """Envia uma mensagem na conversa"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        result = conversation_manager.send_message(lead_id, user_message)
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'intent': result['intent'],
            'score': result['score']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/proposal/generate/<int:lead_id>', methods=['POST'])
def generate_proposal(lead_id):
    """Gera uma proposta comercial"""
    try:
        data = request.json
        requirements = data.get('requirements', '')
        
        proposal = conversation_manager.generate_and_send_proposal(lead_id, requirements)
        
        # Envia por email
        lead = prospector.get_lead(lead_id)
        email_sender.send_proposal_email(lead, proposal)
        
        return jsonify({
            'success': True,
            'proposal': proposal
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sales/close/<int:lead_id>', methods=['POST'])
def close_sale(lead_id):
    """Fecha uma venda"""
    try:
        data = request.json
        deal_value = data.get('value', 0)
        
        result = sales_closer.mark_as_won(lead_id, deal_value)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas do sistema"""
    try:
        stats = sales_closer.get_sales_metrics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/hot-leads', methods=['GET'])
def get_hot_leads():
    """Retorna leads com alto potencial"""
    try:
        hot_leads = sales_closer.identify_ready_leads()
        return jsonify({
            'success': True,
            'hot_leads': hot_leads
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Rotas de Pagamento (Stripe)
@app.route('/api/plans', methods=['GET'])
def get_plans():
    """Lista planos disponíveis"""
    from integrations.stripe_payment import StripePayment
    stripe_payment = StripePayment()
    plans = stripe_payment.get_plans()
    return jsonify({'success': True, 'plans': plans})

@app.route('/api/checkout', methods=['POST'])
def create_checkout():
    """Cria sessão de checkout"""
    try:
        from integrations.stripe_payment import StripePayment
        data = request.json
        
        stripe_payment = StripePayment()
        result = stripe_payment.create_checkout_session(
            plan_id=data.get('plan_id'),
            customer_email=data.get('email'),
            success_url=data.get('success_url', 'http://localhost:5000/success'),
            cancel_url=data.get('cancel_url', 'http://localhost:5000/cancel')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("""
    ██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗██╗  ██╗ █████╗ 
    ██╔══██╗██╔════╝ ██║  ██║██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗
    ██████╔╝█████╗   ██║  ██║██║  ██║█████╗   ╚███╔╝ ███████║
    ██╔══██╗██╔══╝   ██║  ██║██║  ██║██╔══╝    ╚██╔╝  ██╔══██║
    ██║  ██║███████╗╚█████╔╝██████╔╝███████╗   ██║   ██║  ██║
    ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
    
    Sistema de Vendas Autônomo v{config['sistema']['versao']}
    Servidor iniciado em: http://localhost:5000
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
