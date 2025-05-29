from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView,FormView
from .models import Posts,CustomUser
from .forms import PostsForm,CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    return render(request, 'home.html')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CustomUserCreationForm  # Usamos o formulário personalizado
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Salva o usuário e faz o login automaticamente
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Redireciona o usuário autenticado para a página inicial
        if self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('perfil')

@login_required
def perfil(request):
    # Obtenha o perfil do usuário logado
    user_profile = CustomUser.objects.get(username=request.user.username)
    
    # Obtenha os posts do usuário logado
    user_posts = Posts.objects.filter(autor_id=request.user.id)
    return render(request, 'perfil.html', {'user_profile': user_profile, 'user_posts': user_posts})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de login após o logout

class PostListView(ListView):
    model = Posts
    template_name = 'post-list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = Posts.objects.all()

        # Verifica se há um termo de busca na consulta GET
        search_query = self.request.GET.get('q')
        if search_query:
            # Filtra os posts com base no título que contenha o termo de busca
            queryset = queryset.filter(titulo__icontains=search_query)
        return queryset
    

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Posts
    form_class = PostsForm
    template_name = 'post-form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        # Define o autor do post como o usuário logado
        form.instance.autor = self.request.user
        # Exibe uma mensagem de sucesso
        messages.success(self.request, 'O post foi criado com sucesso')
        # Chama o método form_valid da superclasse para continuar com a validação do formulário
        return super().form_valid(form)
    
    

def post_update(request, id):
    post = get_object_or_404(Posts, id=id) # id do post
    form = PostsForm(request.POST or None, request.FILES or None, instance=post) # pega as informações do form
    if form.is_valid(): # se for valido
        form.save() # salva
        
        messages.warning(request, 'O post foi atualizado com sucesso') # mensagem quando cria o post
        return HttpResponseRedirect(reverse('post-list')) # coloquei para retornar post-list
         
    return render(request, 'post-form.html', {"form": form}) # nesse template


def post_delete(request, id): 
    post = Posts.objects.get(id=id) # pelo ID pega o objeto
    if request.method == 'POST':         
        post.delete()
        messages.error(request, 'O post foi deletado com sucesso') # quando deleta post 
        return HttpResponseRedirect(reverse('post-list')) # retorna rota post-list
    return render(request, 'post-delete.html') # nesse template