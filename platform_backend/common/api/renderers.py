from rest_framework.renderers import JSONRenderer
from rest_framework import status

class ResponseDataType:
    """Constant values of response data types"""

    OBJECT = "Object"
    ARRAY = "Array"

class JSONResponseRenderer(JSONRenderer):
    # Override render() method to custom the response
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """

        # Get HTTP status code from renderer context
        status_code = renderer_context["response"].status_code

        # Reformat the response
        response = {
            "is_error": False,
            "message": "",
            "type": ResponseDataType.OBJECT,
            "data": data,
        }

        # Check if the status is success or not
        if not status.is_success(status_code):
            response["is_error"] = True

        # Specify the type of response data
        if isinstance(data, list):
            response["type"] = ResponseDataType.ARRAY

        # Call super to render the response
        return super(JSONResponseRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
