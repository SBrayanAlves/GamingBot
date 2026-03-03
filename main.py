import os
import requests 
from dotenv import load_dotenv
from database import _Session
from models import GameDeal

load_dotenv()

_stores = {}

stores = os.getenv("stores")

response_stores = requests.get(stores)

if response_stores.status_code == 200:
    data_stores = response_stores.json()
    for store in data_stores:
        if store.get('isActive') == 1:
            store_id = store.get('storeID')
            store_name = store.get('storeName')

            if store_id and store_name:
                _stores[store_id] = store_name

# Dados das lojas salvas no dicionario _stores, agora vamos pegar os jogos

_deals = []
gravel = []

deals = os.getenv("deals")

response_deals = requests.get(deals)

if response_deals.status_code == 200:
    _deals = response_deals.json()

# ---
# Filtragem vulgo "Pente fino"
    
# Jogos salvos na lista _deals, agora vamos para a logica de negocio

# Comparacao do dealID
# Salva no banco de dados e retorna uma lista nova com jogos novos -> gravel{}
# Primeira Filtragem -> "dealID" -> Compara se aquela promocao ja apareceu
# Nome do processo -> Gravel 

with _Session() as session:
    deals_db = session.query(GameDeal).all()
    ids_deal = {deal.deal_ID for deal in deals_db}
    for api_dealid in _deals:
        if api_dealid["dealID"] in ids_deal: 
            #print(f"{api_dealid["dealID"]} ja existe no banco de dados")
            pass
        else:
            #print(f"{api_dealid["dealID"]} ID novo registrado")
            gravel.append(api_dealid)
            gameid = GameDeal(deal_ID=api_dealid["dealID"])
            session.add(gameid)
    session.commit()

'''
Como vai funcionar o sistema de filtragem
Exemplo de retorno API:
[ 
    {
    "internalName": "STARTREKVOYAGERACROSSTHEUNKNOWN", 
    "title": "Star Trek: Voyager - Across the Unknown", -> Mensagem
    "metacriticLink": "/game/star-trek-voyager-across-the-unknown/", 
    "dealID": "znV0gTCyWvLN8L2sP3OJ%2Bat0Vudm7h%2FQQp3ysER8S%2Bg%3D", -> Filtrado
    "storeID": "23", -> Mensagem & Comparacao 
    "gameID": "316380", 
    "salePrice": "25.79", -> Mensagem
    "normalPrice": "34.99", -> Mensagem
    "isOnSale": "1", 
    "savings": "26.293227", -> Mensagem & Filtro
    "metacriticScore": "78", 
    "steamRatingText": "Mostly Positive", 
    "steamRatingPercent": "74", -> Filtro
    "steamRatingCount": "1928", 
    "steamAppID": "2643390", 
    "releaseDate": 1771372800, 
    "lastChange": 1771584345, 
    "dealRating": "10.0", 
    "thumb": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2643390/be41ff71b3f3d73566a3aec812615e4760c7111e/capsule_231x87.jpg?t=1771840084" -> Mensagem
    },...
]
'''
# Segunda Filtragem -> "savings" == porcentagem de desconto >= 30
# Nome do processo -> Sand
# resultado = sand{}

print(type(gravel)) # -> list -> dict [{...}]
print(gravel)

sand = []

for game in gravel:
    if (float(game["savings"])) >= 30:
        print(f'jogo com {float(game["savings"]):.2f}% de desconto')
        sand.append(game)
    else:
        print("Desconto ruim")
        pass

print(sand)

# Terceira Filtragem -> "steamRatingPercent" == nota na steam >= 6
# Nome do processo -> Coal
# resultado = coal[]

coal = []

for steamratinggame in sand:
    if (float(steamratinggame["steamRatingPercent"])) >= 60:
        print(f"O jogo {steamratinggame["title"]} tem um steam rating de {steamratinggame["steamRatingPercent"]}")
        coal.append(steamratinggame)
    else:
        print(f"O Jogo {steamratinggame["title"]} e ruim")
        pass

print(coal)

# Montagem da Mensagem + Comparacao de storeID para achar a loja

for finalgame in coal:
    store_id = finalgame["storeID"]
    
    if store_id in _stores:
        store_name = _stores[store_id]
        print(f'{finalgame["title"]} está na loja {store_name}')
    else:
        print("Loja não encontrada")




