import json
import time
from django.contrib import messages
# TODO: These need to be deleted or revised.  They are not valid for Django 2.2.
# TODO: Update to this? https://gist.github.com/DmytroLitvinov/39d9a1a93a46eb9da1e17d8e73f35e11
class AjaxMessaging(object):
    """
    To make django error messages set by django.contrib.messages framework
    are shown in templates when AJAx requests are made.

    Usage:
    1. add this middleware to the settings file's middleware list.
    2. In your app.js file, define a global $(document).ajaxComplete method and
    then iterate over all the messages that may be available in the json response; see below:
    $( document )
        .ajaxComplete(function(e, xhr, settings) {
            var contentType = xhr.getResponseHeader("Content-Type");

            if (contentType == "application/javascript" || contentType == "application/json") {
                var json = $.parseJSON(xhr.responseText);

                $.each(json.django_messages, function (i, item) {
                    createAlert(item.extra_tags, item.message, false);
                });
            }
        })
        .ajaxError(function(e, xhr, settings, thrownError) {
            createAlert("danger", "Error " + xhr.status + ": " +  thrownError, false);
        });
    """
    def process_response(self, request, response):
        if request.is_ajax():
            if response['Content-Type'] in ["application/javascript", "application/json"]:
                try:
                    content = json.loads(response.content)
                except ValueError as e:
                    return response

                django_messages = []

                storage = messages.get_messages(request)
                for message in storage:
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })
                if django_messages:
                    content['django_messages'] = django_messages
                    response.content = json.dumps(content)
        return response

# TODO: Delete?  Copied from https://github.com/timsavage/django-extras
class TimingMiddleware(object):
    """
    Appends the X-PROCESSING_TIME_MS header to all responses.
    This value is the total time spent processing a user request in microseconds.
    """
    REQUEST_ATTR = '_timing_start'
    RESPONSE_HEADER = 'X-PROCESSING_TIME_MS'

    def process_request(self, request):
        setattr(request, self.REQUEST_ATTR, time.clock())

    def process_response(self, request, response):
        start = getattr(request, self.REQUEST_ATTR, None)
        if start:
            length = time.clock() - start
            response[self.RESPONSE_HEADER] = "%i" % (length * 1000)
        return response