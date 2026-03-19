import os
import requests 
from dotenv import load_dotenv
from database import _Session
from models import GameDeal

load_dotenv()

# Def responsavel por fazer a requisicao na API de lojas e promocoes
# Retorna duas listas: _stores & _deals

def api_stores():
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
    return _stores

    # Dados das lojas salvas no dicionario _stores, agora vamos pegar os jogos

def api_deals():
    _deals = []

    deals = os.getenv("deals")

    response_deals = requests.get(deals)

    if response_deals.status_code == 200:
        _deals = response_deals.json()

    return _deals

# ---
# Filtragem vulgo "Pente fino"

# Jogos salvos na lista _deals, agora vamos para a logica de negocio

# Comparacao do dealID
# Salva no banco de dados e retorna uma lista nova com jogos novos -> gravel{}
# Primeira Filtragem -> "dealID" -> Compara se aquela promocao ja apareceu
# Nome do processo -> Gravel 

# Def responsavel por fazer a comparacao no banco de dados e salvar nos itens

def db_query(_deals):
    gravel = []

    with _Session() as session:
        deals_db = session.query(GameDeal).all()
        ids_deal = {deal.deal_ID for deal in deals_db}
        for api_dealid in _deals:
            if api_dealid.get("dealID", "0") in ids_deal: 
                pass
            else:
                gravel.append(api_dealid)
                gameid = GameDeal(deal_ID=api_dealid["dealID"])
                session.add(gameid)
        session.commit()
    return gravel

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

def sand_process(gravel):
    sand = []

    for game in gravel:
        if (float(game.get("savings", "0"))) >= 30:
            sand.append(game)
    return sand

# Terceira Filtragem -> "steamRatingPercent" == nota na steam >= 6
# Nome do processo -> Coal
# resultado = coal[]

def coal_process(sand):
    coal = []

    for steamratinggame in sand:
        if (float(steamratinggame.get("steamRatingPercent", "0"))) >= 50:
            coal.append(steamratinggame)
    return coal

# Montagem da Mensagem + Comparacao de storeID para achar a loja

def msg_telebot(coal, _stores):
    for finalgame in coal:
        store_id = finalgame.get("storeID", "0")
        
        if store_id in _stores:
            store_name = _stores.get(store_id, "null")
            print("="*50)
            print(f'{finalgame["title"]}\nDe {finalgame["normalPrice"]} por {finalgame["salePrice"]} - {float(finalgame["savings"]):.2f}% de desconto\nNota na steam: {finalgame["steamRatingPercent"]}\nLoja: {store_name}')


if __name__ == "__main__":
    result_api_store = api_stores()
    result_api_deals = api_deals()

    result_db_query = db_query(result_api_deals)
    result_sand = sand_process(result_db_query)
    result_coal = coal_process(result_sand)

    final_msg = msg_telebot(result_coal, result_api_store)

