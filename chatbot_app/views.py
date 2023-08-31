import pandas as pd, numpy as np, openai, environ
from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe
# Create your views here.
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse
import json
from rest_framework.response import Response
from django.views.generic import TemplateView



def generate_response(message_list):
    response = openai.ChatCompletion.create(
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

def get_message_list(olympiad = False, i=0):
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
@api_view(['POST'])
def chatbot(request):
    openai.api_key = settings.OPEN_API_KEY
    i = request.data.get("id")    
    messages_ = get_message_list(olympiad = True if df.iloc[i]['9_olimpiad_winner'] == 'yes' else False, i = i)
    prompt = request.data.get("msg")
    if prompt:
        messages_ += [{"role": "user", "content": prompt}]
        new_response = generate_response(message_list = messages_)

        def stream():
            for msg in new_response:
                if msg['choices'][0]['delta'].get('content') != None:
                    yield msg['choices'][0]['delta'].get('content').encode()

        messages_ += [{"role": "assistant", 'content': new_response}]

        response = StreamingHttpResponse(stream(), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="my_data.json"'

        return response
    
def index(request):
      return render(request, 'home.html')

def room(request, room_name):
    """"""
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def chat(request):
    return render(request, 'chat.html')



# def generate_response(message_list):
#         response = openai.ChatCompletion.create(
#             model= "gpt-3.5-turbo",
#             messages = message_list,

#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         return response.choices[0].message['content']
# df = pd.read_excel('sample_people.xlsx')

# def get_message_list(olympiad = False, i=0):
#         message_list_no_olympiad =  [
#                         {"role": "system", "content": "You are a helpful AI assistant."},
#                         {"role": "assistant", "content":"What is your employability status?"},
#                         {"role": "user", "content":"not available" if pd.isnull(df.iloc[i]['3_activity']) else "I am " + df.iloc[i]['3_activity']},
#                         # f"I am {"not available" if pd.isnull(df.iloc[i]['3_activity']) else df.iloc[i]['3_activity']}"
#                         {"role": "assistant", "content":"What is your bachelor level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['6_DIM_points']) else str(round(df.iloc[i]['6_DIM_points']))},
#                         {"role": "assistant", "content":"How is your system of bachelor level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 700 is highest and best. Higher, better."},
#                         {"role": "assistant", "content":"What is your master's level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['7_Master_points']) else str(round(df.iloc[i]['7_Master_points']))},

#                         {"role": "assistant", "content":"How is your system of master's level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

#                         {"role": "assistant", "content":"What is your PhD level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['8_PhD_points']) else str(round(df.iloc[i]['8_PhD_points']))},

#                         {"role": "assistant", "content":"How is your system of PhD level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."}#,
#                         #{"role": "user", "content": prompt},
#                     ]


#         message_list_olympiad =  [
#                         {"role": "system", "content": "You are a helpful AI assistant."},
#                         {"role": "assistant", "content":"What is your employability status?"},
#                         {"role": "user", "content":"not available" if pd.isnull(df.iloc[i]['3_activity']) else "I am " + df.iloc[i]['3_activity']},
#                         {"role": "assistant", "content":"What is your bachelor level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['6_DIM_points']) else str(round(df.iloc[i]['6_DIM_points']))},
#                         {"role": "assistant", "content":"How is your system of bachelor level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 700 is highest and best. Higher, better."},
#                         {"role": "assistant", "content":"What is your master's level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['7_Master_points']) else str(round(df.iloc[i]['7_Master_points']))},

#                         {"role": "assistant", "content":"How is your system of master's level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

#                         {"role": "assistant", "content":"What is your PhD level entrance exam point?"},
#                         {"role": "user", "content": "not available" if pd.isnull(df.iloc[i]['8_PhD_points']) else str(round(df.iloc[i]['8_PhD_points']))},

#                         {"role": "assistant", "content":"How is your system of PhD level entrance exam graded?"},
#                         {"role": "user", "content":"0 is lowest and worst, 100 is highest and best. Higher, better."},

#                         {"role": "assistant", "content":"Give me detailed information about your success in olympiad."},
#                         {"role": "user", "content":f"""I have participated in {df.iloc[i]['10_olimpiad_subject']} 
#                                                          olimpiads in {df.iloc[i]['11_olimpiad_level']} level and got the rank of 
#                                                          {df.iloc[i]['12_rank_in_olimpiad']}"""}#,


#                     ]
#         return message_list_olympiad if olympiad else message_list_no_olympiad
# @api_view(['POST'])
# def chatbot(request):
#     openai.api_key = settings.OPEN_API_KEY
#     i = request.data.get("id")    
#     messages_ = get_message_list(olympiad = True if df.iloc[i]['9_olimpiad_winner'] == 'yes' else False, i = i)
#     prompt = request.data.get("msg")
#     if prompt:
#          messages_ += [{"role": "user", "content": prompt}]
#          new_response = generate_response(message_list = messages_)
#          print(new_response)
#          messages_ += [{"role": "assistant", 'content': new_response}]

#     return Response({"message":new_response})

# def index(request):
#       return render(request, 'home.html')

# def room(request, room_name):
#     """"""
#     return render(request, 'room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })



