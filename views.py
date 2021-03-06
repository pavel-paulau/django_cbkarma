from django.shortcuts import render_to_response
from django.template import RequestContext

from couchbase.client import CbClient
from couchbase.histo import LatencyDict

def home(request):
    client = CbClient()

    # Output data dictionary
    data = list()

    for row in client.query(ddoc='karma', view='uid')['rows']:
        latest_timestamp = max(row['value']['events'].keys())

        status = row['value']['events'][latest_timestamp]['phase'] + ': ' + \
                 row['value']['events'][latest_timestamp]['status']

        data.append({'test_id': row['id'],
                     'build': row['value'].get('build', ''),
                     'spec': row['value'].get('spec', ''),
                     'ini': row['value'].get('ini', ''),
                     'status': status,
                     'timestamp': latest_timestamp
        })

    # Response context
    context = {'title': 'Dashboard', 'data': data}

    return render_to_response('home.html', context)

def details(request):
    client = CbClient()

    # Phases
    test_id = request.GET['id']
    test_details = client.find(test_id)

    events = test_details.get('events', {})

    phases = list()
    for event in sorted(events):
        phases.append("{0} phase {1} at {2}".format(events[event]['phase'],
                                                    events[event]['status'],
                                                    event))

    histograms = test_details.get('histograms', {})
    histograms = dict((d, LatencyDict(a)) for d, a in histograms.iteritems())

    reports = test_details.get('reports', {})

    context = RequestContext(request, {'phases': phases,
                                       'histograms': histograms,
                                       'reports': reports,
                                       'build': test_details.get('build'),
                                       'spec': test_details.get('spec'),
                                       'ini': test_details.get('ini'),
                                       'test_id': test_id,
                                       'title': 'Test Details'})

    return render_to_response('details.html', context)
