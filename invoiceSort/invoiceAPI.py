import openai 
  
openai.my_api_key = 'YOUR_API_KEY'


# Step 6: Set a context for the ChatGPT API that is used to tell the 
# API what is it supposed to do using the JSON file. In this, we have 
# defined the role as a system because we are creating this for users and this 
# ChatGPT is a system and also defined the content.

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]


while True: 
    message = input("User : ") 
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
    reply = chat.choices[0].message.content 
    print(f"ChatGPT: {reply}") 
    messages.append({"role": "assistant", "content": reply}) 