import requests
import os
import xml.etree.ElementTree as ElementTree
import base64
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    base64text = req.params.get('base64text')
    if not base64text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            base64text = req_body.get('base64text')

    if base64text:
        str_text = base64.b64decode(base64text).decode()

        subscription_key = os.getenv("APIKEY_COGNITIVE_SERVICE")

        fetch_token_url = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)

        constructed_url = 'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1'

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3',
            #'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'.
            #'X-Microsoft-OutputFormat': 'audio-16khz-64kbitrate-mono-mp3'.
            #'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3'.
            #'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'.
            #'X-Microsoft-OutputFormat': 'audio-24khz-96kbitrate-mono-mp3'.
            #'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3'.
        }

        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'ja-JP')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'ja-JP')
        voice.set('name', 'ja-JP-NanamiNeural')
        prosody = ElementTree.SubElement(voice, 'prosody')
        prosody.set('pitch','medium') # high
        prosody.set('rate','medium') # fast
        prosody.text = str_text
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            byte_media = response.content
            base64media = base64.b64encode( byte_media).decode('utf-8')
            #with open('sample.mp3', 'wb') as audio:
            #    audio.write(response.content)
            #    print("\nStatus code: " + str(response.status_code) )

        return func.HttpResponse( base64media, status_code=200)

    else:
        return func.HttpResponse("no input", status_code=200)