from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from BeaconManager.mqtt import getTagsInfo
from BeaconManager.models import Tag, Node, Layout
from .forms import LayoutForm, NodeSelectForm

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
    selectedNode = request.session.get('selected_node')
    node_obj = Node.objects.get(id=selectedNode)

    unknownTags = getTagsInfo()
    knownTags = Tag.objects.all()
    statusT = Tag.TAG_STATUS
    statusD = dict((x,y) for x,y in statusT)
    #print(statusD['p'])
    tempKnown = {}
    for t in knownTags:
        lookupID = t.tagID
        for k in unknownTags:
            if(k[0]==lookupID and k[1]==node_obj.node_id):
                tempKnown[lookupID] = [t.name,t.description,statusD[t.status],unknownTags[k][1]]
                #unknownTags.pop(k)

    return render(
        request,
        'tags_data.html',
        context={
            'title':"Tag's Data",
            'classID':'2',
            'year':datetime.now().year,
            'selectedNode':node_obj.node_id,
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
    for (tagMac,nodeMac),values in unknownTags.items():
        for t in knownTags:
            if(t.tagID == tagMac):
                tempKnown.append({"name":t.name, "mac":t.tagID, "location":values[1], "snode":nodeMac})

    json_data = {
        "tags": tempKnown
        }
    return JsonResponse(json_data, safe=False)

def viewliveLoc(request):
    """View function for Live Location page"""
    selectedLayout = request.session.get('selected_layout')
    layout_obj = Layout.objects.get(id=selectedLayout)

    allNodes = layout_obj.node_set.all()        #get all nodes associated with current layout
    reqData = {}
    for n in allNodes:
        reqData[n.node_id] = n.location
    
    #calculate scale
    scaleH = int(layout_obj.length)/640
    scaleV = int(layout_obj.width)/360
    if scaleH >= scaleV:
        scale = scaleH
    else:
        scale = scaleV

    return render(
        request,
        'live_location.html',
        context={
            'title':'Live Location of Tags',
            'classID':'3',
            'year':datetime.now().year,
            'reqData':reqData,
            'selectedLayout':layout_obj.name,
            'layoutLength':layout_obj.length,
            'layoutWidth':layout_obj.width,
            'layoutFile':layout_obj.image,
            'layoutScale':scale,
            }
        )

def viewLayoutSelector(request):
    """View function for Form selector page"""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LayoutForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['selected_layout'] = request.POST['layout_name']
            # redirect to a new URL:
            return HttpResponseRedirect('/BeaconManager/tagsLoc/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LayoutForm()

    return render(
        request,
        'layout_form.html',
        context={
            'title':'Layout Selection',
            'classID':'3',
            'year':datetime.now().year,
            'form':form,
            }
        )

def viewNodeSelector(request):
    """View function for Node selector page"""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NodeSelectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['selected_node'] = request.POST['node_name']
            # redirect to a new URL:
            return HttpResponseRedirect('/BeaconManager/tagsData/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NodeSelectForm()

    return render(
        request,
        'node_sel_form.html',
        context={
            'title':'Node Selection',
            'classID':'2',
            'year':datetime.now().year,
            'form':form,
            }
        )

