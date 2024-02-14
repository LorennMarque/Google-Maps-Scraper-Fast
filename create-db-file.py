import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///places_data.db', echo=True)

pd.read_csv('places_data.csv').to_sql('locations', con=engine, if_exists='replace', index=False)