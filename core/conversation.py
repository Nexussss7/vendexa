# -*- coding: utf-8 -*-
"""
VENDEXA - Gerenciador de Conversas
Gerencia o fluxo de conversas com leads
"""

from typing import Dict, List
from datetime import datetime
import json

class ConversationManager:
    """Gerencia conversas com múltiplos leads"""
    
    def __init__(self, ai_engine, prospector):
        """Inicializa o gerenciador
        
        Args:
            ai_engine: Instância do motor de IA
            prospector: Instância do prospector
        """
        self.ai_engine = ai_engine
        self.prospector = prospector
        self.active_conversations = {}
    
    def start_conversation(self, lead_id: int) -> str:
        """Inicia uma conversa com um lead
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Mensagem inicial
        """
        lead = self.prospector.get_lead(lead_id)
        if not lead:
            return "Erro: Lead não encontrado"
        
        # Inicia conversa com IA
        initial_message = self.ai_engine.start_conversation(str(lead_id), lead)
        
        # Registra interação
        self.prospector.log_interaction(
            lead_id, 
            'chat', 
            'Conversa iniciada', 
            initial_message
        )
        
        # Atualiza status
        self.prospector.update_lead_status(lead_id, 'contatado')
        
        self.active_conversations[lead_id] = {
            'started_at': datetime.now().isoformat(),
            'message_count': 1
        }
        
        return initial_message
    
    def send_message(self, lead_id: int, message: str) -> Dict:
        """Envia uma mensagem e processa a resposta
        
        Args:
            lead_id: ID do lead
            message: Mensagem do cliente
            
        Returns:
            Dicionário com resposta e análise
        """
        # Analisa intenção
        intent = self.ai_engine.analyze_intent(message)
        
        # Gera resposta
        response = self.ai_engine.send_message(str(lead_id), message)
        
        # Registra interação
        self.prospector.log_interaction(
            lead_id,
            'chat',
            message,
            response
        )
        
        # Atualiza contador de mensagens
        if lead_id in self.active_conversations:
            self.active_conversations[lead_id]['message_count'] += 1
        
        # Atualiza status baseado na intenção
        if intent.get('intencao') == 'pronto_para_comprar':
            self.prospector.update_lead_status(lead_id, 'qualificado')
        
        # Recalcula score
        score = self.prospector.calculate_lead_score(lead_id)
        
        return {
            'response': response,
            'intent': intent,
            'score': score,
            'should_send_proposal': intent.get('intencao') == 'pronto_para_comprar'
        }
    
    def generate_and_send_proposal(self, lead_id: int, requirements: str) -> str:
        """Gera e envia uma proposta comercial
        
        Args:
            lead_id: ID do lead
            requirements: Requisitos identificados
            
        Returns:
            Proposta gerada
        """
        lead = self.prospector.get_lead(lead_id)
        if not lead:
            return "Erro: Lead não encontrado"
        
        # Gera proposta
        proposal = self.ai_engine.generate_proposal(lead, requirements)
        
        # Registra
        self.prospector.log_interaction(
            lead_id,
            'proposta',
            f'Proposta gerada: {requirements}',
            proposal
        )
        
        # Atualiza status
        self.prospector.update_lead_status(lead_id, 'proposta')
        
        return proposal
    
    def end_conversation(self, lead_id: int, reason: str = 'concluido'):
        """Encerra uma conversa
        
        Args:
            lead_id: ID do lead
            reason: Motivo do encerramento
        """
        if lead_id in self.active_conversations:
            duration = datetime.now() - datetime.fromisoformat(
                self.active_conversations[lead_id]['started_at']
            )
            
            self.prospector.log_interaction(
                lead_id,
                'chat',
                f'Conversa encerrada: {reason}',
                f'Duração: {duration.total_seconds():.0f}s'
            )
            
            del self.active_conversations[lead_id]
        
        self.ai_engine.close_conversation(str(lead_id))
    
    def get_conversation_stats(self, lead_id: int) -> Dict:
        """Retorna estatísticas da conversa
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Estatísticas da conversa
        """
        history = self.prospector.get_lead_history(lead_id)
        lead = self.prospector.get_lead(lead_id)
        
        return {
            'total_interactions': len(history),
            'status': lead.get('status'),
            'score': lead.get('score'),
            'last_interaction': lead.get('ultima_interacao'),
            'is_active': lead_id in self.active_conversations
        }

if __name__ == "__main__":
    print("Gerenciador de Conversas VENDEXA inicializado com sucesso!")
