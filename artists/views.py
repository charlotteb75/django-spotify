from django.shortcuts import render
import requests
from django.http import HttpResponse

from .models import Artist
from tracks.models import Track




def get_token(url_token, data, headers):
    """
    Cette fonction fait une requête à l'API Spotify avec le client id et le client secret de l'application
    enregistrée pour récupérer un token à jour.
    Args:
    url (String) : url vers laquelle on envoie la requête POST
    data (dict) : type de crendentials demandé
    headers (dict): client id et client secret encodés en base 64
    Returns:
    token (String) : token à jour
    """
    response = requests.request("POST", url_token, data=data, headers=headers)
    result = response.json()
    print(result)
    token = result['access_token']
    return token

def artist_list_view(request):

    name_search = request.GET.get('name_search')
    if name_search=='':
        return render(request, "error_page_home.html")
    else:
        url_token = "https://accounts.spotify.com/api/token"
        data = {"grant_type":"client_credentials"}
        headers = {
        'Authorization': "Basic NWUxZDZlZDg5NjE4NDY0MDljZjA0NzNiODIxNDBjNmE6NzE1ZTRhMzRiODYzNDQyZWJiNmM0YTQ1M2Y2OTY3YmI="
        }
        token = get_token(url_token, data, headers)
        headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + str(token),
        'cache-control': "no-cache",
        'Postman-Token': "e053cb84-262c-43e4-bbb9-d192250da6d6",
        }
        r = requests.get('https://api.spotify.com/v1/search', params={'q':name_search, 'type':'artist'}, headers = headers)
        if r.status_code == 200:
            artist_list = []
            for item in r.json()['artists']['items']:
                print(item['name'])

                try:
                    image = item['images'][0]['url']
                    artist = Artist(name = item['name'].replace("/"," "), genres = ", ".join(item['genres']), popularity=item['popularity'],
                    image = item['images'][0]['url'])
                    artist_list.append(artist)
                except:
                    artist = Artist(name = item['name'].replace("/"," "), genres = ", ".join(item['genres']), popularity=item['popularity'],
                    image = '/media/user_logo.jpg')
                    artist_list.append(artist)
        else:
            print(r.json())
            return HttpResponse('Could not get data')
        if len(artist_list)==0:
            return render(request, "error_page_not_found.html")
        else:
            context = {
            'artist_list':artist_list
            }
            return render(request, "artists/artist_list.html", context)



def artist_page_view(request, artist_name):

    #choice = request.GET.get('choice')
    print(artist_name)
    url_token = "https://accounts.spotify.com/api/token"
    data = {"grant_type":"client_credentials"}
    headers = {
    'Authorization': "Basic NWUxZDZlZDg5NjE4NDY0MDljZjA0NzNiODIxNDBjNmE6NzE1ZTRhMzRiODYzNDQyZWJiNmM0YTQ1M2Y2OTY3YmI="
    }
    token = get_token(url_token, data, headers)
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer " + str(token),
    'cache-control': "no-cache",
    'Postman-Token': "e053cb84-262c-43e4-bbb9-d192250da6d6",
    }
    r = requests.get('https://api.spotify.com/v1/search', params={'q':artist_name, 'type':'artist'}, headers = headers)
    if r.status_code == 200:
        for item in r.json()['artists']['items']:
            if item['name'] == artist_name:

                try:
                    image = item['images'][0]['url']
                    artist = Artist(name = item['name'], genres = ", ".join(item['genres']), popularity=item['popularity'],
                    followers = f"{item['followers']['total']:,}", id_artist=item['id'], image = item['images'][0]['url'])
                    break
                except:
                    artist = Artist(name = item['name'], genres = item['genres'], popularity=item['popularity'],
                    followers = f"{item['followers']['total']:,}", id_artist=item['id'], image = "/media/user_logo.jpg")
                    break
    else:
        print(r.json())
        return HttpResponse('Could not get artist data')
    r = requests.get('https://api.spotify.com/v1/artists/'+str(artist.id_artist)+'/related-artists', headers = headers)
    if r.status_code == 200:
        related_artists = []
        for item in r.json()['artists']:
            print(item['name'])
            rel_artist = Artist(name = item['name'])
            related_artists.append(rel_artist.name)
    else:
        return HttpResponse('Could not get related artists')

    r = requests.get('https://api.spotify.com/v1/artists/'+str(artist.id_artist)+'/top-tracks', params={'market':'FR'}, headers = headers)
    if r.status_code == 200:
        top_tracks= []
        for item in r.json()['tracks']:
            print(item['preview_url'])
            track = Track(name = item['name'], release_date=item['album']["release_date"][:4], image=item['album']["images"][0]["url"],
            preview=item['preview_url'])
            top_tracks.append(track)
    else:
        print(r.status_code)
        return HttpResponse('Could not get top tracks')

    context = {
    'artist_page':artist,
    'related_artists': related_artists,
    'top_tracks':top_tracks
    }
    return render(request, "artists/artist_page.html", context)
