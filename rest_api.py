import time
import json
from uuid import uuid4

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from couchbase.client import CbClient

@require_GET
def init(request):
    return HttpResponse(uuid4().hex)

@csrf_exempt
@require_POST
def update(request):
    client = CbClient()

    test_id = request.POST.get('id', uuid4().hex)

    build = request.POST.get('build', '')
    spec = request.POST.get('spec', '')
    description = request.POST.get('description', '')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    phase = request.POST.get('phase', '')
    status = request.POST.get('status', '')

    events = client.find(test_id).get('events', {})
    events.update({timestamp: {'phase': phase, 'status': status}})

    doc = {'build': build,
           'spec': spec,
           'description': description,
           'events': events,
           'type': 'update'}

    client.update(test_id, doc)

    return HttpResponse(test_id)

@csrf_exempt
@require_POST
def histo(request):
    client = CbClient()

    test_id = request.POST.get('id', uuid4().hex)
    description = request.POST.get('description', uuid4().hex)
    attachment = request.POST.get('attachment', '')
    attachment = json.loads(str(attachment))

    histograms = client.find(test_id).get('histograms', {})
    histograms.update({description: attachment})

    doc = {'histograms': histograms}

    client.update(test_id, doc)

    return HttpResponse(test_id)

@csrf_exempt
@require_POST
def report(request):
    client = CbClient()

    print request.POST
    test_id = request.POST.get('test_id', uuid4().hex)
    description = request.POST.get('description', uuid4().hex)
    url = request.POST.get('url', '')

    print client.find(test_id)

    reports = client.find(test_id).get('reports', {})
    reports.update({description: url})

    doc = {'reports': reports}
    print doc

    client.update(test_id, doc)

    if request.POST.get('submit'):
        location = '/details?id={0}'.format(test_id)
        return redirect(location)
    else:
        return HttpResponse(test_id)
