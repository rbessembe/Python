import json
import base64
import gzip
import urllib3
import os

# Read all the environment variables
webhook_url = os.environ['SLACK_WEBHOOK_URL']

# Decoding data and printing needed logs 
def lambda_handler(event, context):
    decoded_event = json.loads(gzip.decompress(base64.b64decode(event['awslogs']['data'])))

    text = '''
    Log_Group: {loggroup}
    Log_stream: {logstream}
    Log_Event: {filtermatch}
    '''.format(
        loggroup=decoded_event['logGroup'],
        logstream=decoded_event['logStream'],
        filtermatch=decoded_event['logEvents'][0]['message']
    )
    
    http = urllib3.PoolManager()
    encoded_data = json.dumps({'text': text}).encode('utf-8')
    response = http.request("POST", webhook_url, body=encoded_data, headers={'Content-Type': 'application/json'})
