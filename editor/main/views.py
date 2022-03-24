import imp
import re
from tempfile import tempdir
from urllib import request
from urllib.robotparser import RequestRate
from xml.etree.ElementTree import Comment
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Mobile,Category,Photo,Comments,Photocrop
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
from ckeditor.fields import RichTextField

imgc = 0
photoc = ""
TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"
data=[]
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
	global data
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
	if request.method=="POST":
		data=request.POST.getlist("repid")
		if len(data)==2:
			return redirect('main:editor',mid,cid)
		else:
			context['error']="Limit was Exceeded"
			return render(request,'main/view.html',context)

		# print(data)
		# if(len(data)>2):
		# 	context['error']="Limit was Exceeded"
		# 	return render(request,'main/view.html',context)
	
	return render(request, 'main/view.html',context) 
	# return redirect('main:editor',context)
	# return redirect('main:editor',mid,cid)
	# return context
# def editor(request,mid,cid):

def editor(request,mid,cid):

	# data=viewCategoryImage(HttpResponse)
	# print(context)
	# mid=request.GET.get('mid')	
	# cid=request.GET.get('cid')
	global data	
	strData = ",".join(data)
	ph = []
	name=Mobile.objects.get(id=mid)
	cate=Category.objects.get(id=cid)
	for i in range(len(data)):
		ph.append(Photo.objects.get(category_id=cid,mobile_id=mid,id=int(data[i])))
		# itr.append(i)
	# for i,j in mylist:
	# 	for k in i:
	# 		print(k.image.url)
		# print(i,j)
	# photo1=Photo.objects.filter(category_id=cid,mobile_id=mid,id=int(data[0]))
	# photo2=Photo.objects.filter(category_id=cid,mobile_id=mid,id=int(data[1]))
	samsung=Photo.objects.filter(cname='samsung',category_id=cid,mobile_id=mid)
	# print("p1",photo1)
	# print("p2",photo2)
	# photos=[]
	# photos.append(samsung)
	# for i in data:
	# 	p=Photo.objects.filter(pk=i)
	# 	for j in p:
	# 		photos.append(j)
	# print(photos)
	# print(photo,"photo")
	# print(samsung)
	# photos1=[]
	# for i in photo:
	# 	if i.cname =='samsung':
	# 		continue
	# 	else:
	# 		photos.append(i)
	# for i in range(len(photos)):
	# 	if i <=1:
	# 		photos1.append(photos[i])
	# print(photos)
	# print(photos1)
	# print(photos1)
	if request.method == 'POST':
		n = request.POST.get('name')
		complist = request.POST.get('complist')
		plst = complist.split(",")
		cmt = request.POST.get('comment')
		res=Comments.objects.create(mobile=name,category=cate,name=n,comment=cmt)
		for eachPID in range(len(plst)):
			photoObj = Photo.objects.get(id = int(plst[eachPID]))
			res.compList.add(photoObj)
		if res:
			messages.info(request, 'Thank You for the comment')
		else:
			messages.info(request, 'No Comment posted')
	form = CommentForm()
	cmmt = Comments.objects.filter(category_id=cid,mobile_id=mid)

	compLIST = []
	for lore in cmmt:
		for eachlore in lore.compList.all():
			compLIST.append(eachlore.id)

	print("CID",cid,"-","MID",mid,"-","compLIST",compLIST)
	cmmt1 = Comments.objects.filter(category_id=cid,mobile_id=mid,compList__in = compLIST).distinct()
	print("Comment",cmmt1)
	for ec in cmmt1:
		print("Yuck",ec.comment)

	cmmts=[]
	# for i in cmmt:
	# 	print(i.comment)
	# for i in cmmt:
	# 	cmmts.extend([(i.name, i.comment)])
	# print(cmmts)
	# cp = Photocrop.objects.filter(category_id=cid,mobile_id=mid)
	context={
		'mid':mid,
		'cid':cid,
		'name':name,
		'cate':cate,
		'samsung': samsung,
        # 'photo1':photo1,
		# 'photo2':photo2,
		'photo':ph,
		# 'testing': ph,
		'form':form,
		"com_list": strData,	
		'cmmt':cmmt1,
		# 'cp':cp
    }
	
	return render(request,'main/editor.html',context)

def cropedimages(request,mid,cid):
	cp = Photocrop.objects.filter(category_id=cid,mobile_id=mid)
	name=Mobile.objects.get(id=mid)
	cate=Category.objects.get(id=cid)
	context={
		'name':name,
		'cate':cate,
		"cp": cp
	}
	return render(request,'main/cropedimages.html',context)
def save_temp_profile_image_from_base64String(imageString, id):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "\\" + str(id)):
			os.mkdir(settings.TEMP + "\\" + str(id))
		url = os.path.join(settings.TEMP + "\\" + str(id),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, id)
	return None
def photocrop(request,mid,cid,*args, **kwargs):
	global imgc
	global photoc
	imgc = request.POST.get('selectedimage')
	print("img",imgc)
	photoc=Photo.objects.filter(pk=imgc,category_id=cid,mobile_id=mid)
	print(photoc,"photoc")
	context={
		'mid':mid,
		'cid':cid,
        'photo':photoc 
    }
	urls,temp=[],[]
	if len(photoc)>0:
		for ph in photoc:
			urls.append(ph.image.url)
		temp=urls[0]
		print("urls[0]",urls[0])
	else:
		
		print("else")
	s=temp[1:]
	print(s)
	rimg = cv2.imread(str(s))
	print(rimg,"rimggggggg")
	with open(str(s), "rb") as img_file:
		imageString = base64.b64encode(img_file.read())			# print(my_string)
	url = save_temp_profile_image_from_base64String(imageString, imgc)
	print(url)
	if request.method == "POST":
			cropX = request.POST.get("x_axis")
			cropY = request.POST.get("y_axis")
			cropWidth = request.POST.get("img_width")
			cropHeight = request.POST.get("img_height")
			if cropX == None:
				cropX='0'
			if cropY == None:
				cropY='0'
			if cropWidth == None:
				cropWidth='0'
			if cropHeight == None:
				cropHeight='0'
			if float(cropX) < 0 or cropX==None:
				cropX = 0
			if float(cropY) < 0 or cropX==None: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			x=int(float(str(cropX)))
			y=int(float(str(cropY)))
			h=int(float(str(cropHeight)))
			w=int(float(str(cropWidth)))
			print(x,y,w,h)
			# crop_img = rimg[y:y+h, x:x+w]
			# print("crop image",crop_img)
			# cv2.imwrite(url, crop_img)
		# res= Photocrop.objects.create(mobile=mid,category=cid,photo=img,cimage=)
		# crop_img = img[y:y+h, x:x+w]
		# cv2.imshow(url, crop_img)
		# cv2.waitKey(0)
		# crop_img = img[int(cropY):int(cropY)+int(cropHeight), int(cropX):int(cropX)+int(cropWidth)]
		# print(crop_img)
		# print(crop_img)
		# with open("my_image.jpg", "rb") as img_file:
		# 	my_string = base64.b64encode(img_file.read())
		# print(my_string)	

		# cv2.imwrite(url, crop_img)
	return render(request,'main/photocrop.html',context)
def photocropsave(request,mid,cid):
	global imgc
	global photoc
	print("pic",photoc)
	urls,temp=[],[]
	print(photoc)
	print("after photo")
	if len(photoc)>0:
		for ph in photoc:
			urls.append(ph.image.url)
		temp=urls[0]
		print("urls[0]",urls[0])
	else:
		
		print("else")
	s=temp[1:]
	print(s)
	rimg = cv2.imread(str(s))
	print(rimg)
	with open(str(s), "rb") as img_file:
		imageString = base64.b64encode(img_file.read())			# print(my_string)
	url = save_temp_profile_image_from_base64String(imageString, imgc)
	print(url)
	if request.method == "POST":
			cropX = request.POST.get("x_axis")
			cropY = request.POST.get("y_axis")
			cropWidth = request.POST.get("img_width")
			cropHeight = request.POST.get("img_height")
			if cropX == None:
				cropX='0'
			if cropY == None:
				cropY='0'
			if cropWidth == None:
				cropWidth='0'
			if cropHeight == None:
				cropHeight='0'
			if float(cropX) < 0 or cropX==None:
				cropX = 0
			if float(cropY) < 0 or cropX==None: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			x=int(float(str(cropX)))
			y=int(float(str(cropY)))
			h=int(float(str(cropHeight)))
			w=int(float(str(cropWidth)))
			print(x,y,w,h)
			crop_img = rimg[y:y+h, x:x+w]
			print("crop image",crop_img)
			# cv2.imwrite(url, crop_img)
		# res= Photocrop.objects.create(mobile=mid,category=cid,photo=img,cimage=)
		# crop_img = img[y:y+h, x:x+w]
		# cv2.imshow(url, crop_img)
		# cv2.waitKey(0)
		# crop_img = img[int(cropY):int(cropY)+int(cropHeight), int(cropX):int(cropX)+int(cropWidth)]
		# print(crop_img)
		# print(crop_img)
		# with open("my_image.jpg", "rb") as img_file:
		# 	my_string = base64.b64encode(img_file.read())
		# print(my_string)	
			for i in photoc:
				print(i.id," instance")
			cv2.imwrite(url, crop_img)
			pc=Photocrop()
			for i in photoc:
				pc.photo= i
			mob=Mobile.objects.filter(pk=mid)
			cat=Category.objects.filter(pk=cid)
			print(mob)
			print(cat)
			for i in mob:
				pc.mobile=i
			
			for i in cat:
				pc.category=i
			
			# pc.mobile=mob
			# pc.category=cid
			pc.cimage= files.File(open(url,'rb'))
			pc.save()
			# Photocrop.cimage.save("",files.File(open(url,'rb')))
			context ={
		'cid':cid,
		'mid':mid
	}
			
	return redirect('main:cropedimages',mid,cid)
	return render(request,'croppedimages.html')
def report(request,mid):
	data= Photo.objects.filter(mobile_id=mid)
	cats = Category.objects.filter(mobile_id =mid)
	l=[]
	for i in data:
		l.append(i.cname)
	print(l)
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


# Create Superuser
# user = User.objects.create_superuser(username='')
# user.username = ''
# user.first_name = ''
# user.last_name = ''
# user.email = ''
# user.set_password("")
# user.is_active = True
# user.is_staff = True
# user.is_superuser = True
# user.save()
