from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Comment, Categories, Rate
from .forms import LoginForm, RegisterForm, CommentForms, NewPostForm, RatePostForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, UpdateView,CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


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


def rate(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = RatePostForm(request.POST)
        if form.is_valid():
            try:
                r = Rate(owner=request.user, post=post)
                r.save()
                post.rating_sum = post.rating_sum + form.cleaned_data['rating_sum']
                post.save()
            except BaseException as e:
                pass
    return HttpResponseRedirect(f'/view/{pk}/')


def reqister(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.last_name = form.cleaned_data['lastName']
            user.first_name = form.cleaned_data['firstName']
            user.save()
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request, 'blog/login.html', {'form': form})


def search(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.GET.get('query') is None:
        return render(request, 'blog/search.html')

    res = Post.objects.filter(Q(title__icontains=request.GET.get('query')) |
                              Q(clipped_text__icontains=request.GET.get('query')) |
                              Q(text__icontains=request.GET.get('query')))
    return render(request, 'blog/search.html', {'result': res})


def add_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    fix_me = ""

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.owner = request.user
            post.title = form.cleaned_data['title']
            post.clipped_text = form.cleaned_data['clipped_text']
            post.text = form.cleaned_data['text']
            post.save()
            fix_me = "Запись успешно добавлена"
    else:
        form = NewPostForm()

    return render(request, 'blog/add_post.html', {'form': form, 'msg': fix_me})


def user(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    user = get_object_or_404(User, id=pk)
    posts = Post.objects.filter(owner = pk)
    context = {
        'user':user,
        'posts':posts,
    }
    return render(request, 'blog/user.html', context)


def error_404(request, exception):
    return render(request, 'blog/404.html')
