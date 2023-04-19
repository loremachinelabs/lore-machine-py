import numpy as np
import io
from constants import * 
import pandas as pd 
import openai 

openai.api_key = OPENAI_KEY

def build_prompt(columns):
    text = BUILD_TABLE_QUERY
    text = text + COLUMN_QUERY
    for c in columns[:-1]:
        text = text + "'" + str(c) + "' ," 
    text = text + "'"+ columns[-1] + "'."
    text = text + CLOSING_LINE
    return text + '\n\n'

def final_prompt(text,columns=BASELINE_COLUMNS):
    start = build_prompt(columns)
    return start,text 

def text_to_table(text,columns=BASELINE_COLUMNS):
    queries = final_prompt(text,columns)
    full_text = openai.ChatCompletion.create(model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": queries[0]},
            {"role": "user", "content": queries[1]},
        ])
    res_text = full_text['choices'][0]['message']['content']
    with open('res_text.txt', 'w') as f:
        f.write(res_text)
    data = pd.read_csv('res_text.txt',error_bad_lines=False)
    data.to_csv('table_to_text.csv')
    return data


print(openai.api_key)
text = open('example.txt').read()
data = pd.read_csv('res_text.txt',error_bad_lines=False)
print(data)
data.to_csv('table_to_text.csv')

