import sqlite3
import datasets

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()