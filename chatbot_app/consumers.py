import json, asyncio, pandas as pd, numpy as np, openai, environ
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


async def generate_response(message_list):
    response = await asyncio.to_thread(openai.ChatCompletion.create,
        model= "gpt-3.5-turbo",
        messages = message_list,
        # [
        #     {"role": "system", "content": "You are a helpful business advisor."},
        #     {"role": "user", "content": prompt},
        # ],
        max_tokens=150,  # Adjust this value based on your desired response length
        n=1,
        stop=None,
        temperature=0.7,  # Adjust this value to control randomness (higher values make output more random)
        stream = True
    )
    return response

df = pd.read_excel('sample_people.xlsx')

async def get_message_list(olympiad = False, i=0):
    message_list_no_olympiad =  [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "assistant", "content":"What is your employment status?"},
                    {"role": "user", "content":"not available" if pd.isnull(df.iloc[i]['3_activity']) else "I am " + df.iloc[i]['3_activity']},
                    # f"I am {"not available" if pd.isnull(df.iloc[i]['3_activity']) else df.iloc[i]['3_activity']}"
                    {"role": "assistant", "content":"What is your bachelor level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['6_DIM_points']) else str(round(df.iloc[i]['6_DIM_points']))},
                    {"role": "assistant", "content":"How is your system of bachelor level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 700 is highest and best. Higher, better."},
                    {"role": "assistant", "content":"What is your master's level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['7_Master_points']) else str(round(df.iloc[i]['7_Master_points']))},
                    
                    {"role": "assistant", "content":"How is your system of master's level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

                    {"role": "assistant", "content":"What is your PhD level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['8_PhD_points']) else str(round(df.iloc[i]['8_PhD_points']))},

                    {"role": "assistant", "content":"How is your system of PhD level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."}#,
                    #{"role": "user", "content": prompt},
                ]


    message_list_olympiad =  [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "assistant", "content":"What is your employment status?"},
                    {"role": "user", "content":"not available" if pd.isnull(df.iloc[i]['3_activity']) else "I am " + df.iloc[i]['3_activity']},
                    {"role": "assistant", "content":"What is your bachelor level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['6_DIM_points']) else str(round(df.iloc[i]['6_DIM_points']))},
                    {"role": "assistant", "content":"How is your system of bachelor level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 700 is highest and best. Higher, better."},
                    {"role": "assistant", "content":"What is your master's level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['7_Master_points']) else str(round(df.iloc[i]['7_Master_points']))},
                    
                    {"role": "assistant", "content":"How is your system of master's level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

                    {"role": "assistant", "content":"What is your PhD level entrance exam point?"},
                    {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['8_PhD_points']) else str(round(df.iloc[i]['8_PhD_points']))},

                    {"role": "assistant", "content":"How is your system of PhD level entrance exam graded?"},
                    {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

                    {"role": "assistant", "content":"Give me detailed information about your success in olympiad."},
                    {"role": "user", "content":f"""I have participated in {df.iloc[i]['10_olimpiad_subject']} 
                                                     olimpiads in {df.iloc[i]['11_olimpiad_level']} level and got the rank of 
                                                     {df.iloc[i]['12_rank_in_olimpiad']}"""}#,

                ]
    return message_list_olympiad if olympiad else message_list_no_olympiad


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        
        message = json.loads(text_data)
        openai.api_key = settings.OPEN_API_KEY
        i = 1
        messages_ = await get_message_list(olympiad = True if df.iloc[i]['9_olimpiad_winner'] == 'yes' else False, i = i)
        prompt = "Hello how are you"
        if prompt:
            messages_ += [{"role": "user", "content": prompt}]
            new_response = await generate_response(message_list = messages_)

        async def data_stream():

            for msg in new_response:
                if msg['choices'][0]['delta'].get('content') != None:
                    print(msg['choices'][0]['delta'].get('content').encode())
                    await asyncio.sleep(0.1)
                    
                    yield json.dumps({'message': msg['choices'][0]['delta'].get('content')}) 

        # Send the stream of data to the client
        async for message in data_stream():
            await self.send(text_data=message)