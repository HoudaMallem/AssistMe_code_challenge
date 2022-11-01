from datetime import datetime

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """ a custom json render class to render the response in the right format  """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {"errors": {}, "data": [], 'date': datetime.now()}
        if 'ErrorDetail' in str(data):
            response_data["errors"] = data
        elif data:
            response_data["data"] = data
        response = super(CustomJSONRenderer,
                         self).render(response_data, accepted_media_type,
                                      renderer_context)
        return response
