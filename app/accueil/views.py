from django.shortcuts import render


def index(request):
    """Page d'accueil du site."""
    return render(request, "accueil/index.html")
