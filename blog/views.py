from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, query
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Comment, Categories, Rate
from .forms import LoginForm, RegisterForm, CommentForms, NewPostForm, RatePostForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, UpdateView,CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

class IndexView(ListView):
    model = Post
    paginate_by = 2
    template_name = 'blog/index.html'


class LogoutView(View):
    
    def get(self,request):
        logout(request)
        return redirect('blog:index')

class RatingRetrieveUpdateView(UpdateView, DetailView, LoginRequiredMixin):
    model = Post
    fields = '__all__'
    template_name = 'blog/post_form.html'
    
    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        self.object = self.get_object()
        try:
            r = Rate(owner=request.user, post=self.object)
            r.save()
            request.POST['rating_sum'] = self.object.rating_sum + int(request.POST['rating_sum'])
            return super(RatingRetrieveUpdateView, self).post(request, **kwargs)
        except BaseException as e:
            pass
        return redirect('blog:detail', pk=self.object.id)    
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['rate_form'] = RatePostForm()
        rate = 0
        r = Rate.objects.filter(post=pk).count()
        if r > 0:
            rate = self.object.rating_sum / r
        context['rate'] = rate

        self.object.views += 1
        self.object.save()

        return context

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'blog/register.html'

    def post(self, request, **kwargs):
        form = RegisterForm(request.POST or None)
        registred = False
        if form.is_valid():
            sign_up = form.save(commit=False)
            sign_up.password = make_password(form.cleaned_data['password'])
            sign_up.status = 1
            sign_up.save()
            registred = True
        return render(request, 'blog/register.html', {'form': form, 'registred': registred})

class LoginView(FormView):
    form_class  = AuthenticationForm
    template_name = 'blog/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:index')
class SearchView(ListView):
    template_name = 'blog/search.html'
    model = Post
    context_object_name = 'result'

    def get_queryset(self):
        query = self.request.GET.get('query', None)
        result = []
        if query is None:
            return result
        result = self.model.objects.filter(Q(title__icontains=query) |
                                    Q(clipped_text__icontains=query) |
                                    Q(text__icontains=query))
        return result
    
class NewPostView(CreateView, LoginRequiredMixin):
    form_class = NewPostForm
    model = Post
    template_name = 'blog/add_post.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()        
        return redirect('blog:index')

class UserDetailView(DetailView, LoginRequiredMixin):
    model= User
    template_name = 'blog/user.html'


def error_404(request, exception):
    return render(request, 'blog/404.html')
