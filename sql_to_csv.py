import sqlite3
import pandas as pd

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()