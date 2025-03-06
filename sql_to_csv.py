import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("dataset.sqlite")
cursor = conn.cursor()

# Fetch data
cursor.execute("SELECT question, answer FROM data")
rows = cursor.fetchall()

# Convert to a Pandas DataFrame
df = pd.DataFrame(rows, columns=["question", "answer"])

# Save to CSV with a header
csv_filename = "dataset.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file saved as {csv_filename}")

# Close the connection
conn.close()
