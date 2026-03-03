# 🎮 Gaming Deals Bot

Bot em Python para monitoramento de promoções de jogos via API.

O sistema realiza múltiplas etapas de filtragem para garantir que apenas promoções relevantes sejam processadas e enviadas.

---

## 🚀 Funcionalidades

O projeto executa um pipeline de filtragem dividido em etapas:

### 1️⃣ Gravel – Remoção de duplicados

* Compara os `dealID` da API com os já salvos no banco de dados.
* Apenas promoções novas são mantidas.

### 2️⃣ Sand – Filtro de desconto

* Mantém apenas jogos com **desconto ≥ 30%**.

### 3️⃣ Coal – Filtro de avaliação

* Mantém apenas jogos com **Steam Rating ≥ 60%**.

### 4️⃣ Validação de Loja

* Apenas lojas ativas são consideradas.
* As lojas são carregadas dinamicamente da API.

---

## 🏗 Estrutura do Projeto

```
project/
│
├── main.py
├── models.py
├── database.py
├── .env
└── README.md
```

---

## 🗄 Banco de Dados

Utiliza SQLAlchemy para persistência.

Tabela principal:

### GameDeal

| Campo   | Tipo   | Descrição            |
| ------- | ------ | -------------------- |
| deal_ID | String | ID único da promoção |

---

## ⚙️ Variáveis de Ambiente (.env)

```env
stores=https://api.exemplo.com/stores
deals=https://api.exemplo.com/deals
Bot=SEU_TOKEN_AQUI
```

---

## 🔄 Fluxo de Execução

1. Carrega variáveis de ambiente.
2. Busca lojas ativas.
3. Busca promoções.
4. Remove promoções já existentes no banco.
5. Filtra por desconto.
6. Filtra por avaliação.
7. Valida loja ativa.
8. Envia mensagem via bot.

---

## 🧠 Conceitos Aplicados

* Manipulação de listas de dicionários
* Uso de `set` para comparação eficiente
* Filtros encadeados
* Persistência com SQLAlchemy
* Consumo de API com `requests`
* Separação de responsabilidades por etapas

---

## 📦 Instalação

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install requests python-dotenv sqlalchemy
```

---

## ▶️ Execução

```bash
python main.py
```

---

## 🔥 Próximas Melhorias

* Separar pipeline em funções
* Criar sistema de logs
* Implementar envio automático para Telegram
* Adicionar testes automatizados
* Criar agendamento com cron ou scheduler

---

## 👨‍💻 Autor Sebastião Brayan de Araujo Alves

Projeto desenvolvido para estudo de backend com foco em:

* Manipulação de dados de API
* Filtragem eficiente
* Arquitetura limpa

---

## 📌 Status

🟢 Em desenvolvimento
