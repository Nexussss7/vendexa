# -*- coding: utf-8 -*-
"""
VENDEXA - Sistema Principal de Execução
Inicia o sistema de vendas autônomo
"""

import sys
import os
import json
import logging
from datetime import datetime

# Configura logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f'vendexa_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('VENDEXA')

from core.ai_engine import AIEngine
from core.prospector import Prospector
from core.conversation import ConversationManager
from core.sales_closer import SalesCloser
from integrations.email_sender import EmailSender
from database.db_manager import DatabaseManager

class VendexaSystem:
    """Sistema principal VENDEXA"""
    
    def __init__(self):
        """Inicializa o sistema"""
        logger.info("Inicializando VENDEXA...")
        
        # Carrega configurações
        self.config = self.load_config()
        self.api_keys = self.load_api_keys()
        
        # Inicializa componentes
        self.db_path = 'data/leads.db'
        self.initialize_components()
        
        logger.info("VENDEXA inicializado com sucesso!")
    
    def load_config(self):
        """Carrega configurações"""
        try:
            with open('config/config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar config.json: {e}")
            sys.exit(1)
    
    def load_api_keys(self):
        """Carrega chaves de API"""
        try:
            with open('config/api_keys.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar api_keys.json: {e}")
            sys.exit(1)
    
    def initialize_components(self):
        """Inicializa todos os componentes do sistema"""
        try:
            # Database
            self.db_manager = DatabaseManager(self.db_path)
            logger.info("Database Manager inicializado")
            
            # AI Engine
            api_key = self.api_keys['google_gemini']['api_key']
            self.ai_engine = AIEngine(api_key)
            logger.info("AI Engine inicializado")
            
            # Prospector
            self.prospector = Prospector(self.db_path)
            logger.info("Prospector inicializado")
            
            # Conversation Manager
            self.conversation_manager = ConversationManager(
                self.ai_engine, 
                self.prospector
            )
            logger.info("Conversation Manager inicializado")
            
            # Sales Closer
            self.sales_closer = SalesCloser(
                self.prospector, 
                self.conversation_manager
            )
            logger.info("Sales Closer inicializado")
            
            # Email Sender
            self.email_sender = EmailSender('config/config.json')
            logger.info("Email Sender inicializado")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar componentes: {e}")
            sys.exit(1)
    
    def start_web_server(self):
        """Inicia o servidor web"""
        logger.info("Iniciando servidor web...")
        from web.app import app
        
        host = '0.0.0.0'
        port = 5000
        
        logger.info(f"Servidor disponível em http://localhost:{port}")
        logger.info("Pressione CTRL+C para parar o servidor")
        
        app.run(host=host, port=port, debug=False)
    
    def show_status(self):
        """Mostra status do sistema"""
        stats = self.db_manager.get_statistics()
        
        print("\n" + "="*60)
        print("VENDEXA - STATUS DO SISTEMA")
        print("="*60)
        print(f"\nVersão: {self.config['sistema']['versao']}")
        print(f"Email: {self.config['sistema']['email_contato']}")
        print(f"\nEstatísticas:")
        print(f"  Total de Leads: {stats['total_leads']}")
        print(f"  Total de Interações: {stats['total_interacoes']}")
        print(f"  Total de Vendas: {stats['total_vendas']}")
        print(f"  Valor Total: R$ {stats['valor_total_vendas']:.2f}")
        print(f"  Score Médio: {stats['score_medio']}")
        print("\n" + "="*60 + "\n")

def print_banner():
    """Exibe banner do sistema"""
    print("""
    ██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗██╗  ██╗ █████╗ 
    ██╔══██╗██╔════╝ ██║  ██║██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗
    ██████╔╝█████╗   ██║  ██║██║  ██║█████╗   ╚███╔╝ ███████║
    ██╔══██╗██╔══╝   ██║  ██║██║  ██║██╔══╝    ╚██╔╝  ██╔══██║
    ██║  ██║███████╗╚█████╔╝██████╔╝███████╗   ██║   ██║  ██║
    ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
    
    Sistema de Vendas Autônomo com IA
    Vendas Inteligentes, Resultados Automáticos
    """)

def main():
    """Função principal"""
    print_banner()
    
    try:
        # Inicializa sistema
        vendexa = VendexaSystem()
        
        # Mostra status
        vendexa.show_status()
        
        # Inicia servidor web
        vendexa.start_web_server()
        
    except KeyboardInterrupt:
        logger.info("\nSistema encerrado pelo usuário")
        print("\n\nSistema VENDEXA encerrado.")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        print(f"\nErro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
