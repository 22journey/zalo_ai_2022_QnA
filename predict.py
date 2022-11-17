import json
from core.context.from_els import ElasticsearchDB
import sys
import os

sys.path = [
    os.path.join(os.path.dirname(__file__), "bertv"),
] + sys.path

from bertv.reader import Reader
reader = Reader()

context = ElasticsearchDB(
    "http://localhost:9200",
    "wikipedia_29220620",
)

file_input = "./data/train_test/zac2022_testa_only_question.json"

with open(file_input, "r") as f:
    testa = json.loads(f.read())

for d in testa["data"]:
    q = d["question"]
    print(q)
    contexts = context.find_contexts(q)
    for c in contexts:
        print(c)
        break
    break

qac = [
        (
            "thành phố biển nào là nơi diễn ra lễ hội rước đèn trung thu lớn nhất việt nam",
        """Tết trung thu tại Việt Nam . Rước đèn . Tại Phan Thiết ( Bình Thuận ) , người ta tổ chức rước đèn quy mô lớn với hàng ngàn học sinh tiểu học và trung học cơ sở diễu hành khắp các đường phố , lễ hội này được xác lập kỷ lục lớn nhất Việt Nam ."""
        ),]

for question, d in qac:
    documents = [d, ]
    #Find relevant passages from documents
    passages = documents
    
    # Select top 40 paragraphs
    passages = passages[:40]
    
    #Using reading comprehend model (BERT) to extract answer for each passage
    answers = reader.getPredictions(question,passages)
    
    #Reranking passages by answer score
    answers = [[passages[i], answers[i][0],answers[i][1]] for i in range(0,len(answers))]
    answers = [a for a in answers if a[1] != '']
    answers.sort(key = lambda x : x[2],reverse=True)
    
    print("Final result: ")
    print("Question: ", question)
    try:
        print("Passage: ", answers[0][0])
        print("Answer : ", answers[0][1])
        print("Score  : ", answers[0][2])
    except Exception as e:
        print(e)