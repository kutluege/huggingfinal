import requests, pprint

API_URL = "https://agents-course-unit4-scoring.hf.space"
questions = requests.get(f"{API_URL}/questions", timeout=15).json()   # tüm liste

print(f"Toplam {len(questions)} soru geldi.")
pprint.pp(questions[::])                                             # ilk 3 soruyu yazdır
