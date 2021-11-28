import logging
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        my_app_setting_value = os.getenv("custom_secret_string")
        logging.info(f'My app setting value:{my_app_setting_value}')
        return func.HttpResponse(
             "azf-p38 functions.",
             status_code=200
        )
