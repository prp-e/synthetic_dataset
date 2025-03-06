import sqlite3
import pandas as pd

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT question, answer FROM data")
rows = cursor.fetchall()

data = [item for row in rows for item in row]

print(data)

conn.close()