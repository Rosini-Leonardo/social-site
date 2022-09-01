from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,DeleteView
from django.http import HttpResponseRedirect , HttpResponseBadRequest

from .mixins import StaffMixing
from .models import Discussione,Post,Sezione
from .forms import DiscussioneModelForm,PostModelForm

# Create your views here.
class CreaSezione(StaffMixing,CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "forum/crea_sezione.html"
    success_url = "/"
    

def visualizza_sezione(request,pk):
    sezione = get_object_or_404(Sezione,pk=pk)
    # Inverse order (from the most recent)
    discussioni_sezione = Discussione.objects.filter( 
        sezione_appartenenza = sezione 
    ).order_by("-data_creazione")

    context = { 
        "sezione" : sezione,
        "discussioni":discussioni_sezione,
    }
    return render(request, 'forum/singola_sezione.html',context)

@login_required
def crea_discussione(request,pk):
    sezione = get_object_or_404(Sezione,pk=pk)
    if request.method == 'POST':
        form = DiscussioneModelForm(request.POST)
        if form.is_valid():
            # Create a 'commit'
            discussione = form.save(commit=False)
            # Update values 
            discussione.sezione_appartenenza = sezione
            discussione.autore_discussione = request.user
            # Save the query
            discussione.save()

            primo_post = Post.objects.create(
                discussione = discussione,
                autore_post = request.user,
                contenuto = form.cleaned_data['contenuto']
            )
            
            # Redirect to the 'discussione' created
            return HttpResponseRedirect(discussione.get_absolute_url())
    else:
        form = DiscussioneModelForm()
    context = { 'form': form, "sezione" : sezione }
    return render(request, 'forum/crea_discussione.html',context)

def visualizza_discussione(request,pk):
    discussione = get_object_or_404(Discussione,pk=pk)
    posts_discussione = Post.objects.filter(discussione = discussione)
    form_risposta = PostModelForm()

    # Pagination 
    paginator = Paginator(posts_discussione, 4)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    context = {
        "discussione" : discussione,
        "posts_discussione" : posts,
        "form_risposta" : form_risposta,
    }
    return render(request,'forum/singola_discussione.html',context)

@login_required
def aggiungi_risposta(request,pk):
    discussione = get_object_or_404(Discussione,pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.discussione = discussione
            form.instance.autore_post = request.user
            form.save()
            # Success - redirect
            url_discussione = reverse("discussione_view",kwargs={"pk":pk})

            # get number of page and redirect
            page_in_discussione = discussione.get_n_pages()
            if page_in_discussione > 1:
                success_url = url_discussione + "?page=" + str(page_in_discussione)
                return HttpResponseRedirect(success_url)
            
            # normal redirect
            else:
                return HttpResponseRedirect(url_discussione)
    # error
    else:
        return HttpResponseBadRequest()


class rimuoviPost(DeleteView):
    model = Post
    success_url = "/"
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_post_id = self.request.user.id)