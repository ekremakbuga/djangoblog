from django.contrib import admin
from article.models import Article,Comment   #.models idi hata verdi diye degistirdim



# Register your models here.

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display=["title","author","created_date"]
    list_display_links=["title","created_date"]

    search_fields=["title"]
    list_filter=["created_date"]
    class Meta:
        model=Article


