from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from shortenersite.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from django.shortcuts import render
 
def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('shortenersite/index.html', c)
 
def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)

def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        try:
            url_obj = Urls.objects.get(httpurl=url)
        except:
            url_obj = None
        if url_obj is None:
            short_id = get_short_code()
            b = Urls(httpurl=url, short_id=short_id)
            b.save()

            response_data = {}
            response_data['url'] = short_id
        else:
            response_data = {}
            response_data['url'] = url_obj.short_id
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}),
             content_type="application/json")
 
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))

        return short_id


def get_url(request):
    short_url = request.POST.get("shorturl", '')
    print(short_url)
    if not (short_url == ''):
        try:
            real_url = Urls.objects.get(short_id=short_url)
        except:
            real_url = None
        print(real_url)
        if real_url is not None:
            data = json.dumps(real_url, indent=4, sort_keys=True, default=str)
            return HttpResponse(data, content_type='application/json')

        return HttpResponse(json.dumps({"error": "error occurs"}),
                            content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}),
                        content_type="application/json")
