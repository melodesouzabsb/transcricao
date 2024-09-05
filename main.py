from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="A partir de uma descrição preciso que vc classifique o sentimento como negativo, neutro ou positivo.\nAtribua, também, uma pontuação de -5 a 5 onde -5 é totalmente negativo, 0 é neutro, para avaliações inconclusivas quanto à entrega, 5 é totalmente positivo\nO retorno deve ser um json\n\n#\nFormato de entrada\nid, nome, email, comentário\n#\n\n#\nFormato da saída\n{\nid:\nnome:\nemail:\nsentimento:\npontuacao:\n}\n#\n",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "classifique o comentário \"Jogo de panelas excelente material, entrega a tempo, design muito bom.\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "{\n\"sentimento\": \"positivo\",\n\"pontuacao\": 5\n} \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "classifique  \"1234,panela de pressão,teste@gmail.com,muito bom\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n\"id\": \"1234\",\n\"nome\": \"panela de pressão\",\n\"email\": \"teste@gmail.com\",\n\"sentimento\": \"positivo\",\n\"pontuacao\": 4\n}\n``` \n",
      ],
    },
  ]
)

response = chat_session.send_message("classifique '1234,panela de pressão,teste@gmail.com,muito bom'")

print(response.text)