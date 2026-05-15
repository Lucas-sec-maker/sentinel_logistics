import os
from google import genai
from dotenv import load_dotenv
import PIL.Image

# 1. Carrega as configurações de segurança do .env
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("ERRO: A chave GOOGLE_API_KEY não foi encontrada no arquivo .env!")

# Usando o novo padrão de inicialização do cliente
client = genai.Client(api_key=api_key)

def auditor_nota_fiscal(caminho_imagem):
    try:
        imagem = PIL.Image.open(caminho_imagem)
    except FileNotFoundError:
        return f"Erro: O arquivo {caminho_imagem} não foi encontrado."

    prompt = """
    Você é um auditor fiscal automatizado do ecossistema de logística da Cayena.
    Analise rigorosamente esta imagem de Nota Fiscal, cupom ou recibo.
    
    Extraia os seguintes campos e retorne estritamente em formato JSON válido:
    {
        "cnpj_emissor": "apenas os números do CNPJ",
        "valor_total": "apenas o número decimal separado por ponto, ex: 1500.50",
        "data_emissao": "formato DD/MM/AAAA"
    }
    """

    print(f"🤖 Analisando o documento '{caminho_imagem}' com a nova API do Gemini...")
    
    # Nova chamada usando o modelo atualizado gemini-2.5-flash
    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt, imagem]
    )
    return resposta.text

if __name__ == "__main__":
    nome_arquivo_teste = "nota_teste.jpg"
    
    if os.path.exists(nome_arquivo_teste):
        resultado = auditor_nota_fiscal(nome_arquivo_teste)
        print("\n--- Dados Extraídos pela IA ---")
        print(resultado)
    else:
        print(f"\n💡 Insira uma foto de nota fiscal na pasta com o nome: '{nome_arquivo_teste}'")