import logging
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import azure.functions as func
from base64 import b64decode


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    subscription_key = os.getenv("APIKEY_FACEAPI_SERVICE")
    uri_base = 'p2-cgnsrv-face.cognitiveservices.azure.com'

    params = urllib.parse.urlencode({
        'returnFaceAttributes': 'smile,age,emotion',
    })

    type = req.params.get('type')
    if type=="wake":
        parsed = {
                 "success": True,
                 "reason": "wake functions",
        }
        return func.HttpResponse(json.dumps(parsed, sort_keys=True, indent=2))

    elif type=="url":
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        #body = "{'url': 'https://data.be-story.jp/mwimgs/c/6/500/img_c6be26183c95e4cec265df522c42a5f4758231.jpg'}"

        url = req.params.get('url')

        if not url:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                url = req_body.get('url')

        if not url:
            parsed = {
                     "success": False,
                     "reason": "Select type=url but url param is empty.",
            }
            return func.HttpResponse(json.dumps(parsed, sort_keys=True, indent=2),status_code=400)

        body = "{'url': '" + url + "'}"

    elif type=="image":
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

        image = req.params.get('image')
        if not image:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                image = req_body.get('image')

        if not image:
            parsed = {
                     "success": False,
                     "reason": "Select type=image but image param is empty.",
            }
            return func.HttpResponse(json.dumps(parsed, sort_keys=True, indent=2),status_code=400)
        
        image_base64 = image.split(",")[1]
        image_data = b64decode(image_base64)
        body = image_data

    else:
        parsed = {
                 "success": False,
                 "reason": "BAD REQUEST",
        }
        return func.HttpResponse(json.dumps(parsed, sort_keys=True, indent=2),status_code=400)

    conn = http.client.HTTPSConnection(uri_base)
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    conn.close()

    return func.HttpResponse(json.dumps(parsed, sort_keys=True, indent=2))