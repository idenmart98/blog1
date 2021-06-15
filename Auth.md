# Авторизация пользователя
```python
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
```

# Аутентификация в запросах
```python
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

# Как авторизовать пользователя
Если у вас есть аутентифицированный пользователь, которого вы хотите присоединить к текущему сеансу - это делается с помощью `login()` функции.

```python
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```

# Как выйти из системы 

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
```


## Ограничение доступа для авторизованных пользователей
Самый простой способ ограничить доступ к страницам - это проверить `request.user.is_authenticated` и перенаправить на страницу входа:
```python
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
```

Или отобразить сообщение об ошибке:

```python
from django.shortcuts import render

def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/login_error.html')
    # ...
```

## Декоратор login_required
```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```