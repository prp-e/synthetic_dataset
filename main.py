import random
import time
from openai import OpenAI

random.seed()

client = OpenAI(base_url = "https://text.pollinations.ai/openai", api_key="sk-0000000000000000000000000")

def questions_creation(topic, language, qty):
    questions = []
    for q in range(qty):
        try:
            question = client.chat.completions.create(
            model = "openai",
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
            time.sleep(0.25)
        except:
            print("An error occured.")
    
    return questions

def answer_creation(question):
    pass

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
