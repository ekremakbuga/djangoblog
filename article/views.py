from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    '''context={
        "number":[1,2,3,4,5,6]
        }
    '''
    return render(request,"index.html") #,context
def about(request):
    return render(request,"about.html")
'''def detail(request,id):
    return HttpResponse("Detail:"+str(id))
'''
def articles(request):
    keyword=request.GET.get("keyword")
    if keyword:
        articles=Article.objects.filter(title__contains= keyword)
        context={
            "articles":articles
        }
        return render(request,"articles.html",context)

    articles=Article.objects.all()
    context={
        "articles" : articles
    }
    return render(request,"articles.html",context)


@login_required(login_url="/user/login/")
def dashboard(request):
    articles=Article.objects.filter(author=request.user)
    context={
        "articles":articles
    }

    return render(request,"dashboard.html",context)

@login_required(login_url="/user/login/")
def addarticle(request):
    form=ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article=form.save(commit=False)
        article.author=request.user
        article.save()
        '''
        form.save() kaydetme yapinca ilk basta article objesi olusturuyor
        daha sonra article.save() yapiyor aslinda biz article objesi olusturduktan sonra biz buraya
        bir tane user vermemiz lazim yazar bilgisi vermeden kaydedince django bize hata veriyor
        form.save(commit=False) sen burda save islemini gerceklestirme bunu ben obje üzerinden yapacam

        '''
        messages.success(request,"Makale Başarıyla Oluşturuldu...")
        return redirect("article:dashboard")

    context={
        "form" :form
    }
    return render(request,"addarticle.html",context)

def detail(request,id): #neden her zaman request aliyordu ek olarak dinamik url oldugu icin id alcak
    #article=Article.objects.filter(id=id).first()
    article=get_object_or_404(Article,id=id)
    comments=article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})
@login_required(login_url="/user/login/")
def updateArticle(request,id):
    article=get_object_or_404(Article,id=id)
    form=ArticleForm(request.POST or None,request.FILES or None,instance=article)
    if form.is_valid():
        article=form.save(commit=False)
        article.author=request.user
        article.save()
        messages.success(request,"Makale Başarıyla Güncellendi...")
        return redirect("article:dashboard")
    context={
        "form" :form
    }
    return render(request,"update.html",context)

@login_required(login_url="/user/login/")
def deleteArticle(request,id):
    article=get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Makaleniz Başarıyla Silindi...")
    return redirect("article:dashboard")

def addComment(request,id):
    article=get_object_or_404(Article,id=id)
    if request.method=="POST":
        comment_author=request.POST.get("comment_author")
        comment_content=request.POST.get("comment_content")
        newComment=Comment(comment_author=comment_author,comment_content=comment_content)
        newComment.article=article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))














    


    


