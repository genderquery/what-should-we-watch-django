import os
from collections import namedtuple

import requests

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', None)
BASE_URL = 'https://api.themoviedb.org/3/'
DEFAULT_PARAMS = {
    'api_key': TMDB_API_KEY
}

_configuration = None


def get_configuration():
    global _configuration
    if _configuration:
        return _configuration
    response = requests.get(BASE_URL + 'configuration',
                            params={**DEFAULT_PARAMS})
    response.raise_for_status()
    data = response.json()
    _configuration = namedtuple(
        'TmdbConfiguration', field_names=data.keys())(*data.values())
    return _configuration


def search_movies(query):
    response = requests.get(BASE_URL + 'search/movie',
                            params={**DEFAULT_PARAMS, 'query': query})
    response.raise_for_status()
    return response.json()


def get_movie(movie_id):
    response = requests.get(BASE_URL + 'movie/{movie_id}'.format(movie_id=movie_id),
                            params={**DEFAULT_PARAMS})
    response.raise_for_status()
    return response.json()
