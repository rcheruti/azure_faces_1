
import requests
import json

with open('./config.json') as f:
    keys = json.load(f)

url = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/persongroups'
chave1 = keys['faces']
groupID = 'Grupo1'

headers = {
    'Ocp-Apim-Subscription-Key': chave1 ,
    'Content-Type': 'application/json'
}
# Pessoa que serão adicionadas no grupo, uma URL por linha no vetor
faces = [
    {
        'personID': 'SteveJobs',
        'url': 'https://i2.wp.com/artesanatocomonegocio.com.br/wp-content/uploads/2017/10/STEVE_JOBS_100711_W_APPLE_LOGO-512x384-e1507322916376.jpg?fit=512%2C384&ssl=1'
    }
]

# ---------------------

print('Criando o grupo de "Pessoas"...')
body = { 'name': 'Grupo 1', 'userData': 'Informações adicionais para o grupo' }
resp = requests.request('put', url + '/' + groupID, json = body, headers = headers )

if( resp.status_code >= 200 and resp.status_code < 300 ):
    print('Grupo "{}" criado (nesta requisicao). Adicionando pessoas...'.format(groupID))
    for pessoa in faces:
        body = { 'url': pessoa['url'] }
        resp2 = requests.request('post', url + '/' + groupID + '/person/' + pessoa['personID'] +'/persistedFaces', 
                            json = body, headers = headers )
        # @TODO continuar aqui!!!
elif( resp.status_code == 409 ):
    print('Grupo "{}" já existia.'.format(groupID))
else:
    print('Um erro aconteceu! StatusCode: {}, {}'.format( resp.status_code, resp.text ))
    print('Terminando')
    exit(1)

# ---------------------


