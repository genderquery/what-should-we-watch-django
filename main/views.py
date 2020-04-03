from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.db import models

from lib import tmdb

from .models import Party, Suggestion, Vote


def index(request):
    return render(request, 'main/index.html')


def join(request):
    party_code = request.POST['party_code'].strip().upper()
    try:
        party = Party.objects.get(code=party_code)
    except Party.DoesNotExist:
        messages.error(
            request,
            _("There isn't a party with the code '%(party_code)s'" %
              {'party_code': party_code})
        )
        return redirect('index')
    request.session['party_id'] = party.id
    return redirect('party')


def start(request):
    party = Party.objects.create()
    request.session['party_id'] = party.id
    return redirect('party')


def party(request):
    try:
        party_id = request.session['party_id']
        party = Party.objects.get(pk=party_id)
    except:
        return redirect('index')

    def get_details(suggestion):
        suggestion.details = tmdb.get_movie(suggestion.media_id)
        return suggestion

    suggestions = map(get_details, (party.suggestions
        .annotate(score=models.functions.Coalesce(models.Sum('votes__value'), 0))
        .order_by('-score')
    ))
    
    context = {
        'party': party,
        'suggestions': suggestions,
    }

    return render(request, 'main/party.html', context)


def search(request):
    query = request.GET['q']
    result = tmdb.search_movies(query)
    context = {
        'result': result
    }
    return render(request, 'main/results.html', context)


def add(request):
    party_id = request.session['party_id']
    media_id = request.POST['media_id']
    media_type = request.POST['media_type']
    Suggestion.objects.create(
        party_id=party_id,
        media_id=media_id,
        media_type=media_type,
    )
    return redirect('party')


def vote(request):
    session_id = request.session.session_key
    suggestion_id = request.POST['suggestion']
    value = request.POST['vote']
    Vote.objects.update_or_create(
        defaults={'value': value},
        session_id=session_id,
        suggestion_id=suggestion_id,
    )
    return redirect('party')
