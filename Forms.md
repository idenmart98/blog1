# HTML-формы

В HTML форма - это набор элементов внутри, `<form>...</form>` которые позволяют посетителю делать такие вещи, как ввод текста, выбирать параметры, манипулировать объектами или элементами управления и т.д. А затем отправлять эту информацию обратно на сервер.

Форма состоит из `input` элементов.

Помимо своих `input` элементов, форма должна определять две вещи:
- *где* : URL-адрес, на который должны быть отправлены данные
- *как* : HTTP-метод, используя который мы должны отправить данные

# GET и POST
`GET` и `POST` являются единственными методами HTTP, которые можно использовать при работе с формами.


## Создание формы
### Работа, которую нужно сделать
Предположим, вы хотите создать простую форму на своем веб-сайте, чтобы получить имя пользователя. Вам понадобится что-то вроде этого в вашем шаблоне:
```html
<form action="/your-name/" method="post">
    <label for="your_name">Your name: </label>
    <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
    <input type="submit" value="OK">
</form>
```

### Создание формы в Django

Создадим в нашей папке приложения файл `forms.py`
```python
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
```

У `Form` экземпляра есть `is_valid()` метод, который запускает процедуры проверки для всех его полей. Если при вызове этого метода все поля содержат действительные данные, он:

- возвращает `True`
- помещает данные формы в `cleaned_data` атрибут.

Чтобы обработать форму, нам нужно создать ее экземпляр в представлении для URL-адреса, по которому мы хотим, чтобы он был опубликован:

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
```

### Шаблон
В нашем шаблоне особо много делать не нужно :
```html
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```
