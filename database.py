# Arquivo responsavel pela conexao com banco de dados

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base #, GameDeal

engine = create_engine('sqlite:///gaming_bot.db', echo=True)

_Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
