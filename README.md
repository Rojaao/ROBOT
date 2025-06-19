# Deriv Bot (Terminal Only Version)

Este é um robô para operar na Deriv.com via API Token, com 3 estratégias baseadas em análise dos últimos 8 dígitos.

## Estratégias

- **0 Absoluto**: Se os 8 últimos dígitos forem todos acima de 3, entra em Over 3.
- **4 Acima**: Se houver 4 ou mais dígitos abaixo de 3, entra em Over 3.
- **4 Plus**: Limite aleatório de 2 a 7 dígitos abaixo de 3 para entrada.

## Uso

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o script deriv_bot.py com sua lógica personalizada.

**OBS:** Esta versão é ideal para integração futura com Streamlit ou outra interface.