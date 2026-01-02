# -*- coding: utf-8 -*-
"""
VENDEXA - Motor de IA
Utiliza Google Gemini API para conversas inteligentes
"""

import google.generativeai as genai
import json
import os
from typing import Dict, List, Optional

class AIEngine:
    """Motor de IA usando Google Gemini"""
    
    def __init__(self, api_key: str):
        """Inicializa o motor de IA
        
        Args:
            api_key: Chave da API do Google Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat_sessions = {}
        
    def create_sales_prompt(self, lead_info: Dict) -> str:
        """Cria um prompt personalizado para vendas
        
        Args:
            lead_info: Informações do lead (nome, empresa, interesse, etc)
            
        Returns:
            Prompt formatado para o modelo
        """
        prompt = f"""
Você é um assistente de vendas inteligente da VENDEXA.

**SOBRE A VENDEXA:**
VENDEXA é um Sistema de Vendas Autônomo com IA que automatiza 100% do processo de vendas.

**PLANOS E PREÇOS:**

1. **Plano Starter - R$ 297/mês**
   - Até 100 leads/mês
   - 1.000 conversas/mês com IA
   - Email marketing automatizado
   - Suporte por email
   - Ideal para: Pequenas empresas e startups

2. **Plano Professional - R$ 697/mês** (MAIS POPULAR)
   - Até 500 leads/mês
   - 5.000 conversas/mês com IA
   - Email + WhatsApp automatizado
   - Suporte prioritário
   - Relatórios avançados
   - Ideal para: Médias empresas

3. **Plano Enterprise - R$ 1.497/mês**
   - Leads ILIMITADOS
   - Conversas ILIMITADAS
   - IA personalizada para seu negócio
   - Todos os canais (Email, WhatsApp, SMS)
   - Suporte 24/7 dedicado
   - API dedicada
   - Customizações sob medida
   - Ideal para: Grandes empresas

**BENEFÍCIOS:**
- ✅ Automatize 100% das vendas
- ✅ IA que vende 24 horas por dia, 7 dias por semana
- ✅ Aumente conversões em até 300%
- ✅ Reduza custos com equipe de vendas
- ✅ Escale sem limites
- ✅ ROI comprovado em 30 dias

**SEU OBJETIVO:**
1. Entender as necessidades do cliente
2. Recomendar o plano ideal baseado no tamanho da empresa
3. Destacar benefícios específicos para o negócio dele
4. Responder objeções de forma profissional
5. Conduzir ao fechamento da venda

**Informações do Lead:**
- Nome: {lead_info.get('nome', 'Cliente')}
- Empresa: {lead_info.get('empresa', 'Não informado')}
- Interesse: {lead_info.get('interesse', 'Automação de vendas')}
- Orçamento: {lead_info.get('orcamento', 'A definir')}

**IMPORTANTE:**
- Seja profissional e cordial
- Seja objetivo e claro
- Seja persuasivo mas não insistente
- Foque em agregar valor
- Sempre mencione que temos teste grátis de 7 dias
- Ao final, sempre ofereça agendar uma demonstração

Responda em português do Brasil.
"""
        return prompt
    
    def start_conversation(self, lead_id: str, lead_info: Dict) -> str:
        """Inicia uma nova conversa com um lead
        
        Args:
            lead_id: ID único do lead
            lead_info: Informações do lead
            
        Returns:
            Mensagem inicial de saudação
        """
        system_prompt = self.create_sales_prompt(lead_info)
        chat = self.model.start_chat(history=[])
        self.chat_sessions[lead_id] = chat
        
        # Mensagem inicial
        initial_message = f"""Olá {lead_info.get('nome', 'Cliente')}! 👋

Sou o assistente virtual da VENDEXA. Estou aqui para ajudá-lo a encontrar a melhor solução para suas necessidades.

Como posso ajudá-lo hoje?"""
        
        return initial_message
    
    def send_message(self, lead_id: str, message: str) -> str:
        """Envia uma mensagem e recebe resposta
        
        Args:
            lead_id: ID do lead
            message: Mensagem do cliente
            
        Returns:
            Resposta da IA
        """
        if lead_id not in self.chat_sessions:
            return "Erro: Sessão não encontrada. Inicie uma nova conversa."
        
        chat = self.chat_sessions[lead_id]
        response = chat.send_message(message)
        return response.text
    
    def analyze_intent(self, message: str) -> Dict:
        """Analisa a intenção da mensagem do cliente
        
        Args:
            message: Mensagem do cliente
            
        Returns:
            Dicionário com análise de intenção
        """
        prompt = f"""
Analise a seguinte mensagem de um cliente e identifique:
1. Intenção principal (interesse, dúvida, objeção, pronto_para_comprar, despedida)
2. Nível de interesse (baixo, médio, alto)
3. Sentimento (positivo, neutro, negativo)

Mensagem: "{message}"

Responda APENAS em formato JSON:
{{
    "intencao": "...",
    "nivel_interesse": "...",
    "sentimento": "...",
    "resumo": "..."
}}
"""
        
        response = self.model.generate_content(prompt)
        try:
            # Extrai JSON da resposta
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:-3].strip()
            elif text.startswith('```'):
                text = text[3:-3].strip()
            return json.loads(text)
        except:
            return {
                "intencao": "desconhecida",
                "nivel_interesse": "medio",
                "sentimento": "neutro",
                "resumo": "Não foi possível analisar"
            }
    
    def generate_proposal(self, lead_info: Dict, requirements: str) -> str:
        """Gera uma proposta comercial personalizada
        
        Args:
            lead_info: Informações do lead
            requirements: Requisitos identificados
            
        Returns:
            Proposta formatada
        """
        prompt = f"""
Crie uma proposta comercial profissional baseada nas seguintes informações:

Cliente: {lead_info.get('nome', 'Cliente')}
Empresa: {lead_info.get('empresa', 'Não informado')}
Requisitos: {requirements}
Orçamento: {lead_info.get('orcamento', 'A definir')}

A proposta deve incluir:
1. Saudação personalizada
2. Resumo das necessidades identificadas
3. Solução proposta
4. Benefícios principais
5. Investimento
6. Próximos passos
7. Chamada para ação

Formate de forma profissional e persuasiva.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def close_conversation(self, lead_id: str):
        """Encerra uma conversa
        
        Args:
            lead_id: ID do lead
        """
        if lead_id in self.chat_sessions:
            del self.chat_sessions[lead_id]

if __name__ == "__main__":
    # Teste básico
    print("Motor de IA VENDEXA inicializado com sucesso!")
