import random
import time
import sqlite3
from openai import OpenAI
from config import *

random.seed()

client = OpenAI(base_url = "https://api.novita.ai/v3/openai", api_key=NOVITA_AI_KEY)

def initialize_database():
    conn = sqlite3.connect("dataset.sqlite")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_question(conn, question):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data (question) VALUES (?)", (question,))
    conn.commit()
    return cursor.lastrowid

def add_answer(conn, row_id, answer):
    cursor = conn.cursor()
    cursor.execute("UPDATE data SET answer = ? WHERE id = ?", (answer, row_id))
    conn.commit()

def questions_creation(topic, language, qty):
    questions = []
    for q in range(qty):
        try:
            question = client.chat.completions.create(
            model = "deepseek/deepseek_v3",
            messages = [
                {
                    "role" : "system",
                    "content" : "You are a question generator. The user gives you a topic and a language, you must generate a question in that topic and language. Do not use markdown."
                },
                {
                    "role" : "user",
                    "content" : f"topic: {topic}\nlanguage:{language}"
                }
            ],
            temperature = 1.0,
            seed = random.randint(0, 999999999999)
        )
            questions.append(question.choices[0].message.content)
            print(f"Question {q} has been generated successfully.")
            time.sleep(5)
        except:
            print("An error occured.")
    
    return questions

def answer_creation(question, language):
    
    answer = client.chat.completions.create(
        model = "deepseek/deepseek_v3",
        messages = [
            {
                "role" : "system",
                "content" : "You are a helpful assistant and designed to provide detailed and useful information on question you've been asked. Your task is to provide a very detailed answer and use reasoning if necessary. Also the language for questions and answers are provided by the user. Use the provided data well."
            },
            {
                "role" : "user",
                "content": f"question: {question}\nlanguage:{language}"
            }
        ],
        temperature = 0.85,
        max_tokens = 4096
    )

    return answer.choices[0].message.content

if __name__ == "__main__":

    topics = [
    "abstract_algebra", "anatomy", "astronomy", "business_ethics",  "college_computer_science", "college_mathematics", "college_physics", "computer_security", "econometrics", "electrical_engineering", "elementary_mathematics", "formal_logic", "global_facts", "international_law",
    "logical_fallacies", "machine_learning", "management", "marketing", "prehistory", "public_relations", "security_studies","sociology"
]
    
    languages = ["Persian", "English", "Arabic", "Turkish"]
    qty = 100

    initialize_database()
    conn = sqlite3.connect("dataset.sqlite")

    print(f"There are {len(topics)} topics.")

    for lang in languages:
        print(f"Working on the {lang} portion of the dataset.")
        for topic in topics:
            print(f"Working on {topic}")
            questions = questions_creation(topic, lang, qty)
            for question in questions:
                row_id = add_question(conn, question)
                answer = answer_creation(conn, question)
                add_answer(conn, row_id, answer)
                print(f"{row_id} is done.")