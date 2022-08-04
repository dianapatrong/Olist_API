import os
import pandas as pd
import src.config as conf
from sqlalchemy import create_engine


engine = create_engine(f"mysql://{conf.db_username}:{conf.db_pwd}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4")
con = engine.connect()

path = "olist_dataset"
for file in os.listdir(path):
    filename = f"{path}/{file}"
    table_name = file.split(".")[0].replace("olist_", "")
    print(f"Loading {path}/{file} into {table_name} tableName")
    df = pd.read_csv(filename)
    df.to_sql(con=con, name=table_name, index=False, if_exists="replace")