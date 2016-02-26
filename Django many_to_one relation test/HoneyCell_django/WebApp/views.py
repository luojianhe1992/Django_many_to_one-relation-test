from django.shortcuts import render

# allow us to redirect
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.template import RequestContext, loader

# import the User class in models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# import the auth.models User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from WebApp.models import *


@login_required
def index(request):
    print("in the index function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/index.html', context)



# registration is normal route, and login is login is "django.contrib.views.login"
def registration(request):
    errors = []
    context = {}
    if request.method == "GET":
        return render(request, 'WebApp/register.html', context)

    # add 'errors' attribute to the context
    context['errors'] = errors

    password1 = request.POST['password']
    password2 = request.POST['password_confirmation']

    if password1 != password2:

        print("Passwords did not match.")

        # error1 happens
        errors.append("Passwords did not match.")

    if len(User.objects.all().filter(username = request.POST['user_name'])) > 0:
        print("Username is already taken.")

        # error2 happens
        errors.append("Username is already taken.")

    if errors:
        return render(request, 'WebApp/register.html', context)

    # create a new user from the valid form data, using create_user function with 2 arguments, 'username' and 'password'
    new_user = User.objects.create_user(username=request.POST['user_name'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
    new_user.save()

    # using 'authenticate' function
    new_user = authenticate(username = request.POST['user_name'], password = request.POST['password'])

    # using 'login' function
    login(request, new_user)

    # using 'redirect' function
    return redirect(reverse('message'))

@login_required
def message(request):
    print("in the message function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/message.html', context)

@login_required
def upload(request):
    print("in the upload function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/upload.html', context)

@login_required
def preprocess(request):
    print("in the preprocess function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/preprocessing.html', context)

@login_required
def visualization(request):
    print("in the visualization function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/knnresult.html', context)

# def logout view
def my_logout(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def honeycell(request):
    print("in the honeycell function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/honeycell.html', context)

@login_required
def honeycomb(request):
    print("in the honeycomb function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/honeycomb.html', context)

@login_required
def analytics(request):
    print("in the analytics function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/analytics.html', context)

@login_required
def add_reporter(request):
    print("in the add_reporter function.")

    context = {}
    context['user'] = request.user

    errors = []
    context['errors'] = errors

    if request.method == "GET":
        return render(request, 'WebApp/add_reporter.html', context)
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if len(Reporter.objects.filter(first_name=first_name)):
            print("The first_name already exist.")
            errors.append("The first_name already exist.")

            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email

            return render(request, 'WebApp/add_reporter.html', context)

        if len(Reporter.objects.filter(last_name=last_name)):
            print("The last_name already exist.")
            errors.append("The last_name already exist.")

            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email

            return render(request, 'WebApp/add_reporter.html', context)

        if len(Reporter.objects.filter(email=email)):
            print("The email already exist.")
            errors.append("The email already exist.")

            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email

            return render(request, 'WebApp/add_reporter.html', context)

        new_reporter_instance = Reporter(first_name=first_name,
                                         last_name=last_name,
                                         email=email)
        new_reporter_instance.save()
        print("new_reporter_instance already save.")
        return render(request, 'WebApp/add_reporter.html', context)


from WebApp.forms import *

@login_required
def add_article(request):
    print("in the add_article function.")

    context = {}
    context['user'] = request.user

    errors = []
    context['errors'] = errors

    if request.method == "GET":
        form = ArticleForm()
        context['form'] = form
        return render(request, 'WebApp/add_article.html', context)

    else:
        form = ArticleForm(request.POST, request.FILES)
        context['form'] = form

        if not form.is_valid():
            print("The form is not valid.")
            context['form'] = form
            return render(request, 'WebApp/add_article.html', context)

        if len(Article.objects.filter(reporter=form.clean_reporter(), headline=form.clean_headline())):
            print("The headline for this reporter already exist.")
            errors.append("The headline for this reporter already exist.")

            return render(request, 'WebApp/add_article.html', context)

        if len(Article.objects.filter(reporter=form.clean_reporter(), content=form.clean_content())):
            print("The content for this reporter already exist.")
            errors.append("The content for this reporter already exist.")

            return render(request, 'WebApp/add_article.html', context)

        if len(Article.objects.filter(reporter=form.clean_reporter(), pub_date=form.clean_pub_date())):
            print("The pub_date for this reporter already exist.")
            errors.append("The pub_date for this reporter already exist.")

            return render(request, 'WebApp/add_article.html', context)


        print("The form is valid.")
        form.save()
        print("Already save the form.")
        return render(request, 'WebApp/add_article.html', {'user': request.user, 'form': ArticleForm()})

@login_required
def show_reporters(request):
    print("in the function show_reporters.")

    context = {}
    context['user'] = request.user

    reporters = Reporter.objects.all()
    context['reporters'] = reporters

    return render(request, 'WebApp/show_reporters.html', context)


@login_required
def show_articles(request):
    print("in the function show_articles.")

    context = {}
    context['user'] = request.user

    articles = Article.objects.all()
    context['articles'] = articles

    return render(request, 'WebApp/show_articles.html', context)


@login_required
def show_reporters_articles(request):
    print("in the function show_reporters_articles")

    context = {}
    context['user'] = request.user

    data = []
    context['data'] = data

    for each_reporter in Reporter.objects.all():
        each_reporter_articles = {}
        data.append(each_reporter_articles)
        each_reporter_articles['reporter'] = each_reporter
        each_reporter_articles['articles'] = Article.objects.filter(reporter=each_reporter)
        each_reporter_articles['row_span'] = len(Article.objects.filter(reporter=each_reporter)) + 1

    print("%" * 30)
    print(data)
    print("%" * 30)

    return render(request, 'WebApp/show_reporters_articles.html', context)