from django.urls import path
from .views import (
    aggiungi_risposta,
    CreaSezione,
    crea_discussione,
    visualizza_sezione,
    visualizza_discussione,
    rimuoviPost,
)

urlpatterns = [
    # Sezione
    path('nuova-sezione/',CreaSezione.as_view(),name="crea_sezione"),
    path('sezione/<int:pk>/',visualizza_sezione,name="sezione_view"),
    # Discussione
    path('sezione/<int:pk>/crea-discussione/',crea_discussione,name="crea_discussione"),
    path('discussione/<int:pk>/',visualizza_discussione,name="discussione_view"),
    # Reply
    path('discussione/<int:pk>/rispondi/',aggiungi_risposta,name="risposta_view"),
    # Delete Post
    path('discussione/<int:id>/rimuovi-post/<int:pk>/',rimuoviPost.as_view(),name="rimuovi_post"),
]