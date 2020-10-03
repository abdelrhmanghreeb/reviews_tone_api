import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


API_KEY = os.environ.get('WATSON_TONE_ANALYZER_API_KEY', '')
URL = "https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/52546f18-3bab-48e7-bd37-1eb94d946ed1"
VERSION = "2017-09-21"

authenticator = IAMAuthenticator(API_KEY)

tone_analyzer = ToneAnalyzerV3(
    version = VERSION,
    authenticator=authenticator
)

tone_analyzer.set_service_url(URL)

def analyze_tone(text):
	""""""
	try:
		return(tone_analyzer.tone(
				{"text":text}, 
				content_type='application/json'
				).get_result()
			)
	except Exception as e:
		print(e)
