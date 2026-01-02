# -*- coding: utf-8 -*-
"""
VENDEXA - Integração com Stripe
Processa pagamentos e assinaturas
"""

import stripe
import json
import os
from typing import Dict, Optional

class StripePayment:
    """Gerencia pagamentos via Stripe"""
    
    def __init__(self, api_key: str = None):
        """Inicializa Stripe
        
        Args:
            api_key: Chave da API do Stripe
        """
        if api_key:
            stripe.api_key = api_key
        else:
            # Tenta carregar do arquivo de configuração
            try:
                with open('config/api_keys.json', 'r', encoding='utf-8') as f:
                    keys = json.load(f)
                    stripe.api_key = keys.get('stripe', {}).get('secret_key', '')
            except:
                pass
        
        # Planos disponíveis
        self.plans = {
            'starter': {
                'name': 'Starter',
                'price': 29700,  # em centavos (R$ 297,00)
                'currency': 'brl',
                'interval': 'month',
                'features': [
                    'Até 100 leads/mês',
                    '1.000 conversas/mês',
                    'IA básica',
                    'Email marketing',
                    'Suporte por email'
                ]
            },
            'professional': {
                'name': 'Professional',
                'price': 69700,  # R$ 697,00
                'currency': 'brl',
                'interval': 'month',
                'features': [
                    'Até 500 leads/mês',
                    '5.000 conversas/mês',
                    'IA avançada',
                    'Email + WhatsApp',
                    'Suporte prioritário',
                    'Relatórios avançados'
                ]
            },
            'enterprise': {
                'name': 'Enterprise',
                'price': 149700,  # R$ 1.497,00
                'currency': 'brl',
                'interval': 'month',
                'features': [
                    'Leads ilimitados',
                    'Conversas ilimitadas',
                    'IA personalizada',
                    'Todos os canais',
                    'Suporte 24/7',
                    'API dedicada',
                    'Customizações'
                ]
            }
        }
    
    def create_checkout_session(self, plan_id: str, customer_email: str, 
                               success_url: str, cancel_url: str) -> Dict:
        """Cria sessão de checkout
        
        Args:
            plan_id: ID do plano (starter, professional, enterprise)
            customer_email: Email do cliente
            success_url: URL de sucesso
            cancel_url: URL de cancelamento
            
        Returns:
            Dados da sessão de checkout
        """
        try:
            plan = self.plans.get(plan_id)
            if not plan:
                return {'error': 'Plano não encontrado'}
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': plan['currency'],
                        'product_data': {
                            'name': f'VENDEXA - Plano {plan["name"]}',
                            'description': ', '.join(plan['features'][:3])
                        },
                        'unit_amount': plan['price'],
                        'recurring': {
                            'interval': plan['interval']
                        }
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                customer_email=customer_email,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'plan_id': plan_id,
                    'plan_name': plan['name']
                }
            )
            
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_payment_link(self, plan_id: str) -> Optional[str]:
        """Cria link de pagamento permanente
        
        Args:
            plan_id: ID do plano
            
        Returns:
            URL do link de pagamento
        """
        try:
            plan = self.plans.get(plan_id)
            if not plan:
                return None
            
            # Cria produto
            product = stripe.Product.create(
                name=f'VENDEXA - {plan["name"]}',
                description=', '.join(plan['features'])
            )
            
            # Cria preço
            price = stripe.Price.create(
                product=product.id,
                unit_amount=plan['price'],
                currency=plan['currency'],
                recurring={'interval': plan['interval']}
            )
            
            # Cria link de pagamento
            payment_link = stripe.PaymentLink.create(
                line_items=[{'price': price.id, 'quantity': 1}]
            )
            
            return payment_link.url
        except Exception as e:
            print(f"Erro ao criar link de pagamento: {e}")
            return None
    
    def verify_webhook(self, payload: bytes, sig_header: str, 
                      webhook_secret: str) -> Optional[Dict]:
        """Verifica webhook do Stripe
        
        Args:
            payload: Payload da requisição
            sig_header: Header de assinatura
            webhook_secret: Secret do webhook
            
        Returns:
            Evento verificado ou None
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        except Exception as e:
            print(f"Erro ao verificar webhook: {e}")
            return None
    
    def get_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Busca informações de assinatura
        
        Args:
            subscription_id: ID da assinatura
            
        Returns:
            Dados da assinatura
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_end': subscription.current_period_end,
                'plan': subscription.plan.nickname if subscription.plan else None
            }
        except Exception as e:
            print(f"Erro ao buscar assinatura: {e}")
            return None
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancela assinatura
        
        Args:
            subscription_id: ID da assinatura
            
        Returns:
            True se cancelado com sucesso
        """
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            print(f"Erro ao cancelar assinatura: {e}")
            return False
    
    def get_plans(self) -> Dict:
        """Retorna todos os planos disponíveis
        
        Returns:
            Dicionário com planos
        """
        return self.plans

if __name__ == "__main__":
    print("Stripe Payment Integration - VENDEXA")
    
    # Mostra planos
    stripe_payment = StripePayment()
    plans = stripe_payment.get_plans()
    
    print("\nPlanos Disponíveis:")
    for plan_id, plan in plans.items():
        print(f"\n{plan['name']} - R$ {plan['price']/100:.2f}/{plan['interval']}")
        for feature in plan['features']:
            print(f"  ✓ {feature}")
