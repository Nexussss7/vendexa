# 🚀 VENDEXA - Sistema de Vendas Autônomo com IA

![VENDEXA Logo](https://img.shields.io/badge/VENDEXA-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Sobre o VENDEXA

**VENDEXA** é uma startup autônoma completa que utiliza Inteligência Artificial para:

✅ **Prospectar clientes** automaticamente  
✅ **Conversar** de forma natural e inteligente  
✅ **Vender** produtos/serviços sem intervenção humana  
✅ **Funcionar 24/7** sem parar  

### 🌟 Principais Funcionalidades

- **Motor de IA Avançado**: Utiliza Google Gemini 1.5 Flash para conversas naturais
- **Prospecção Inteligente**: Sistema de scoring automático de leads
- **Conversas Personalizadas**: Adapta-se ao perfil de cada cliente
- **Fechamento Automático**: Identifica momento certo para fechar vendas
- **Follow-up Inteligente**: Sequências automáticas de acompanhamento
- **Dashboard Web**: Interface para monitorar todas as operações
- **Email Marketing**: Envio automático de propostas e follow-ups

## 💻 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Google Gemini API**: Inteligência Artificial (GRATUITA)
- **Flask**: Framework web para API
- **SQLite**: Banco de dados local
- **SMTP**: Envio de emails

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- Conta Google (para API Gemini gratuita)
- Conexão com internet

### Passo a Passo

1. **Clone ou baixe o projeto VENDEXA**
   ```bash
   cd VENDEXA
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a API do Google Gemini**
   - A chave já está configurada em `config/api_keys.json`
   - Chave: `AIzaSyBMoWhLcOz3lg4ffJ0TtNBUXUuUMdyuiaE`
   - Limites gratuitos: 15 req/min, 1500 req/dia

4. **Configure o email (opcional)**
   - Edite `config/api_keys.json`
   - Adicione sua senha de app do Gmail
   - Crie em: https://myaccount.google.com/apppasswords

5. **Execute o sistema**
   ```bash
   python main.py
   ```

6. **Acesse o sistema**
   - Abra: http://localhost:5000
   - API estará disponível para uso

## 📚 Documentação da API

### Endpoints Principais

#### 1. Criar Lead
```http
POST /api/leads
Content-Type: application/json

{
    "nome": "João Silva",
    "email": "joao@empresa.com",
    "telefone": "11999999999",
    "empresa": "Empresa XYZ",
    "cargo": "Diretor",
    "interesse": "Automação de vendas",
    "orcamento": "R$ 5.000/mês"
}
```

#### 2. Iniciar Conversa
```http
POST /api/conversation/start/{lead_id}
```

#### 3. Enviar Mensagem
```http
POST /api/conversation/message/{lead_id}
Content-Type: application/json

{
    "message": "Gostaria de saber mais sobre os preços"
}
```

#### 4. Gerar Proposta
```http
POST /api/proposal/generate/{lead_id}
Content-Type: application/json

{
    "requirements": "Sistema de automação de vendas para 10 usuários"
}
```

#### 5. Fechar Venda
```http
POST /api/sales/close/{lead_id}
Content-Type: application/json

{
    "value": 5000.00
}
```

#### 6. Estatísticas
```http
GET /api/stats
```

#### 7. Hot Leads
```http
GET /api/hot-leads
```

## 📁 Estrutura do Projeto

```
VENDEXA/
├── core/                      # Núcleo do sistema
│   ├── ai_engine.py          # Motor de IA (Gemini)
│   ├── prospector.py         # Sistema de prospecção
│   ├── conversation.py       # Gerenciador de conversas
│   └── sales_closer.py       # Sistema de fechamento
├── database/                 # Banco de dados
│   └── db_manager.py         # Gerenciador de BD
├── integrations/             # Integrações
│   └── email_sender.py       # Envio de emails
├── web/                      # Interface web
│   └── app.py                # API Flask
├── config/                   # Configurações
│   ├── config.json           # Configurações gerais
│   └── api_keys.json         # Chaves de API
├── data/                     # Dados
│   └── leads.db              # Banco SQLite
├── logs/                     # Logs do sistema
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## 🚀 Uso Rápido

### Uso via API

```python
import requests

# Criar lead
response = requests.post('http://localhost:5000/api/leads', json={
    'nome': 'Maria Santos',
    'email': 'maria@empresa.com',
    'empresa': 'Tech Corp',
    'interesse': 'Automação'
})
lead_id = response.json()['lead_id']

# Iniciar conversa
requests.post(f'http://localhost:5000/api/conversation/start/{lead_id}')

# Enviar mensagem
response = requests.post(
    f'http://localhost:5000/api/conversation/message/{lead_id}',
    json={'message': 'Quanto custa?'}
)
print(response.json()['response'])
```

## 📊 Métricas e Relatórios

O VENDEXA rastreia automaticamente:

- 📊 Total de leads
- ✅ Taxa de conversão
- 💰 Valor total de vendas
- 🔥 Hot leads (alto potencial)
- 💬 Número de interações
- ⭐ Score médio dos leads

## ⚙️ Configurações Avançadas

### Ajustar Modelo de IA

Edite `config/config.json`:

```json
{
    "ia": {
        "modelo": "gemini-1.5-flash",
        "temperatura": 0.7,
        "max_tokens": 1000
    }
}
```

### Personalizar Follow-ups

```json
{
    "prospeccao": {
        "score_minimo_qualificacao": 60,
        "score_minimo_hot_lead": 70,
        "dias_follow_up": [2, 5, 7]
    }
}
```

## 🔒 Segurança

⚠️ **IMPORTANTE**:

- Nunca compartilhe suas chaves de API publicamente
- Não commite `api_keys.json` em repositórios públicos
- Use variáveis de ambiente em produção
- Mantenha backups regulares do banco de dados

## 👥 Suporte

- **Email**: ramonrodrigo2708@gmail.com
- **Documentação**: Veja este README
- **Issues**: Reporte problemas diretamente

## 📝 Licença

MIT License - Você pode usar, modificar e distribuir livremente.

## 🎉 Próximos Passos

1. ✅ Instalar dependências
2. ✅ Configurar API keys
3. ✅ Executar o sistema
4. 🚀 Começar a vender automaticamente!

---

**Desenvolvido com ❤️ por Ramon Rodrigo**  
**VENDEXA - Vendas Inteligentes, Resultados Automáticos**
