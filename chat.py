import os
import openai
api_key='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'
openai.api_key = api_key

prompt = 'criar user schema com nome, endereço, idade e email fastapi'

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.7,
  max_tokens=300,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)["choices"][0]["text"].strip(" \n")


print(response)