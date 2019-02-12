
# Usar Watson para pegar Idade e Sexo,
# e usar Azure para pegar a localização do rosto
# ----------------------------------

import sys
import requests
import json
# from watson_developer_cloud import VisualRecognitionV3
from io import BytesIO
from PIL import Image, ImageDraw

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
        rect = resp.json()[0]

        print('Colocar retangulos na imagem...')
        response = requests.get(imagem, verify=False)
        img = Image.open(BytesIO(response.content))
        draw = ImageDraw.Draw(img)
        draw.rectangle( ( (rect['faceRectangle']['left'] , rect['faceRectangle']['top']), (rect['faceRectangle']['height'] , rect['faceRectangle']['width']) ), outline='red')
        img.show()
    else:
        print( 'Erro ao analisar imagem. StatusCode: {}, {}'.format( resp.status_code, resp.text ) )

def watsonData( imagem ):
    # sys.path.append('../')
    
    visual_recognition = VisualRecognitionV3( '2018-03-19', iam_apikey = keys['watson'] )
    classes = visual_recognition.classify(imagesFile=imagem, threshold='0.6', classifier_ids='default' ).get_result()
    # with open('../../../datasets/imagens/lions/imagem_test1.jpg', 'rb') as images_file:
    #     classes = visual_recognition.classify(
    #         images_file,
    #         threshold='0.6',
    #     classifier_ids='default').get_result()
    print(json.dumps(classes, indent=2))

# --------------
# executar buscas

#watsonData('https://www.somostodosum.com.br/conteudo/imagem/16476.jpg')
azureFacePos('https://www.somostodosum.com.br/conteudo/imagem/16476.jpg')
