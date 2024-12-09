import os
import glob
import dotenv
import requests


# Variáveis globais
TOKEN = None
ID_PDV = None
FILE_ANALYZE_ID = None

def listar_arquivos(diretorio, extensao):
    padrao = os.path.join(diretorio, f'**/*.{extensao}')
    arquivos = glob.glob(padrao, recursive=True)
    return arquivos

def gerar_token():
    global ID_PDV, TOKEN

    dotenv.load_dotenv()

    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ID_PDV = os.getenv('ID_PDV')

    if not ACCESS_KEY or not SECRET_KEY or not ID_PDV:
        return "-1"  

    url = "https://xml.embed.it/v1/validateLogin"
    headers = {"Content-Type": "application/json"}
    payload = {"accessKey": ACCESS_KEY, "secretKey": SECRET_KEY}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        TOKEN = data.get("token")
        return "0" 
    except requests.exceptions.RequestException as e:
        return "-1"  
    except ValueError as e:
        return "-1" 

def zip(path_zip):
    global FILE_ANALYZE_ID

    if not os.path.exists(path_zip):
        return "-1"

    url = "https://xml.embed.it/v1/doc/zip"
    headers = {"Authorization": TOKEN}

    try:
        with open(path_zip, 'rb') as file:
            files = {
                'file': file,
                'softwareHousePdvId': (None, ID_PDV),
            }
            response = requests.post(url, headers=headers, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            FILE_ANALYZE_ID = data.get("fileAnalyzeId")

            if status == "DONE":
                return "0"
            elif status in ["INITIAL", "PROCESSING"]:
                return "1"
            else:
                return "-1"
    except requests.exceptions.RequestException as e:
        return "-1"
    except ValueError as e:
        return "-1"


def rar(path_rar):
    global FILE_ANALYZE_ID

    if not os.path.exists(path_rar):
        return "-1"

    url = "https://xml.embed.it/v1/doc/rar"
    headers = {"Authorization": TOKEN}

    try:
        with open(path_rar, 'rb') as file:
            files = {
                'file': file,
                'softwareHousePdvId': (None, ID_PDV),
            }
            response = requests.post(url, headers=headers, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            FILE_ANALYZE_ID = data.get("fileAnalyzeId")

            if status == "DONE":
                return "0"
            elif status in ["INITIAL", "PROCESSING"]:
                return "1"
            else:
                return "-1"
    except requests.exceptions.RequestException as e:
        return "-1"
    except ValueError as e:
        return "-1"


def path(path_file):
    global FILE_ANALYZE_ID

    if not os.path.exists(path_file):
        return "-1"

    url = "https://xml.embed.it/v1/doc/file"
    headers = {"Authorization": TOKEN}

    try:
        with open(path_file, 'rb') as file:
            files = {
                'file': file,
                'softwareHousePdvId': (None, ID_PDV),
            }
            response = requests.post(url, headers=headers, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            FILE_ANALYZE_ID = data.get("fileAnalyzeId")

            if status == "DONE":
                return "0"
            elif status in ["INITIAL", "PROCESSING"]:
                return "1"
            else:
                return "-1"
    except requests.exceptions.RequestException as e:
        return "-1"
    except ValueError as e:
        return "-1"

def xml(content):
    global FILE_ANALYZE_ID

    url = "https://xml.embed.it/v1/doc/xml"
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "content": content,
        "softwareHousePdvId": ID_PDV
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        FILE_ANALYZE_ID = data.get("fileAnalyzeId")

        if status == "DONE":
            return "0" 
        elif status in ["INITIAL"]:
            return "INITIAL = 1"
        else:
            return "-1"  
    except requests.exceptions.RequestException as e:
        return "-1"  
    except ValueError as e:
        return "-1"  

# Função que obtém o status
def status():
    if not FILE_ANALYZE_ID:
        return "-1"

    url = f"https://xml.embed.it/v1/doc/file/{FILE_ANALYZE_ID}"
    headers = {"Authorization": TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")

        if status == "DONE":
            return "1"
        elif status == "INITIAL":
            return "0"
        elif status == "ERROR":
            return "-1"
        else:
            return "-1"
    except requests.exceptions.RequestException as e:
        return "-1"
    except ValueError as e:
        return "-1"
