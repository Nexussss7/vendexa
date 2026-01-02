# -*- coding: utf-8 -*-
"""
VENDEXA - Painel Administrativo
Dashboard para administradores
"""

from flask import Blueprint, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
import hashlib
import json
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Credenciais do admin (em produção, usar banco de dados)
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': hashlib.sha256('vendexa2026'.encode()).hexdigest()  # Senha: vendexa2026
}

def login_required(f):
    """Decorator para rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if (username == ADMIN_CREDENTIALS['username'] and 
            password_hash == ADMIN_CREDENTIALS['password']):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': '/admin/dashboard'})
            return redirect(url_for('admin.dashboard'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Credenciais inválidas'}), 401
            return render_template_string(LOGIN_TEMPLATE, error='Credenciais inválidas')
    
    return render_template_string(LOGIN_TEMPLATE)

@admin_bp.route('/logout')
def logout():
    """Logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    return render_template_string(DASHBOARD_TEMPLATE)

@admin_bp.route('/api/stats')
@login_required
def get_stats():
    """Retorna estatísticas para o dashboard"""
    from database.db_manager import DatabaseManager
    
    db_path = 'data/leads.db'
    db = DatabaseManager(db_path)
    stats = db.get_statistics()
    
    return jsonify(stats)

@admin_bp.route('/api/leads')
@login_required
def get_leads():
    """Lista todos os leads"""
    import sqlite3
    
    conn = sqlite3.connect('data/leads.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM leads ORDER BY data_criacao DESC LIMIT 100')
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(leads)

@admin_bp.route('/api/recent-interactions')
@login_required
def get_recent_interactions():
    """Retorna interações recentes"""
    import sqlite3
    
    conn = sqlite3.connect('data/leads.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT i.*, l.nome, l.email 
        FROM interacoes i
        JOIN leads l ON i.lead_id = l.id
        ORDER BY i.data DESC
        LIMIT 50
    ''')
    interactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(interactions)

# Templates HTML

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VENDEXA - Login Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .credentials {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
        .credentials strong { color: #333; }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🚀 VENDEXA</h1>
        <p class="subtitle">Painel Administrativo</p>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" id="username" name="username" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="password">Senha</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Entrar</button>
        </form>
        
        <div class="credentials">
            <strong>Credenciais Padrão:</strong><br>
            Usuário: <code>admin</code><br>
            Senha: <code>vendexa2026</code>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VENDEXA - Dashboard Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { font-size: 24px; }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .logout-btn:hover { background: rgba(255,255,255,0.3); }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section h2 {
            margin-bottom: 20px;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
            color: #666;
        }
        .status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-novo { background: #e3f2fd; color: #1976d2; }
        .status-contatado { background: #fff3e0; color: #f57c00; }
        .status-qualificado { background: #f3e5f5; color: #7b1fa2; }
        .status-fechado { background: #e8f5e9; color: #388e3c; }
        .loading { text-align: center; padding: 40px; color: #999; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🚀 VENDEXA - Dashboard Administrativo</h1>
            <a href="/admin/logout" class="logout-btn">Sair</a>
        </div>
    </div>
    
    <div class="container">
        <div class="stats-grid" id="stats">
            <div class="loading">Carregando estatísticas...</div>
        </div>
        
        <div class="section">
            <h2>👥 Leads Recentes</h2>
            <div id="leads">
                <div class="loading">Carregando leads...</div>
            </div>
        </div>
        
        <div class="section">
            <h2>💬 Interações Recentes</h2>
            <div id="interactions">
                <div class="loading">Carregando interações...</div>
            </div>
        </div>
    </div>
    
    <script>
        // Carrega estatísticas
        fetch('/admin/api/stats')
            .then(r => r.json())
            .then(data => {
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card">
                        <h3>Total de Leads</h3>
                        <div class="value">${data.total_leads || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Interações</h3>
                        <div class="value">${data.total_interacoes || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Vendas Fechadas</h3>
                        <div class="value">${data.total_vendas || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Valor Total</h3>
                        <div class="value">R$ ${(data.valor_total_vendas || 0).toFixed(2)}</div>
                    </div>
                `;
            });
        
        // Carrega leads
        fetch('/admin/api/leads')
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById('leads').innerHTML = '<p>Nenhum lead cadastrado ainda.</p>';
                    return;
                }
                
                let html = '<table><thead><tr><th>Nome</th><th>Email</th><th>Empresa</th><th>Status</th><th>Score</th></tr></thead><tbody>';
                data.slice(0, 10).forEach(lead => {
                    html += `<tr>
                        <td>${lead.nome}</td>
                        <td>${lead.email}</td>
                        <td>${lead.empresa || '-'}</td>
                        <td><span class="status status-${lead.status}">${lead.status}</span></td>
                        <td>${lead.score}/100</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                document.getElementById('leads').innerHTML = html;
            });
        
        // Carrega interações
        fetch('/admin/api/recent-interactions')
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById('interactions').innerHTML = '<p>Nenhuma interação registrada ainda.</p>';
                    return;
                }
                
                let html = '<table><thead><tr><th>Lead</th><th>Tipo</th><th>Mensagem</th><th>Data</th></tr></thead><tbody>';
                data.slice(0, 10).forEach(int => {
                    html += `<tr>
                        <td>${int.nome}</td>
                        <td>${int.tipo}</td>
                        <td>${(int.mensagem || '').substring(0, 50)}...</td>
                        <td>${new Date(int.data).toLocaleString('pt-BR')}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                document.getElementById('interactions').innerHTML = html;
            });
        
        // Auto-refresh a cada 30 segundos
        setInterval(() => location.reload(), 30000);
    </script>
</body>
</html>
'''
