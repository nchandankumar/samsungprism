import imp
from urllib import request
from xml.etree.ElementTree import Comment
from django.conf import settings
from django.shortcuts import render,redirect
from .models import Mobile,Category,Photo,Comments
from .forms import CommentForm
from django.contrib import messages

# cropping modules
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
from django.core import files

temp_image_name = "temp_image_name.png"

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
		if i <=1:
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

def temp_image(imagestring,pid):
	INCORRECT_PADDING_EXCEPTION = "Incorrect Padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(f"{settings.TEMP}/{pid}"):
			os.mkdir(settings.TEMP+"/"+str(pid))
		url = os.path.join(f"{settings.TEMP}/{pid}",temp_image_name)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imagestring)
		with storage.open('','wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imagestring+="="* ((4-len(imagestring)%4)%4)
			return temp_image(imagestring,pid)
	return None
def photocrop(request,mid,cid,*args, **kwargs):
	payload ={}
	img = request.POST.get('selectedimage')
	photo=Photo.objects.filter(pk=img,category_id=cid,mobile_id=mid)
	url = []
	
	for i in photo:
		url.append(i.image.url)
	s=url[0]
	print(s)
	# imgurl=temp_image(photo,img)
	# print(imgurl)
	imge = cv2.imread(s[1:])
	# cropX = int(float(str(request.POST.get("cropX"))))
	# cropY = int(float(str(request.POST.get("cropY"))))
	# cropWidth = int(float(str(request.POST.get("cropWidth"))))
	# cropHeight = int(float(str(request.POST.get("cropHeight"))))

	# if cropX < 0:
	# 	cropX = 0
	# if cropY < 0:
	# 	cropY = 0
	# crop_img=img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
	# ch=cv2.imwrite(imgurl,crop_img)
	# user.profile_image.save("pimage.png",files.File(open(imgurl,"rb")))
	
	
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

# def crop_image(request, *args, **kwargs):
# 	_payload ={}
# 	user =request.user
# 	if request.POST and user.is_a