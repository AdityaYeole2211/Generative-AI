import tiktoken 


enc = tiktoken.encoding_for_model('gpt-4o')

text = "Hello, I am Aditya Yeole"

tokens = enc.encode(text)

print("Tokens = ", tokens)

#decode -> will be same 

decoded = enc.decode(tokens)

print("Decoded Text : ", decoded)