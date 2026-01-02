# -*- coding: utf-8 -*-
"""
VENDEXA - Sistema de Prospecção Automática
Identifica e qualifica leads automaticamente
"""

import random
import time
from datetime import datetime
from typing import Dict, List
import sqlite3

class Prospector:
    """Sistema de prospecção automática de leads"""
    
    def __init__(self, db_path: str):
        """Inicializa o prospector
        
        Args:
            db_path: Caminho para o banco de dados
        """
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT,
                empresa TEXT,
                cargo TEXT,
                interesse TEXT,
                orcamento TEXT,
                fonte TEXT,
                status TEXT DEFAULT 'novo',
                score INTEGER DEFAULT 0,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultima_interacao TIMESTAMP,
                notas TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                tipo TEXT,
                mensagem TEXT,
                resposta TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_lead(self, lead_data: Dict) -> int:
        """Adiciona um novo lead ao banco de dados
        
        Args:
            lead_data: Dados do lead
            
        Returns:
            ID do lead criado
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO leads (nome, email, telefone, empresa, cargo, interesse, orcamento, fonte)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead_data.get('nome'),
                lead_data.get('email'),
                lead_data.get('telefone', ''),
                lead_data.get('empresa', ''),
                lead_data.get('cargo', ''),
                lead_data.get('interesse', ''),
                lead_data.get('orcamento', ''),
                lead_data.get('fonte', 'manual')
            ))
            
            lead_id = cursor.lastrowid
            conn.commit()
            return lead_id
        except sqlite3.IntegrityError:
            # Email já existe
            cursor.execute('SELECT id FROM leads WHERE email = ?', (lead_data.get('email'),))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def get_lead(self, lead_id: int) -> Dict:
        """Busca um lead pelo ID
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Dados do lead
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def update_lead_status(self, lead_id: int, status: str):
        """Atualiza o status de um lead
        
        Args:
            lead_id: ID do lead
            status: Novo status (novo, contatado, qualificado, proposta, fechado, perdido)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE leads 
            SET status = ?, ultima_interacao = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, lead_id))
        
        conn.commit()
        conn.close()
    
    def calculate_lead_score(self, lead_id: int) -> int:
        """Calcula o score de qualificação do lead
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Score de 0 a 100
        """
        lead = self.get_lead(lead_id)
        if not lead:
            return 0
        
        score = 0
        
        # Pontuação por informações completas
        if lead.get('empresa'):
            score += 20
        if lead.get('cargo'):
            score += 15
        if lead.get('telefone'):
            score += 10
        if lead.get('orcamento'):
            score += 25
        
        # Pontuação por interesse
        if lead.get('interesse'):
            score += 20
        
        # Pontuação por interações
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM interacoes WHERE lead_id = ?', (lead_id,))
        num_interacoes = cursor.fetchone()[0]
        conn.close()
        
        score += min(num_interacoes * 2, 10)
        
        # Atualiza o score no banco
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE leads SET score = ? WHERE id = ?', (score, lead_id))
        conn.commit()
        conn.close()
        
        return score
    
    def get_hot_leads(self, min_score: int = 60) -> List[Dict]:
        """Retorna leads com alto potencial
        
        Args:
            min_score: Score mínimo
            
        Returns:
            Lista de leads qualificados
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM leads 
            WHERE score >= ? AND status NOT IN ('fechado', 'perdido')
            ORDER BY score DESC, data_criacao DESC
        ''', (min_score,))
        
        leads = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return leads
    
    def log_interaction(self, lead_id: int, tipo: str, mensagem: str, resposta: str = ''):
        """Registra uma interação com o lead
        
        Args:
            lead_id: ID do lead
            tipo: Tipo de interação (email, chat, telefone, etc)
            mensagem: Mensagem enviada
            resposta: Resposta recebida
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interacoes (lead_id, tipo, mensagem, resposta)
            VALUES (?, ?, ?, ?)
        ''', (lead_id, tipo, mensagem, resposta))
        
        cursor.execute('''
            UPDATE leads SET ultima_interacao = CURRENT_TIMESTAMP WHERE id = ?
        ''', (lead_id,))
        
        conn.commit()
        conn.close()
    
    def get_lead_history(self, lead_id: int) -> List[Dict]:
        """Retorna o histórico de interações de um lead
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Lista de interações
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM interacoes 
            WHERE lead_id = ?
            ORDER BY data DESC
        ''', (lead_id,))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return history

if __name__ == "__main__":
    print("Sistema de Prospecção VENDEXA inicializado com sucesso!")
