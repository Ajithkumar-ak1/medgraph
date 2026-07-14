from pipeline import graphrag

question = "Why might a patient with excessive thirst receive insulin?"


answer = graphrag(question)


print(answer)