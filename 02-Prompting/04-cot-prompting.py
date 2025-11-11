from openai import OpenAI
from dotenv import load_dotenv
import json 
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url= 'https://generativelanguage.googleapis.com/v1beta/openai/'
)

# Chain of Thought prompting: Model is encouraged to break reasoning step by step before arriving at a conclusion.
SYSTEM_PROMPT = '''
You are a helpful AI assistant specialized in solving user queries. 
If a user input a query , you analyze it and break it down step by step before returning the answer.
The steps are you recieve a query , you analyze it, you think , you think again , you think several times and 
then you calculate, validate your answer and then return the result.

The order of the steps are : "Analyze", "Think", "Output", "Validate", and "Result".
Rules to follow at any cost : 
1. Follow the strict JSON schema as per format.
2. Always perform one step at a time and wait for next input.
3. Carefully analyze the user query.
4. Give output one step at a time.
5. Always output exactly one JSON object per response. Never output multiple objects at once.
Output Format : 
{{"step" : "string", "content" : "string"}}

Example:
Input: What is  6/3 - 2 ?
Output : {{"step" : "analyze", "content" : "Alright, The user is interest in a maths query and the query involves mutliple operators and operands."}}
Output : {{"step": "think", content : "BODMAS rule should be applied here as multiple operators with varying precendence are present in query."}}
Output : {{"step" : "validate", "content" : "Yes, Bodmas is the rule that should be applied here."}}
Output : {{"step" : "think", "content" : "The query involves two operators : division and substraction. Division should be done first according to BODMAS."}}
Output : {{"step" : "validate", "content" : "Yes according to BODMAS, Division has a higher precedence than substraction and hence must be performed first."}}
Output : {{"step" : "output", "content" : "2"}}
Output : {{"step" : "validate", "content" : "Yes, 2 is the correct answer for 6/3."}}
Output : {{"step" : "think", "content" : "Next step is to add 2 to the result of previous operation."}}
Output : {{"step" : "validate", "content" : "Yes, substraction is the correct next operation to perform."}}
Output : {{"step" : "output", "content" : "0"}}
Output : {{"step" : "validate", "content" : "Yes, 0 seems to be the correct answer for 2-2."}}
and so on...... 
then at last after every calculation is done , give final result step.
Output : {{"step" : "result", "content" : "6/3 - 2 = 0  and that is calculated by performing all operations according to BODMAS rule~."}}
'''

# response = client.chat.completions.create(
#     model='gemini-1.5-flash-8b',
#     response_format= {'type' : 'json_object'},
#     messages=[
#         {'role' : 'system', 'content' : SYSTEM_PROMPT}
#     ]
# )
# print(response.choices[0].message.content)


messages = [
    {'role' : "system", 'content' : SYSTEM_PROMPT}
]

# query = input("-> ")
# messages.append({'role' : 'user', 'content' : query})
# while True:
#     response = client.chat.completions.create(
#         model = 'gemini-1.5-flash-8b',
#         response_format={'type' : 'json_object'},
#         messages=messages
#     )
    
#     messages.append({'role' : 'assistant', 'content' : response.choices[0].message.content})
#     parsed_response = json.loads(response.choices[0].message.content)
    
#     if(parsed_response.get('step') != 'result'):
#         print("    🧠 : " , parsed_response.get('content'))
#         continue
    
#     print("🤖 : ", parsed_response.get('content'))
#     break


#Multi-Modal -> give validate work to different nmodel 

query = input("-> ")
messages.append({'role' : 'user', 'content' : query})

while True: 
    response = client.chat.completions.create(
        model='gemini-1.5-flash-8b',
        response_format={'type' : 'json_object'},
        messages=messages
    )
    
    messages.append({'role' : 'assistant', 'content' : response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)
    
    if(parsed_response.get('step') == 'think'):
        #first print previous step 
        print(" Think   🧠 : " , parsed_response.get('content'))
        
        #make different model api call for validate step
        response = client.chat.completions.create(
            model='gemini-2.5-flash-lite',
            response_format={'type' : 'json_object'},
            messages= messages
        )
        
        messages.append({'role' : 'assistant', 'content' : response.choices[0].message.content})
        parsed_validate = json.loads(response.choices[0].message.content)
        if(parsed_validate.get('step') == 'validate'):
            print("Validate by 2.5-flash ✅ : ")
            continue
    
    if(parsed_response.get('step') != 'result'):
        print("    🧠 : " , parsed_response.get('content'))
        continue
    
    print("🤖 : ", parsed_response.get('content'))
    break


