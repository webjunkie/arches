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

from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.apps import apps
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Max, Min
from arches.app.models import models
from arches.app.models.concept import Concept
from arches.app.utils.JSONResponse import JSONResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.views.concept import get_preflabel_from_conceptid
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.elasticsearch_dsl_builder import Bool, Match, Query, Nested, Terms, GeoShape, Range
from arches.app.utils.data_management.resources.exporter import ResourceExporter
from django.utils.module_loading import import_string
from arches.app.views.base import BaseManagerView

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class ImportExportView(BaseManagerView):
    def get(self, request):
        context = self.get_context_data(
            main_script='views/importexport',
        )
        return render(request, 'views/importexport.htm', context)

def home_page(request):
    return render(request, 'views/importexport.htm', {
        'main_script': 'views/importexport',
    })
