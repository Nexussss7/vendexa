# -*- coding: utf-8 -*-
"""
VENDEXA - Sistema de Envio de Emails
Envia emails automatizados usando SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import json

class EmailSender:
    """Gerencia envio de emails automáticos"""
    
    def __init__(self, config_path: str = None):
        """Inicializa o sistema de email
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config = self.load_config(config_path) if config_path else {}
        self.smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.config.get('smtp_port', 587)
        self.sender_email = self.config.get('sender_email', 'ramonrodrigo2708@gmail.com')
        self.sender_password = self.config.get('sender_password', '')
    
    def load_config(self, config_path: str) -> Dict:
        """Carrega configurações do arquivo
        
        Args:
            config_path: Caminho do arquivo de configuração
            
        Returns:
            Dicionário de configurações
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def send_email(self, to_email: str, subject: str, body: str, html: bool = True) -> bool:
        """Envia um email
        
        Args:
            to_email: Email do destinatário
            subject: Assunto do email
            body: Corpo do email
            html: Se True, envia como HTML
            
        Returns:
            True se enviado com sucesso
        """
        try:
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = to_email
            message['Subject'] = subject
            
            if html:
                html_part = MIMEText(body, 'html')
                message.attach(html_part)
            else:
                text_part = MIMEText(body, 'plain')
                message.attach(text_part)
            
            # Conecta ao servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def send_welcome_email(self, lead: Dict) -> bool:
        """Envia email de boas-vindas
        
        Args:
            lead: Dados do lead
            
        Returns:
            True se enviado com sucesso
        """
        subject = f"Bem-vindo à VENDEXA, {lead['nome']}!"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">Olá {lead['nome']}! 👋</h1>
                
                <p>Seja muito bem-vindo à <strong>VENDEXA</strong>!</p>
                
                <p>Estamos muito felizes em tê-lo conosco. Nossa missão é ajudá-lo a alcançar resultados incríveis com nossas soluções inteligentes.</p>
                
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Próximos Passos:</h3>
                    <ol>
                        <li>Conheça nossas soluções</li>
                        <li>Agende uma demonstração gratuita</li>
                        <li>Receba uma proposta personalizada</li>
                    </ol>
                </div>
                
                <p>Em breve, nossa equipe entrará em contato para entender melhor suas necessidades.</p>
                
                <p>Enquanto isso, se tiver qualquer dúvida, estamos à disposição!</p>
                
                <p style="margin-top: 30px;">
                    Atenciosamente,<br>
                    <strong>Equipe VENDEXA</strong><br>
                    <a href="mailto:ramonrodrigo2708@gmail.com">ramonrodrigo2708@gmail.com</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(lead['email'], subject, body, html=True)
    
    def send_proposal_email(self, lead: Dict, proposal: str) -> bool:
        """Envia email com proposta comercial
        
        Args:
            lead: Dados do lead
            proposal: Texto da proposta
            
        Returns:
            True se enviado com sucesso
        """
        subject = f"Proposta Comercial - VENDEXA para {lead.get('empresa', lead['nome'])}"
        
        # Converte proposta em HTML
        proposal_html = proposal.replace('\n', '<br>')
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">Proposta Comercial</h1>
                
                <div style="background-color: #f9fafb; padding: 20px; border-left: 4px solid #2563eb; margin: 20px 0;">
                    {proposal_html}
                </div>
                
                <p style="margin-top: 30px;">
                    Estou à disposição para esclarecer qualquer dúvida!<br>
                    <strong>Equipe VENDEXA</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(lead['email'], subject, body, html=True)
    
    def send_follow_up_email(self, lead: Dict, message: str) -> bool:
        """Envia email de follow-up
        
        Args:
            lead: Dados do lead
            message: Mensagem de follow-up
            
        Returns:
            True se enviado com sucesso
        """
        subject = f"Acompanhamento - {lead['nome']}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <p>{message}</p>
                
                <p style="margin-top: 30px;">
                    Atenciosamente,<br>
                    <strong>Equipe VENDEXA</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(lead['email'], subject, body, html=True)

if __name__ == "__main__":
    print("Sistema de Email VENDEXA inicializado com sucesso!")
