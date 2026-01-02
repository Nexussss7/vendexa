# 🚀 VENDEXA - Guia de Deploy Profissional

## 📋 Pré-requisitos

1. ✅ Conta no Render.com (gratuita)
2. ✅ Conta no Stripe (gratuita)
3. ✅ Repositório Git (GitHub/GitLab)

## 🔧 Passo 1: Configurar Stripe

### 1.1 Criar Conta Stripe
1. Acesse: https://dashboard.stripe.com/register
2. Crie sua conta gratuita
3. Ative o modo de teste

### 1.2 Obter Chaves da API
1. Acesse: https://dashboard.stripe.com/apikeys
2. Copie:
   - **Publishable key** (começa com `pk_test_`)
   - **Secret key** (começa com `sk_test_`)
3. Cole em `config/api_keys.json`

### 1.3 Configurar Webhook
1. Acesse: https://dashboard.stripe.com/webhooks
2. Clique em "Add endpoint"
3. URL: `https://seu-app.onrender.com/api/webhook/stripe`
4. Eventos: Selecione todos de `checkout.session` e `customer.subscription`
5. Copie o **Webhook secret** (começa com `whsec_`)
6. Cole em `config/api_keys.json`

## 🌐 Passo 2: Deploy no Render.com

### 2.1 Preparar Repositório

1. **Criar repositório no GitHub**
   ```bash
   cd C:\Users\Ramon\Desktop\VENDEXA
   git init
   git add .
   git commit -m "Initial commit - VENDEXA v1.0"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/vendexa.git
   git push -u origin main
   ```

2. **Criar arquivo Procfile** (já incluído)
   ```
   web: python main.py
   ```

### 2.2 Deploy no Render

1. Acesse: https://render.com
2. Faça login/cadastro
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório GitHub
5. Configure:
   - **Name**: vendexa
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

6. **Variáveis de Ambiente**:
   Adicione em "Environment Variables":
   ```
   GOOGLE_GEMINI_API_KEY=AIzaSyBMoWhLcOz3lg4ffJ0TtNBUXUuUMdyuiaE
   STRIPE_SECRET_KEY=sk_test_SUA_CHAVE_AQUI
   STRIPE_PUBLISHABLE_KEY=pk_test_SUA_CHAVE_AQUI
   STRIPE_WEBHOOK_SECRET=whsec_SEU_SECRET_AQUI
   ADMIN_PASSWORD=vendexa2026
   ```

7. Clique em "Create Web Service"

### 2.3 Aguardar Deploy

- O Render fará o deploy automaticamente
- Aguarde 5-10 minutos
- Sua URL será: `https://vendexa.onrender.com`

## 🔐 Passo 3: Acessar Painel Admin

1. Acesse: `https://vendexa.onrender.com/admin/login`
2. **Usuário**: `admin`
3. **Senha**: `vendexa2026`

## 💳 Passo 4: Testar Pagamentos

### Cartões de Teste Stripe

**Sucesso:**
- Número: `4242 4242 4242 4242`
- Data: Qualquer data futura
- CVC: Qualquer 3 dígitos
- CEP: Qualquer

**Falha:**
- Número: `4000 0000 0000 0002`

### Testar Checkout

```bash
curl -X POST https://vendexa.onrender.com/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "starter",
    "email": "teste@exemplo.com",
    "success_url": "https://vendexa.onrender.com/success",
    "cancel_url": "https://vendexa.onrender.com/cancel"
  }'
```

## 📊 Passo 5: Monitorar Sistema

### Dashboard Admin
- URL: `https://vendexa.onrender.com/admin/dashboard`
- Métricas em tempo real
- Leads e interações
- Vendas fechadas

### Logs do Render
1. Acesse seu serviço no Render
2. Clique em "Logs"
3. Veja logs em tempo real

## 🔄 Passo 6: Atualizações

Para atualizar o sistema:

```bash
git add .
git commit -m "Atualização"
git push
```

O Render fará deploy automático!

## 🌍 Passo 7: Domínio Personalizado (Opcional)

1. No Render, vá em "Settings" → "Custom Domain"
2. Adicione seu domínio (ex: `vendexa.com.br`)
3. Configure DNS conforme instruções
4. SSL automático incluído!

## 📱 Passo 8: Integrar com Site

### Botão de Compra

```html
<button onclick="comprarVendexa('starter')">Comprar Plano Starter</button>

<script>
function comprarVendexa(planId) {
  fetch('https://vendexa.onrender.com/api/checkout', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      plan_id: planId,
      email: 'cliente@email.com',
      success_url: window.location.origin + '/sucesso',
      cancel_url: window.location.origin + '/cancelado'
    })
  })
  .then(r => r.json())
  .then(data => {
    if (data.url) window.location.href = data.url;
  });
}
</script>
```

## ✅ Checklist Final

- [ ] Stripe configurado
- [ ] Deploy no Render concluído
- [ ] Painel admin acessível
- [ ] Pagamentos testados
- [ ] Webhook configurado
- [ ] Domínio personalizado (opcional)
- [ ] Sistema monitorado

## 🆘 Suporte

**Email**: ramonrodrigo2708@gmail.com

---

**VENDEXA está no ar! 🚀**
