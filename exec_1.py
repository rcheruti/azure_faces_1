
# Usar Watson para pegar Idade e Sexo,
# e usar Azure para pegar a localização do rosto
# ----------------------------------
    
import requests
import json

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
    resp = requests.request('post', url, json = body, headers = headers, params = params )
    if( resp.status_code >= 200 and resp.status_code < 300 ):
        print('Resposta:')
        print( json.dumps(resp.json(), indent=4, sort_keys=True) )
    else:
        print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

def watsonData( imagem ):
    url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/detect_faces'
    headers = {
        'Content-Type': 'application/json'
    }
    body = { 'url': imagem }
    params = { 
        'api_key':  keys['watson'],
        'version': '2016-05-20'
    }
    print('Fazendo requisicao para Watson para buscar idade e sexo...')
    resp = requests.request('post', url, json = body, headers = headers, params = params, verify=False )
    if( resp.status_code >= 200 and resp.status_code < 300 ):
        print('Resposta:')
        print( json.dumps(resp.json(), indent=4, sort_keys=True) )
    else:
        print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

# --------------
# executar buscas

azureFacePos('https://www.somostodosum.com.br/conteudo/imagem/16476.jpg')
# watsonData('https://www.somostodosum.com.br/conteudo/imagem/16476.jpg')
