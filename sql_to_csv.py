import sqlite3
import json

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT question, answer FROM data")
rows = cursor.fetchall()

data = [f"{question}, {answer}" for question, answer in rows]

df_title = "question, answer\n"
data_csv = '\n'.join(data)

final_data = f"{df_title}{data_csv}"

conn.close()

with open("dataset.csv", "w") as dataset:
    dataset.write(final_data)