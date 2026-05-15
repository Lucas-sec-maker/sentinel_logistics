import os 
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

# ==========================================
# 1. CONFIGURAÇÃO DE SEGURANÇA E AMBIENTE
# ==========================================
# Carrega as variáveis do arquivo .env
load_dotenv()


#Recupera a chave de API  e configura o Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("ERRO: A chave GOOGLE_API_KEY não foi encontrada no arquivo .env!")
genai.configure(api_key=api_key)

# Usamos o Gemini 1.5 Flash: ultra rápido e multimodal (lê imagens)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 2. INTELIGÊNCIA ARTIFICIAL (AUDITORIA)
# ==========================================

def auditor_nota_fiscal(caminho_imagem):
    """
    Recebe a imagem de uma NF/Recibo e utiliza IA para extrair dados
    estruturados prontos para validação sistêmica.
    """
    try:
        # Carrega a imagem usando a biblioteca PIL
        imagem = PIL.Image.open(caminho_imagem)
    except FileNotFoundError:
        return f"Erro: O arquivo {caminho_imagem} não foi encontrado."

    # Prompt estruturado para forçar a IA a responder em JSON puro.
    # Isso é crítico para que o Python consiga ler os dados depois!
    prompt = """
    Você é um auditor fiscal automatizado do ecossistema de logística da Cayena.
    Analise rigorosamente esta imagem de Nota Fiscal, cupom ou recibo.
    
    Extraia os seguintes campos e retorne estritamente em formato JSON válido, 
    sem formatações adicionais, sem blocos de código markdown (como ```json):
    {
        "cnpj_emissor": "apenas os números do CNPJ",
        "valor_total": "apenas o número decimal separado por ponto, ex: 1500.50",
        "data_emissao": "formato DD/MM/AAAA"
    }
    """

    print(f"🤖 Analisando o documento '{caminho_imagem}' com Gemini Vision...")
    
    # Passamos o prompt de texto e a imagem juntos para o modelo
    resposta = model.generate_content([prompt, imagem])
    return resposta.text

# ==========================================
# 3. PONTO DE EXECUÇÃO (TESTE LOCAL)
# ==========================================
if __name__ == "__main__":
    # TODO: Nas próximas sprints, mudaremos isso para uma tela web com Streamlit
    # Para testar hoje, basta colocar uma imagem chamada 'nota_teste.jpg' na mesma pasta
    nome_arquivo_teste = "nota_teste.jpg"
    
    if os.path.exists(nome_arquivo_teste):
        resultado = auditor_nota_fiscal(nome_arquivo_teste)
        print("\n--- Dados Extraídos pela IA ---")
        print(resultado)
    else:
        print(f"\n💡 Ambiente pronto! Para ver a IA funcionando, coloque uma foto de nota fiscal nesta pasta com o nome: '{nome_arquivo_teste}'")
