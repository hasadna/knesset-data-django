from django.views.generic import View
from django.http.response import HttpResponse
import json
from .utils import get_all_mk_names

class GetAllMkNamesView(View):

    def get(self, request):
        mks, mk_names = get_all_mk_names()
        mks = [{"id": mk.id} for mk in mks]
        return HttpResponse(json.dumps([mks, mk_names]))
