# Arquivo dos modelos de dados do bot, como classes e estruturas para armazenar informações relevantes.

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameDeal(Base):
    __tablename__ = 'game_deals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_ID = Column(String, unique=True, nullable=False)