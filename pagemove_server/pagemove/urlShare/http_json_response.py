import json

from django.http import HttpResponse


class HttpJSONResponse(HttpResponse):
    def __init__(self, data):
        json_string = json.dumps(data)
        super(HttpJSONResponse, self).__init__(json_string)
