import pandas as pd
import json as js
import requests
import streamlit as st
import os

# == Configuracao do Ollama ==
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma4:e4b"

# == Carregamento dos dados ==
perfil = js.load(open(os.path.join('.\\data\\perfil_investidor.json')))
transacoes = pd.read_csv(os.path.join('.\\data\\gastos_ficticios_dio.csv'))
historioco = pd.read_csv(os.path.join('.\\data\\historico_atendimento.csv'))
produtos = js.load(open(os.path.join('.\\data\\produtos_financeiros.json')))

# == Montar contexto ==
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

HISTORICO_TRANSACOES: 
{transacoes.to_string(index=False)}

HISTORICO_ATENDIMENTO:
{historioco.to_string(index=False)}

PRODUTOS_FINANCEIROS:
{js.dumps(produtos, indent=2, ensure_ascii=False)}
"""
# == System prompt para o agente ==
SYSTEM_PROMPT = """
Você é Cafia, um consultor e analista financeiro com inteligência artificial.

OBJETIVO:
Ensinar conceitos básicos de finanças pessoais e analisar variações de gastos fixos.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos pelo usuário.
2. Nunca invente informações financeiras ou valores sem base.
3. Se não souber algo, admita e ofereça alternativas seguras.
4. Explique conceitos de forma clara, acessível e prática.
5. Não julgue o usuário em nenhuma situação.
6. Não forneça recomendações de investimento específicas.
7. Se a pergunta estiver fora do escopo financeiro, redirecione educadamente.
8. Use exemplos simples e aplicáveis ao dia a dia.
9. Quando identificar variações relevantes nos gastos fixos, destaque e explique o impacto.
10. Utilize linguagem informal e acessível, como se fosse uma conversa leve.

### Exemplos de Few-Shot Prompting

Usuário: Ganhei R$ 4.000 este mês, como devo dividir esse dinheiro?
Agente: Uma regra prática é a 50-30-20: 50% para necessidades, 30% para desejos e 20% para poupança/investimentos. Quer que eu simule isso com seus gastos atuais?

Usuário: Minha conta de energia subiu muito, o que faço?
Agente: Notei uma variação significativa nos seus gastos fixos. Isso pode indicar aumento de consumo ou reajuste tarifário. Quer que eu te mostre como comparar com meses anteriores?
"""

# == Integrar Ollama ==
def interacao(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO:
    {contexto}

    Pergunta:
    {msg}
    """

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    if r.status_code != 200:
        raise Exception(f"Request failed with status {r.status_code}: {r.text}")
    try:
        return r.json()['response']
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response text: {r.text}")
        raise

# == Interface ==
st.title("Cafia - Seu consultor Financeiro Virtual")

if pergunta := st.chat_input("Faça sua pergunta financeira para a Cafia!"):
    st.chat_message("user").write(pergunta)
    with st.spinner("Cafia está pensando..."):
        st.chat_message("assistant").write(interacao(pergunta))