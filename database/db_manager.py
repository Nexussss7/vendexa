# -*- coding: utf-8 -*-
"""
VENDEXA - Gerenciador de Banco de Dados
Gerencia todas as operações do banco de dados
"""

import sqlite3
from typing import Dict, List, Optional
from datetime import datetime

class DatabaseManager:
    """Gerenciador centralizado do banco de dados"""
    
    def __init__(self, db_path: str):
        """Inicializa o gerenciador
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Cria todas as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de leads
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
        
        # Tabela de interações
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
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                valor REAL,
                data_fechamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Executa uma query SELECT
        
        Args:
            query: Query SQL
            params: Parâmetros da query
            
        Returns:
            Lista de resultados
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Executa uma query INSERT/UPDATE/DELETE
        
        Args:
            query: Query SQL
            params: Parâmetros da query
            
        Returns:
            Número de linhas afetadas ou ID inserido
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return result
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas gerais do sistema
        
        Returns:
            Dicionário com estatísticas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de leads
        cursor.execute('SELECT COUNT(*) FROM leads')
        stats['total_leads'] = cursor.fetchone()[0]
        
        # Leads por status
        cursor.execute('SELECT status, COUNT(*) FROM leads GROUP BY status')
        stats['leads_por_status'] = dict(cursor.fetchall())
        
        # Total de interações
        cursor.execute('SELECT COUNT(*) FROM interacoes')
        stats['total_interacoes'] = cursor.fetchone()[0]
        
        # Total de vendas
        cursor.execute('SELECT COUNT(*), SUM(valor) FROM vendas')
        vendas_data = cursor.fetchone()
        stats['total_vendas'] = vendas_data[0]
        stats['valor_total_vendas'] = vendas_data[1] or 0
        
        # Média de score
        cursor.execute('SELECT AVG(score) FROM leads')
        stats['score_medio'] = round(cursor.fetchone()[0] or 0, 2)
        
        conn.close()
        return stats
    
    def backup_database(self, backup_path: str) -> bool:
        """Cria um backup do banco de dados
        
        Args:
            backup_path: Caminho para o arquivo de backup
            
        Returns:
            True se backup criado com sucesso
        """
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return False

if __name__ == "__main__":
    print("Gerenciador de Banco de Dados VENDEXA inicializado com sucesso!")
