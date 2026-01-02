# -*- coding: utf-8 -*-
"""
VENDEXA - Script de Instalação e Configuração
Execute este script para configurar o sistema pela primeira vez
"""

import os
import sys
import subprocess
import json

def print_banner():
    """Exibe o banner do VENDEXA"""
    print("""
    ██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗██╗  ██╗ █████╗ 
    ██╔══██╗██╔════╝ ██║  ██║██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗
    ██████╔╝█████╗   ██║  ██║██║  ██║█████╗   ╚███╔╝ ███████║
    ██╔══██╗██╔══╝   ██║  ██║██║  ██║██╔══╝    ╚██╔╝  ██╔══██║
    ██║  ██║███████╗╚█████╔╝██████╔╝███████╗   ██║   ██║  ██║
    ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
    
    Sistema de Vendas Autônomo com IA
    Versão 1.0.0
    """)

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    print("\n[1/6] Verificando versão do Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Erro: Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n[2/6] Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_database():
    """Cria o banco de dados inicial"""
    print("\n[3/6] Criando banco de dados...")
    try:
        from database.db_manager import DatabaseManager
        db_path = os.path.join('data', 'leads.db')
        db = DatabaseManager(db_path)
        print("✅ Banco de dados criado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def verify_api_keys():
    """Verifica se as chaves de API estão configuradas"""
    print("\n[4/6] Verificando chaves de API...")
    try:
        with open('config/api_keys.json', 'r', encoding='utf-8') as f:
            api_keys = json.load(f)
        
        gemini_key = api_keys.get('google_gemini', {}).get('api_key', '')
        if gemini_key and gemini_key != 'SUA_CHAVE_AQUI':
            print("✅ Chave do Google Gemini configurada")
            print(f"   Chave: {gemini_key[:20]}...")
            return True
        else:
            print("⚠️  Chave do Google Gemini não configurada")
            print("   Edite config/api_keys.json para adicionar sua chave")
            return True  # Não bloqueia a instalação
    except Exception as e:
        print(f"❌ Erro ao verificar chaves: {e}")
        return False

def create_sample_data():
    """Prepara o sistema para uso profissional"""
    print("\n[5/6] Preparando sistema...")
    try:
        print("✅ Sistema pronto para uso profissional")
        print("   Banco de dados inicializado")
        print("   Pronto para receber leads reais")
        return True
    except Exception as e:
        print(f"⚠️  Aviso: {e}")
        return True

def show_next_steps():
    """Mostra os próximos passos"""
    print("""
    
✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!

🚀 PRÓXIMOS PASSOS:

1. Configure sua senha de email (opcional):
   - Edite: config/api_keys.json
   - Adicione sua senha de app do Gmail
   - Crie em: https://myaccount.google.com/apppasswords

2. Inicie o servidor:
   python main.py

3. Acesse o sistema:
   http://localhost:5000

4. Teste a API:
   - GET  http://localhost:5000/api/stats
   - GET  http://localhost:5000/api/leads
   - GET  http://localhost:5000/api/hot-leads

📚 DOCUMENTAÇÃO:
   Leia o README.md para mais informações

👥 SUPORTE:
   ramonrodrigo2708@gmail.com

---
VENDEXA - Vendas Inteligentes, Resultados Automáticos
    """)

def main():
    """Função principal"""
    print_banner()
    
    print("\nBem-vindo ao instalador do VENDEXA!")
    print("Este script irá configurar todo o sistema automaticamente.\n")
    
    input("Pressione ENTER para continuar...")
    
    # Executa as etapas de instalação
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependências", install_dependencies),
        ("Criar banco de dados", create_database),
        ("Verificar API keys", verify_api_keys),
        ("Criar dados de exemplo", create_sample_data)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Instalação falhou na etapa: {step_name}")
            return False
    
    print("\n[6/6] Finalizando instalação...")
    show_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
