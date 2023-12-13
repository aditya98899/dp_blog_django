from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Article, Topic
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home_view(request):
    #get all articles
    article_list = Article.objects.all()
    topic_list = Topic.objects.all()
    paginator = Paginator(article_list, 8)
    page = request.GET.get('p', 1)
    #get article for this page
    articles = paginator.get_page(page)
    ctx = {
        'articles': articles,
        'topic': topic_list, 
    }
    return render(request, 'blog/home.html', ctx)
@login_required
def add_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)
        image = request.FILES.get('image')
        author = request.user
        if len(title) < 3:
            messages.error(request, 'Tilte must be at least 3 charecters.')
            return redirect('add')
        if len(content) < 50:
            messages.error(request, 'Content must be at least 50 charecters.')
            return redirect('add')
        if not image:
            messages.error(request, 'Image is required.')
            return redirect('add')
        article = Article(title = title, image = image, content = content, topic = topic, author = author)
        article.save()
        messages.success(request, 'Article created successfully')
        return redirect('my_articles')
    return render(request, 'blog/add.html', {
        'topics' : Topic.objects.all()
    })

@login_required
def my_article(request):
    article_list = Article.objects.filter(author = request.user)
    paginator = Paginator(article_list, 8)
    page = request.GET.get('p', 1)
    ctx = {
        'articles' : paginator.get_page(page)
    }
    return render(request, 'blog/my_articles.html', ctx)

@login_required
def inc_like(request, id):
    article = Article.objects.get(id=id)
    article.like  += 1
    article.save()
    return redirect('detail', id=id)

def detail_view(request, id):
    ctx = {'article': Article.objects.get(id=id)}
    return render(request, 'blog/detail.html', ctx)

@login_required
def edit_view(request, id):
    
    if request.method == "POST":
        article = Article.objects.get(id=id)
        title = request.POST.get('title')
        content = request.POST.get('content')
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)
        image = request.FILES.get('image')
        author = request.user
        if len(title) < 3:
            messages.error(request, 'Tilte must be at least 3 charecters.')
            return redirect('edit',id=id)
        if len(content) < 50:
            messages.error(request, 'Content must be at least 50 charecters.')
            return redirect('edit',id=id)
        if not image:
            image=article.image
        
        article.title = title
        article.content=content
        article.topic=topic
        article.image=image
        article.save()
        messages.success(request,'Article updated successfully')
        return redirect('my_articles')
    return render(request, 'blog/add.html',{

        'article' : Article.objects.get(id=id),
        'topics' : Topic.objects.all()
    })
    

@login_required
def delete_view(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    messages.success(request, 'Article deleted successgully')
    return redirect('my_articles')