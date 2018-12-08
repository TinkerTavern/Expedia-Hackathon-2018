from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Reviews.models import Review
from django.core import serializers
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import time
import ffmpy
import json
import time
import os
import os.path
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def addReviewPage(request):
    context = {}
    return render(request, 'Reviews/addReview.html', context)

def displayReviews(request):
    context = {}
    return render(request, 'Reviews/getReview.html', context)

def getReviews(request, l):
    found = False
    wordsInSearch = l.split(" ")
    if request.is_ajax():
        results = Review.objects.filter(location=l).order_by('-upvotes','-datePosted')
        if len(results) == 0:
            for word in wordsInSearch:
                results = Review.objects.filter(location=l).order_by('-upvotes','-datePosted')
                if len(results) > 0:
                    found = True
                    break
        else:
            found = True
        if found:
            data = serializers.serialize("json", results)
        else:
            data = serializers.serialize("json", {"return":"No Data"})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@csrf_exempt
def incrementUpvotes(request):
    if request.is_ajax() and request.method == 'POST':
        r = Review.objects.get(pk=request.POST['id'])
        r.upvotes = r.upvotes+1
        r.save()
        return HttpResponse("success")

@csrf_exempt
def submitReview(request):
    if request.is_ajax() and request.method == 'POST':
        r = Review(author=request.POST['author'],location=request.POST['location'],reviewText=request.POST['review'])#,datePosted=datetime.date.today())
        r.save()
        return HttpResponse("success")
    else:
        raise Http404

def getAudio(request):
        if os.path.isfile("test.wav"): # Deletes the old files first if there
            os.remove("test.wav")
        if os.path.isfile("test.flac"):
            os.remove("test.flac")
        duration = 5 # Seconds
        fs = 48000 # Frequency
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait() # Waits for the recording to end before moving on
        r = sr.Recognizer()
        scipy.io.wavfile.write("test.wav", 48000, recording)
        ff = ffmpy.FFmpeg(inputs={'test.wav': None},outputs={'test.flac': None})
        ff.run()
        harvard = sr.AudioFile("test.flac")
        with harvard as source:
            audio = r.record(source)
        spokenWords = r.recognize_google(audio).lower()
        dict = {'message':spokenWords}
        jsonFile = json.dumps(dict) # Converts string to json
        return HttpResponse(jsonFile, content_type='application/json')
