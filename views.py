from django.shortcuts import render_to_response

from couchbase.client import CbClient

def home(request):
    client = CbClient()

    # Output data dictionary
    data = list()

    for row in client.query(ddoc='karma', view='uid')['rows']:
        latest_timestamp = max(row['value']['events'].keys())

        status = row['value']['events'][latest_timestamp]['phase'] + ': ' + \
                 row['value']['events'][latest_timestamp]['status']

        data.append({'test_id': row['id'],
                     'build': row['value']['build'],
                     'spec': row['value']['spec'],
                     'description': row['value']['description'],
                     'status': status,
                     'timestamp': latest_timestamp
        })

    # Response context
    context = {'title': 'Dashboard', 'data': data}

    return render_to_response('home.html', context)
