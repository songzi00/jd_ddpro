from django.shortcuts import render
from .models import Book
from django.db.models import Q
# Create your views here.



# 首页
def index(request):
    new_book = Book.objects.all()[39:47]
    return render(request, 'index.html',{'new_book':new_book} )



# 搜索页
def seach(request):
    if request.method == 'POST':
        keyword = request.POST.get('keywords')
        setattr_info = Book.objects.filter(book_name__icontains=keyword)
        if not setattr_info:
            message = '无搜索结果'
    return render(request, 'seach.html', locals())

# 详情页
def detail(request,id,):
    products = Book.objects.filter(id=id)
    recommend = Book.objects.all()[1:4]
    data = {
        'products': products,
        'recommend':recommend,

    }
    return render(request, 'detail.html', context=data)





