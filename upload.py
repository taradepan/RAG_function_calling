import os
import dotenv
dotenv.load_dotenv()
import json
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import random


huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path='db')
collection = client.get_or_create_collection(name="data")

def upload_db( name, age, city):
    data = f"name: {name}, Age: {age}, City: {city}"
    id=random.randint(10000, 99999)
    collection.add(
    documents=[data],
    embeddings=[huggingface_ef(data)[0]],
    ids=[str(id)]
    )
    print(f"{data} uploaded with ID: {id}")
    return json.dumps({"Message": "Data uploaded successfully"})


def search_db(input, n=5):
    embedding = huggingface_ef(input)
    
    res = collection.query(
        query_embeddings=[embedding[0]],
        n_results=n,
    )
    
    result = []
    for i in range(len(res['ids'][0])):
        result.append({
            'ID': res['ids'][0][i],
            'Data': res['documents'][0][i]
        })
    
    return json.dumps({"Data": result})

# data = [
#     {"name": "Alice", "age": 30, "city": "New York"},
#     {"name": "Bob", "age": 25, "city": "San Francisco"},
#     {"name": "Charlie", "age": 35, "city": "Los Angeles"},
#     {"name": "David", "age": 40, "city": "Chicago"},
#     {"name": "Eve", "age": 28, "city": "Houston"},
#     {"name": "Frank", "age": 33, "city": "Phoenix"},
#     {"name": "Grace", "age": 45, "city": "Philadelphia"},
#     {"name": "Hank", "age": 50, "city": "San Antonio"},
#     {"name": "Ivy", "age": 27, "city": "San Diego"},
#     {"name": "Jack", "age": 32, "city": "Dallas"}
# ]

def delete_db(id):
    collection.delete(
        ids=[id]
    )
    return json.dumps({"Message": "Data deleted successfully"})

# print(search_db("bob"))