import requests
import json
import random
import string
import os
import tempfile
import time

# Base URL of your FastAPI server
BASE_URL = "http://localhost:80/api/v1"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    return random_string() + "@example.com"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    print(json.dumps(dict(response.headers), indent=4))
    print("Body:")
    try:
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print(response.text)
    print("--------------------")

# User-related tests
def test_user_registration(email, password):
    print("Testing User Registration")
    url = f"{BASE_URL}/users/"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    print_response(response)
    return response.json() if response.status_code == 200 else None

def test_user_login(email, password):
    print("Testing User Login")
    url = f"{BASE_URL}/login"
    data = {"username": email, "password": password}
    response = requests.post(url, data=data)
    print_response(response)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Generated token: {token}")
        return token
    else:
        print("Login failed")
        return None

def test_get_current_user(token):
    print("Testing Get Current User")
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response)

def test_update_user(token, user_id, new_email):
    print(f"Testing Update User (ID: {user_id})")
    url = f"{BASE_URL}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"email": new_email}
    response = requests.put(url, headers=headers, json=data)
    print_response(response)

def test_delete_user(token, user_id):
    print(f"Testing Delete User (ID: {user_id})")
    url = f"{BASE_URL}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print_response(response)

# Knowledgebase-related tests
def test_create_knowledgebase(token, name, description):
    print("Testing Create Knowledgebase")
    url = f"{BASE_URL}/knowledgebases/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "description": description}
    response = requests.post(url, headers=headers, json=data)
    print_response(response)
    return response.json() if response.status_code == 200 else None


def test_get_knowledgebases(token):
    print("Testing Get Knowledgebases")
    url = f"{BASE_URL}/knowledgebases/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response)

def test_get_knowledgebase(token, knowledgebase_id):
    print(f"Testing Get Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response)

def test_update_knowledgebase(token, knowledgebase_id, new_name, new_description):
    print(f"Testing Update Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": new_name, "description": new_description}
    response = requests.put(url, headers=headers, json=data)
    print_response(response)

def test_delete_knowledgebase(token, knowledgebase_id):
    print(f"Testing Delete Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print_response(response)

# Document-related tests
def create_temp_file(content):
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path

def test_create_document(token, knowledgebase_id, filename, content):
    print(f"Testing Create Document in Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}/documents/"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a temporary file
    temp_file_path = create_temp_file(content)
    
    try:
        with open(temp_file_path, 'rb') as file:
            files = {"file": (filename, file, "text/plain")}
            response = requests.post(url, headers=headers, files=files)
        
        print_response(response)
        return response.json() if response.status_code == 200 else None
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
        
def test_index_knowledgebase(token, knowledgebase_id, document_ids):
    print(f"Testing Index Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}/index"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"document_ids": document_ids}
    response = requests.post(url, headers=headers, json=data)
    print_response(response)

def test_query_knowledgebase(token, knowledgebase_id, query):
    print(f"Testing Query Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}/query"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"query": query}
    response = requests.post(url, headers=headers, json=data)
    print_response(response)
    return response.json() if response.status_code == 200 else None


def test_get_documents(token, knowledgebase_id):
    print(f"Testing Get Documents in Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}/documents/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response(response)

def test_delete_document(token, knowledgebase_id, document_id):
    print(f"Testing Delete Document (ID: {document_id}) in Knowledgebase (ID: {knowledgebase_id})")
    url = f"{BASE_URL}/knowledgebases/{knowledgebase_id}/documents/{document_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print_response(response)

def run_tests():
    # User tests
    email = random_email()
    password = random_password()
    user = test_user_registration(email, password)
    if not user:
        print("User registration failed. Aborting further tests.")
        return

    user_id = user["id"]
    token = test_user_login(email, password)
    if not token:
        print("User login failed. Aborting further tests.")
        return

    # test_get_current_user(token)
    # new_email = random_email()
    # test_update_user(token, user_id, new_email)

     # Knowledgebase tests
    kb_name = f"Test Knowledgebase {random_string()}"
    kb_description = f"Description for {kb_name}"
    knowledgebase = test_create_knowledgebase(token, kb_name, kb_description)
    if not knowledgebase:
        print("Knowledgebase creation failed. Aborting further tests.")
        return

    kb_id = knowledgebase["id"]
    test_get_knowledgebases(token)
    test_get_knowledgebase(token, kb_id)

    # Document tests
    doc_filename1 = f"test_document1_{random_string()}.txt"
    doc_content1 = "This is a test document about artificial intelligence. AI is a branch of computer science that aims to create intelligent machines."
    document1 = test_create_document(token, kb_id, doc_filename1, doc_content1)

    doc_filename2 = f"test_document2_{random_string()}.txt"
    doc_content2 = "Machine learning is a subset of AI that focuses on the development of algorithms that can learn from and make predictions or decisions based on data."
    document2 = test_create_document(token, kb_id, doc_filename2, doc_content2)

    if document1 and document2:
        doc_ids = [document1["id"], document2["id"]]
        test_get_documents(token, kb_id)

        # Indexing test
        print("Waiting for 5 seconds before indexing...")
        time.sleep(5)  # Wait for 5 seconds to ensure documents are processed
        test_index_knowledgebase(token, kb_id, doc_ids)

        print("Waiting for 10 seconds before querying...")
        time.sleep(10)  # Wait for 10 seconds to ensure indexing is complete

        # Querying test
        query = "What is artificial intelligence?"
        test_query_knowledgebase(token, kb_id, query)

        # Clean up documents
        for doc_id in doc_ids:
            test_delete_document(token, kb_id, doc_id)
    else:
        print("Skipping indexing and querying tests due to document creation failure")

    # Cleanup
    test_delete_knowledgebase(token, kb_id)
    test_delete_user(token, user_id)

    print("All tests completed.")
if __name__ == "__main__":
    run_tests()