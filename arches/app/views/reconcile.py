'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import csv
import sys
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.utils.JSONResponse import JSONResponse
from django.http import HttpResponseNotFound, QueryDict, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from arches.app.models import models

metadata = {
    "name": "Arches Reconciliation Service",
    "identifierSpace": "",
    "schemaSpace": "",
    "defaultTypes": [{"id": "/arches/arches", "name" : "Node Name"}]
    }


node_objs = models.Node.objects.all()
records = [n.name for n in node_objs]


def search(query):

    # Initialize matches.
    matches = []

    # Search person records for matches.
    for r in records:
        if query.split('.')[0].lower().replace('_', ' ') == r:
            matches.append({
                    "id": r,
                    "name": r,
                    "score": 100,
                    "match": query.split('.')[0].lower().replace('_', ' ') == r,
                    "type": [{"id": "/people/person", "name": "Node Name"}]
                    })

    print >> sys.stderr, matches
    return matches


def jsonpify(obj):
    """
    Like jsonify but wraps result in a JSONP callback if a 'callback'
    query param is supplied.
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return JSONSerializer().serialize(obj)

@csrf_exempt
def reconcile(request):
    if request.GET.get('callback'):
        # a jsonp response!
        data = '%s(%s);' % (request.GET.get('callback'), metadata)
        return HttpResponse(data, "text/javascript")


    # If a single 'query' is provided do a straightforward search.
    if request.POST.get('query'):
        query = request.POST.get('query')
        # If the 'query' param starts with a "{" then it is a JSON object
        # with the search string as the 'query' member. Otherwise,
        # the 'query' param is the search string itself.
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        return JSONResponse({"result": results})

    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    if request.POST.get('queries'):
        queries = request.POST.get('queries')
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": search(query['query'])}
        return JSONResponse(results)

    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return JSONResponse(metadata)
