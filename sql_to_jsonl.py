import sqlite3
import json

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT question, answer FROM data")
rows = cursor.fetchall()

data = [json.dumps([{"from" : "human", "value": question}, {"from" : "gpt", "value" : answer}]) for question, answer in rows]

df_title = "text\n"
data_jsonl = '\n'.join(data)

conn.close()

with open("dataset.jsonl", "w") as dataset:
    dataset.write(data_jsonl)