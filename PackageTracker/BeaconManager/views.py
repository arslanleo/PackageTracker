from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from BeaconManager.mqtt import getTagsInfo
from BeaconManager.models import Tag

# Create your views here.

def index(request):     #its a function based view
    """View function for homepage of website"""
    temp1 = 25

    return render(
        request,
        'index.html',
        context={
            'title':'Home',
            'classID':'1',
            'year':datetime.now().year,
            }
        )

def viewTagsData(request):     #its a function based view
    """View function for homepage of website"""
    unknownTags = getTagsInfo()
    knownTags = Tag.objects.all()
    statusT = Tag.TAG_STATUS
    statusD = dict((x,y) for x,y in statusT)
    print(statusD['p'])
    tempKnown = {}
    for t in knownTags:
        if(t.tagID in unknownTags):
            tempKnown[t.tagID] = [t.name,t.description,statusD[t.status],unknownTags[t.tagID][1]]
            unknownTags.pop(t.tagID)

    return render(
        request,
        'tags_data.html',
        context={
            'title':"Tag's Data",
            'classID':'2',
            'year':datetime.now().year,
            'tagsU':unknownTags,
            'tagsK':tempKnown,
            }
        )

def about(request):
    """View function for About page"""

    return render(
        request,
        'about.html',
        context={
            'title':'About',
            'classID':'4',
            'year':datetime.now().year,
            }
        )

def getLocData(request):
    unknownTags = getTagsInfo()
    knownTags = Tag.objects.all()
    tempKnown = []
    for t in knownTags:
        if(t.tagID in unknownTags):
            tempKnown.append({"name":t.name,"location":unknownTags[t.tagID][1]})
            unknownTags.pop(t.tagID)

    json_data = {
        "tags": tempKnown,
        "nodes" : tempKnown
        }
    return JsonResponse(json_data, safe=False)

def viewliveLoc(request):
    """View function for Live Location page"""

    return render(
        request,
        'live_location.html',
        context={
            'title':'Live Location of Tags',
            'classID':'3',
            'year':datetime.now().year,
            }
        )

