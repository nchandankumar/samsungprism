from urllib import request
from xml.etree.ElementTree import Comment
from django.shortcuts import render,redirect
from .models import Mobile,Category,Photo,Comments
from .forms import CommentForm
from django.contrib import messages

# Create your views here.
def welcome(request):
	return render(request,'main/welcome.html')
def mobile(request):
    # mob=Mobile.objects.filter(brand_id=id)
    mobile = Mobile.objects.all()
    # name=Brand.objects.get(id=id)
    context = {
        'mobile':mobile,
        } 
    return render(request, 'main/model.html',context)
def category(request,mid):
	i=mid
	name=Mobile.objects.get(id=mid)
	mob=Category.objects.filter(mobile_id=mid)
	cat = Category.objects.all()
	context={
        'mob': mob,
        'category':cat,
        'id':i,
        'name':name
    }
	return render(request, 'main/category.html',context)
def viewCategoryImage(request,mid,cid):
	name=Mobile.objects.get(id=mid)
	cate=Category.objects.get(id=cid)
	photo=Photo.objects.filter(category_id=cid,mobile_id=mid)	
	context={
		'mid':mid,
		'cid':cid,
		'name':name,
		'cate':cate,
        'photos':photo   
    }
	return render(request, 'main/view.html',context) 
def editor(request,mid,cid):	
	name=Mobile.objects.get(id=mid)
	cate=Category.objects.get(id=cid)
	photo=Photo.objects.filter(category_id=cid,mobile_id=mid)
	samsung=Photo.objects.filter(cname='samsung',category_id=cid,mobile_id=mid)
	photos=[]
	photos1=[]
	for i in photo:
		if i.cname =='samsung':
			continue
		else:
			photos.append(i)
	for i in range(len(photos)):
		if i <=3:
			photos1.append(photos[i])
	if request.method == 'POST':
		n = request.POST.get('name')
		cmt = request.POST.get('comment')
		res=Comments.objects.create(mobile=name,category=cate,name=n,comment=cmt)
		if res:
			messages.info(request, 'Thank You for the comment')
		else:
			messages.info(request, 'No Comment posted')
	form = CommentForm()
	cmmt = Comments.objects.filter(category_id=cid,mobile_id=mid)
	context={
		'mid':mid,
		'cid':cid,
		'name':name,
		'cate':cate,
		'samsung': samsung,
        'photos':photos1,
		'form':form,
		'cmmt':cmmt 
    }
	
	return render(request,'main/editor.html',context)
def photocrop(request,mid,cid):
	img = request.POST.get('selectedimage')
	photo=Photo.objects.filter(pk=img,category_id=cid,mobile_id=mid)
	context={
		'mid':mid,
		'cid':cid,
        'photo':photo 
    }
	return render(request,'main/photocrop.html',context)
def report(request,mid):
	data= Photo.objects.filter(mobile_id=mid)
	cats = Category.objects.filter(mobile_id =mid)
	l=[]
	for i in data:
		l.append(i.cname)
	context ={
		'cname':set(l),
		'data':data,
		'cats': cats
	}
	return render(request,'main/report.html',context)