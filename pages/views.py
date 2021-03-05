from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html")


def get_results_view(request, name_search):

    r = requests.get('https://api.spotify.com/v1/search', params={'q':name_search})
    if r.status_code == 200:
        return HttpResponse('Yay, it worked')
        print(r)
    else:
        return HttpResponse('Could not save data')
    artist = Artist()
    context = {
        'artist':artist
    }
    return render(request, "search_results.html", context)
