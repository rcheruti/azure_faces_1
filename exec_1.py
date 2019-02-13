
# Usar Watson para pegar Idade e Sexo,
# e usar Azure para pegar a localização do rosto
# ----------------------------------

import requests
import base64
import json

# --- DEBUG
# import logging
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
# --- DEBUG

verifySSL = True
    

with open('./config.json') as f:
    keys = json.load(f)

# -----------
# funções para buscar as informações

def azureFacePos( imagem ):
    url = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/detect'
    chave1 = keys['faces']
    headers = {
        'Ocp-Apim-Subscription-Key': chave1 ,
        'Content-Type': 'application/json'
    }
    body = { 'url': imagem }
    params = { 
        'returnFaceLandmarks': 'false',
        'returnFaceId': 'false',
        'returnFaceAttributes': ''
    }
    print('Fazendo requisicao para Azure para buscar posicao do rosto...')
    resp = requests.post(url, json = body, headers = headers, params = params , verify=verifySSL )
    if( resp.status_code >= 200 and resp.status_code < 300 ):
        print('Resposta:')
        print( json.dumps(resp.json(), indent=4, sort_keys=True) )
    else:
        print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

def watsonData( imagem ):
    url = 'https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces'
    chave = str(base64.b64encode( ('apikey:' + keys['watson']).encode('ascii') ) ,'utf-8')
    headers = {
        'Authorization': 'Basic ' + chave,
        'Accept-Language': 'pt-br' # retornar textos em português
    }
    params = { 
        'version': '2016-05-20',
        'url': imagem
    }
    print('Fazendo requisicao para Watson para buscar idade e sexo...')
    resp = requests.get(url, headers = headers, params = params, verify=verifySSL )
    if( resp.status_code >= 200 and resp.status_code < 300 ):
        print('Resposta:')
        print( json.dumps(resp.json(), indent=4, sort_keys=True) )
    else:
        print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

# --------------
# executar buscas

imageUrl = 'https://www.somostodosum.com.br/conteudo/imagem/16476.jpg'

azureFacePos( imageUrl )
watsonData( imageUrl )
