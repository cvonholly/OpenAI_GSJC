import openai

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

model = "text-davinci-002"

def get_key():
    # Generate the RSA private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    enc = key.public_key().encrypt(
        bytes(open('private_key.txt', 'r').read(),'UTF-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # s =  open('private_key.txt', 'r').read()
    openai.api_key = key.decrypt(
        enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

def get_openai_ans(inp) -> dict:
    get_key()
    response = openai.Completion.create(
        model=model,
        prompt=inp,
        temperature=0.3,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    openai.api_key = "" # removing key access
    return response.choices[0]