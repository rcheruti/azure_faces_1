
import requests
import json

with open('./config.json') as f:
    keys = json.load(f)

url = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/detect'
chave1 = keys['faces']

headers = {
    'Ocp-Apim-Subscription-Key': chave1 ,
    'Content-Type': 'application/json'
}
body = { 'url': 'https://www.somostodosum.com.br/conteudo/imagem/16476.jpg' }
params = { 
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,smile'
}

# ---------------------

print('Fazendo requisicao da analise...')
resp = requests.request('post', url, json = body, headers = headers, params = params )

if( resp.status_code >= 200 and resp.status_code < 300 ):
    print( json.dumps(resp.json(), indent=4, sort_keys=True) )
else:
    print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

