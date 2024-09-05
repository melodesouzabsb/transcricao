import os

import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "temperature": 0,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)

reviews = pd.read_csv('reviews-entrega-MercadoAgil-imagens.csv')

#print (reviews)
#exit (0)


for index, review in reviews.iterrows():
  reviewer_id = review['reviewer_id']
  reviewer_email = review['reviewer_email']
  review_imagem = review['review_image']
  print(f'Processando a imagem do review {reviewer_id} de {reviewer_email}...')
  #exit(0)
  arquivo_imagem = genai.upload_file(path=f'image/{review_imagem}')
  prompt = 'Transcreva detalhadamente o arquivo de imagem em anexo.'
  response = model.generate_content([prompt, arquivo_imagem])
  with open(f"transcricoes-imagem/{reviewer_id}.txt", "w", encoding="utf-8") as arquivo:
    print(f'Salvando transcrição da imagem do review {reviewer_id} de {reviewer_email}...')
    arquivo.write(response.text)
    