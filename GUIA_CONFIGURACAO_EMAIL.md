# 📧 Guia de Configuração de Email - VENDEXA

## Email Configurado

**Email**: ramonrodrigo2708@gmail.com

Este email já está configurado no sistema VENDEXA para:
- Enviar emails de boas-vindas
- Enviar propostas comerciais
- Enviar follow-ups automáticos
- Receber notificações do sistema

## 🔑 Como Obter Senha de App do Gmail

Para que o VENDEXA possa enviar emails automaticamente, você precisa criar uma **Senha de App** no Gmail:

### Passo a Passo:

1. **Acesse sua Conta Google**
   - Vá para: https://myaccount.google.com/
   - Faça login com ramonrodrigo2708@gmail.com

2. **Ative a Verificação em Duas Etapas** (se ainda não estiver ativa)
   - Vá para: https://myaccount.google.com/security
   - Clique em "Verificação em duas etapas"
   - Siga as instruções para ativar

3. **Crie uma Senha de App**
   - Vá para: https://myaccount.google.com/apppasswords
   - Selecione "Email" como app
   - Selecione "Computador Windows" como dispositivo
   - Clique em "Gerar"
   - **COPIE A SENHA GERADA** (16 caracteres)

4. **Configure no VENDEXA**
   - Abra o arquivo: `config/api_keys.json`
   - Localize a seção "email"
   - Substitua "CONFIGURE_AQUI_SUA_SENHA_DE_APP_DO_GMAIL" pela senha gerada
   - Salve o arquivo

### Exemplo de Configuração:

```json
{
    "google_gemini": {
        "api_key": "AIzaSyBMoWhLcOz3lg4ffJ0TtNBUXUuUMdyuiaE",
        ...
    },
    "email": {
        "smtp_password": "abcd efgh ijkl mnop",
        "nota": "Senha de app do Gmail"
    }
}
```

## ⚙️ Configurações SMTP

As configurações SMTP já estão pré-configuradas em `config/config.json`:

```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "ramonrodrigo2708@gmail.com",
        "sender_name": "VENDEXA"
    }
}
```

## ✅ Testando o Envio de Email

Após configurar a senha, teste o envio:

```python
from integrations.email_sender import EmailSender

# Inicializa o sender
email_sender = EmailSender('config/config.json')

# Testa envio
lead_teste = {
    'nome': 'Teste',
    'email': 'seu_email_de_teste@gmail.com'
}

sucesso = email_sender.send_welcome_email(lead_teste)
print(f"Email enviado: {sucesso}")
```

## 🚨 Solução de Problemas

### Erro: "Authentication failed"
- Verifique se a senha de app está correta
- Certifique-se de que a verificação em duas etapas está ativa
- Tente gerar uma nova senha de app

### Erro: "Connection refused"
- Verifique sua conexão com internet
- Confirme que o firewall não está bloqueando a porta 587

### Emails não chegam
- Verifique a pasta de spam
- Aguarde alguns minutos (pode haver atraso)
- Verifique se o email do destinatário está correto

## 📝 Notas Importantes

⚠️ **Segurança**:
- Nunca compartilhe sua senha de app
- Não commite o arquivo `api_keys.json` em repositórios públicos
- Revogue senhas de app que não estão mais em uso

📊 **Limites do Gmail**:
- Máximo de 500 emails por dia
- Máximo de 100 destinatários por email
- Evite enviar muitos emails em curto período (pode ser marcado como spam)

## 🔗 Links Úteis

- Senhas de App: https://myaccount.google.com/apppasswords
- Segurança da Conta: https://myaccount.google.com/security
- Suporte Gmail: https://support.google.com/mail

---

**Email configurado**: ramonrodrigo2708@gmail.com  
**Sistema**: VENDEXA v1.0.0
