from django.shortcuts import render, HttpResponse

from news_app.services.spider import Spider

# Create your views here.

def home(request):
    spider = Spider()
    news_list = spider.crowl_todays()

    return render(request, 'home.html', {"news_item_list": news_list})
