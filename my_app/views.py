from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import  requests
# from .models import Search
from . import models
# Create your views here.

BASE_URL='https://mumbai.craigslist.org/search/?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'
def home(request):
    return render(request,'base.html')

def new_search(request):
    search=request.POST.get('search')
    # add to search table
    models.Search.objects.create(search=search)
    final_url=BASE_URL.format(quote_plus(search))
    response=requests.get(final_url)

    soup=BeautifulSoup(response.text,features='html.parser')

    post_listing=soup.findAll('li',class_='result-row')

    final_posting=[]

    for post in post_listing:
        post_title=post.find(class_='result-title')
        post_title=post_title.get_text(strip=True)

        post_url=post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price= post.find(class_='result-price')
            post_price = post_price.get_text(strip=True)
        else:
            post_price='N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_id)


        else:
            post_image_url='https://mumbai.craigslist.org/images/peace.jpg'


        final_posting.append((post_title,post_url,post_price,post_image_url))

    front_end_data={
        'search':search,
        'final_posting':final_posting
    }
    return render(request,'My_App/index.html',front_end_data)