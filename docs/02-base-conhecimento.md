# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `gastos_ficticios_dio.csv` | CSV | Analisar renda e gastos contextualizados do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Adicionei um arquivo de controle financeiro básico que, pelo menos, eu e algumas pessoas que conheço temos o costume gerar. Nele se encontram diversas informações de gastos fixos do cliente, para que possamos testar a habilidade de análise financeira da IA.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt, o que deixa mais dinâmico caso o usuário tenha interesse em adicionar informações.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Baseado nos dados iniciais carregados por meio dos arquivos e explorando apenas o que é necessário, assim evitando possíveis alucinações e gasto de tokens.
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55

Gastos Recorrentes:
- mes,categoria,descricao,valor
- 2025-10,Aluguel,Aluguel apartamento,1800
- 2025-10,Transporte,Parcela financiamento carro,950
- 2025-10,Transporte,Combustivel,600
- 2025-10,Contas,Luz,220
- 2025-10,Alimentacao,Supermercado,900
- 2025-10,Alimentacao,Restaurantes,350
...
```
