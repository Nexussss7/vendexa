# -*- coding: utf-8 -*-
"""
VENDEXA - Sistema de Fechamento de Vendas
Automatiza o processo de fechamento e follow-up
"""

from typing import Dict, List
from datetime import datetime, timedelta
import json

class SalesCloser:
    """Sistema automático de fechamento de vendas"""
    
    def __init__(self, prospector, conversation_manager):
        """Inicializa o sistema de fechamento
        
        Args:
            prospector: Instância do prospector
            conversation_manager: Instância do gerenciador de conversas
        """
        self.prospector = prospector
        self.conversation_manager = conversation_manager
    
    def identify_ready_leads(self) -> List[Dict]:
        """Identifica leads prontos para fechamento
        
        Returns:
            Lista de leads qualificados
        """
        # Busca leads com alto score
        hot_leads = self.prospector.get_hot_leads(min_score=70)
        
        ready_leads = []
        for lead in hot_leads:
            if lead['status'] in ['qualificado', 'proposta']:
                ready_leads.append(lead)
        
        return ready_leads
    
    def create_follow_up_sequence(self, lead_id: int) -> List[Dict]:
        """Cria uma sequência de follow-up automático
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Lista de ações de follow-up
        """
        lead = self.prospector.get_lead(lead_id)
        
        sequence = [
            {
                'day': 0,
                'action': 'send_proposal',
                'message': 'Enviar proposta comercial personalizada'
            },
            {
                'day': 2,
                'action': 'follow_up_1',
                'message': f'Olá {lead["nome"]}, conseguiu revisar nossa proposta? Estou à disposição para esclarecer qualquer dúvida!'
            },
            {
                'day': 5,
                'action': 'follow_up_2',
                'message': f'{lead["nome"]}, preparei algumas informações adicionais que podem ser úteis. Podemos agendar uma rápida conversa?'
            },
            {
                'day': 7,
                'action': 'final_push',
                'message': f'Olá {lead["nome"]}, esta é uma ótima oportunidade! Temos uma condição especial válida até amanhã. Vamos fechar?'
            }
        ]
        
        return sequence
    
    def send_closing_message(self, lead_id: int) -> str:
        """Envia mensagem de fechamento
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Mensagem de fechamento
        """
        lead = self.prospector.get_lead(lead_id)
        
        closing_message = f"""
🎉 Parabéns {lead['nome']}!

Estou muito feliz em poder ajudá-lo com nossa solução!

Para finalizar, preciso apenas de algumas informações:

1️⃣ Confirmação dos dados da empresa
2️⃣ Forma de pagamento preferida
3️⃣ Data desejada para início

Assim que receber essas informações, enviarei o contrato para assinatura digital.

Estamos quase lá! 🚀
"""
        
        return closing_message
    
    def handle_objection(self, objection_type: str, lead_info: Dict) -> str:
        """Trata objeções comuns
        
        Args:
            objection_type: Tipo de objeção (preco, tempo, concorrencia, etc)
            lead_info: Informações do lead
            
        Returns:
            Resposta para a objeção
        """
        objection_responses = {
            'preco': f"""
Entendo sua preocupação com o investimento, {lead_info['nome']}.

Mas veja por este ângulo: nossa solução vai gerar um retorno muito maior do que o investimento inicial.

Além disso, temos opções de pagamento flexíveis que podem se adequar melhor ao seu orçamento.

Que tal conversarmos sobre as opções disponíveis?
""",
            'tempo': f"""
{lead_info['nome']}, entendo que o tempo é precioso.

Justamente por isso nossa solução foi desenvolvida para ser rápida e fácil de implementar.

A maioria dos nossos clientes começa a ver resultados em menos de uma semana!

Podemos começar com uma implementação gradual, sem impactar sua rotina.
""",
            'concorrencia': f"""
Ótimo que esteja pesquisando, {lead_info['nome']}! Isso mostra que é uma decisão importante.

Nossos diferenciais são:
✅ Suporte 24/7 em português
✅ Implementação rápida e sem complicação
✅ Resultados comprovados
✅ Melhor custo-benefício do mercado

Que tal uma demonstração para você comparar pessoalmente?
""",
            'duvida': f"""
Claro, {lead_info['nome']}! Estou aqui justamente para esclarecer todas as suas dúvidas.

Qual aspecto você gostaria que eu explicasse melhor?

Posso preparar uma apresentação personalizada ou agendar uma demonstração ao vivo.

O que prefere?
"""
        }
        
        return objection_responses.get(objection_type, objection_responses['duvida'])
    
    def mark_as_won(self, lead_id: int, deal_value: float = 0) -> Dict:
        """Marca um lead como venda fechada
        
        Args:
            lead_id: ID do lead
            deal_value: Valor da venda
            
        Returns:
            Resumo da venda
        """
        self.prospector.update_lead_status(lead_id, 'fechado')
        
        lead = self.prospector.get_lead(lead_id)
        history = self.prospector.get_lead_history(lead_id)
        
        self.prospector.log_interaction(
            lead_id,
            'venda',
            f'Venda fechada - Valor: R$ {deal_value:.2f}',
            'Cliente convertido com sucesso!'
        )
        
        return {
            'lead_id': lead_id,
            'lead_name': lead['nome'],
            'deal_value': deal_value,
            'total_interactions': len(history),
            'conversion_date': datetime.now().isoformat(),
            'score': lead['score']
        }
    
    def mark_as_lost(self, lead_id: int, reason: str = '') -> Dict:
        """Marca um lead como perdido
        
        Args:
            lead_id: ID do lead
            reason: Motivo da perda
            
        Returns:
            Resumo
        """
        self.prospector.update_lead_status(lead_id, 'perdido')
        
        self.prospector.log_interaction(
            lead_id,
            'perda',
            f'Lead perdido - Motivo: {reason}',
            'Oportunidade não convertida'
        )
        
        lead = self.prospector.get_lead(lead_id)
        
        return {
            'lead_id': lead_id,
            'lead_name': lead['nome'],
            'reason': reason,
            'lost_date': datetime.now().isoformat()
        }
    
    def get_sales_metrics(self) -> Dict:
        """Retorna métricas de vendas
        
        Returns:
            Métricas consolidadas
        """
        import sqlite3
        
        conn = sqlite3.connect(self.prospector.db_path)
        cursor = conn.cursor()
        
        # Total de leads
        cursor.execute('SELECT COUNT(*) FROM leads')
        total_leads = cursor.fetchone()[0]
        
        # Leads por status
        cursor.execute('SELECT status, COUNT(*) FROM leads GROUP BY status')
        status_counts = dict(cursor.fetchall())
        
        # Taxa de conversão
        won = status_counts.get('fechado', 0)
        conversion_rate = (won / total_leads * 100) if total_leads > 0 else 0
        
        conn.close()
        
        return {
            'total_leads': total_leads,
            'won': won,
            'lost': status_counts.get('perdido', 0),
            'in_progress': total_leads - won - status_counts.get('perdido', 0),
            'conversion_rate': round(conversion_rate, 2),
            'status_breakdown': status_counts
        }

if __name__ == "__main__":
    print("Sistema de Fechamento VENDEXA inicializado com sucesso!")
