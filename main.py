import random
import time
import sqlite3
from openai import OpenAI
from config import *

random.seed()

client = OpenAI(base_url = "https://api.novita.ai/v3/openai", api_key=NOVITA_AI_KEY)

def initialize_database():
    conn = sqlite3.connect("db.sqlite")
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
            time.sleep(0.5)
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
    "abstract_algebra", "anatomy", "astronomy", "business_ethics", "clinical_knowledge",
    "college_biology", "college_chemistry", "college_computer_science", "college_mathematics",
    "college_medicine", "college_physics", "computer_security", "conceptual_physics",
    "econometrics", "electrical_engineering", "elementary_mathematics", "formal_logic",
    "global_facts", "high_school_biology", "high_school_chemistry", "high_school_computer_science",
    "high_school_european_history", "high_school_geography", "high_school_government_and_politics",
    "high_school_macroeconomics", "high_school_mathematics", "high_school_microeconomics",
    "high_school_physics", "high_school_psychology", "high_school_statistics", "high_school_us_history",
    "high_school_world_history", "human_aging", "human_sexuality", "international_law",
    "jurisprudence", "logical_fallacies", "machine_learning", "management", "marketing",
    "medical_genetics", "miscellaneous", "moral_disputes", "moral_scenarios",
    "nutrition", "philosophy", "prehistory", "professional_accounting", "professional_law",
    "professional_medicine", "professional_psychology", "public_relations", "security_studies",
    "sociology", "us_foreign_policy", "virology", "world_religions"
]
    
    languages = ["Persian", "English", "Arabic", "Russian", "Hindi", "Chinese"]
    qty = 1000

    initialize_database()
    conn = sqlite3.connect("db.sqlite")

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