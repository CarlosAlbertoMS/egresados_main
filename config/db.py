from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://usuario@localhost:3306/dbsistema")
meta = MetaData()
conn = engine.connect()