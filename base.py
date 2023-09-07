import base64

with open('similarity.pkl', 'rb') as f:
    similarity_bytes = f.read()
    similarity_base64 = base64.b64encode(similarity_bytes).decode()
