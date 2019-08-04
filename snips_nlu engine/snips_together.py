import azure.cognitiveservices.speech as speechsdk
import json
import random
import os
import string
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "UNKY", "UNKY"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

print("Initialising Snips Engine...")

from snips_nlu import SnipsNLUEngine # requires version 0.19.0
from snips_nlu.default_configs import CONFIG_EN
engine = SnipsNLUEngine.from_path("engine.eng")
#engine = SnipsNLUEngine(config = CONFIG_EN,random_state = 42)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")


region_synonyms = [{"value": "SEA","synonyms": ["South East Asia","South Asia", "SE Asia", "SE", "Asia"]},{"value": "NA","synonyms": ["North America","America"]},{"value": "CHINA","synonyms": []},{"value": "ASIA","synonyms": []},{"value": "EUR","synonyms": ["Europe"]}]


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
while True:
    result = speech_recognizer.recognize_once()
    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    print("Snips Output:")
    output = engine.parse(result.text)
    pprint(output)
    item = output['slots']
    if output["intent"]["intentName"]!="Ask":
        continue
    sendable_dict={}
    for dictionary in item:
        pprint(dictionary)
        if dictionary["slotName"]=="Product Number":
            prd_number = dictionary["value"]["value"]
            testitem = prd_number.strip()
            testitem = testitem.replace(' ',"")
            testitem = testitem.replace(".","")
            sendable_dict["Product Number"] = testitem
        elif dictionary["slotName"]=="Company":
            prd_number = dictionary["value"]["value"]
            testitem = prd_number.strip()
            testitem = testitem.replace(' ',"")
            testitem = testitem.replace(".","")
            sendable_dict["company"] = testitem
        elif dictionary["slotName"]=="Region":
            prd_number = dictionary["value"]["value"]
            testitem = prd_number.strip()
            testitem = testitem.replace(' ',"")
            testitem = testitem.replace(".","")
            for i in region_synonyms:
                if testitem in i["synonyms"]:
                    testitem = i["value"]
            sendable_dict["region"] = testitem
            
            
    if len(list(sendable_dict.keys()))>0:
        try:
            driver = webdriver.Firefox()
            driver.get("http://127.0.0.1:8000/search/")
            if ("Product Number" in sendable_dict.keys()):
                elem = driver.find_element_by_name('product')
                elem.send_keys(sendable_dict["Product Number"])
            if ("region" in sendable_dict.keys()):
                elem = driver.find_element_by_name('region')
                elem.send_keys(sendable_dict["region"])
            if ("company" in sendable_dict.keys()):
                elem = driver.find_element_by_name('company')
                elem.send_keys(sendable_dict["company"])
            button = driver.find_element_by_id('submitbutton')
            button.click()
        except WebDriverException as ex:
            print(ex)
            print("Webdriver Exception")
            driver.close()
        except NoSuchElementException as ex:
            print(ex)
            print("No such Element Exception")
            driver.close()
                
                
        
    input("Press Enter to continue")
    
    
    
    
