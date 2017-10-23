'''
Created on Oct 20, 2017

@author: jagavkar
'''

import boto3
from os import environ
import json
from pygame import mixer
import time
import subprocess
import sys



def get_rekognition_client():
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    return rekognition


def capturePicture():
    print("Capturing picture...")
    subprocess.call (["fswebcam","-r", "640x480", "image.jpg"])
    #subprocess.call(["imagesnap","-w","1", "image.jpg"])
        
            
def makePollySayIt(foundItem, foundConfidence):
    print ("Speaking...")
    speak = "Found "+foundItem+"!, I am about "+ foundConfidence+" percent sure."
    
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=speak,
        TextType= 'text',
        VoiceId='Raveena'
    )
    sound = response.get('AudioStream')
    mixer.init()
    #mixer.music.load('/home/pi/audio.mp3')
    mixer.music.load(sound)
    mixer.music.play()
    time.sleep(5)
    print("played") 
    
    
    
if __name__ == '__main__':
    print("Identifier started....")
    client = get_rekognition_client()
    
    while(True):
        capturePicture()
        try:
            with open("image.jpg", 'rb') as image:
                image_bytes = image.read()
                    
                print ("Detecting objects ...")
                response = client.detect_labels(Image={'Bytes': image_bytes},MaxLabels=1)
                print ('response')
                foundItem = json.dumps(response["Labels"][0]["Name"])
                foundConfidence = json.dumps(response["Labels"][0]["Confidence"])
                
                print ("Found {0}, I am about {1} percent sure.".format(foundItem, foundConfidence))
                
                makePollySayIt(foundItem, foundConfidence)

        except:
            print("Object detection error:", sys.exc_info())
            pass
        time.sleep(5)
