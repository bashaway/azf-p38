import logging
import urllib.request
import base64
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = req.params.get('url')
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url = req_body.get('url')

    if url:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()

        base64media = base64.b64encode(body).decode('utf-8')
        #return func.HttpResponse( base64media, status_code=200)

        dict_return = {
            "image": base64media,
        }

        return func.HttpResponse(json.dumps(dict_return, sort_keys=True, indent=2) , mimetype="application/json" )


    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
