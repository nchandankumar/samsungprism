import imp
from inspect import getcomments
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
		if len(data)<=10:
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
	global data	
	message=""	
	strData = ", ".join(str(v) for v in data)
	print(strData,"strdata++++++++++++++++++++++++")
	ph = []
	name=Mobile.objects.get(id=mid)
	cate=Category.objects.get(id=cid)

	for i in range(len(data)):
		ph.append(Photo.objects.get(category_id=cid,mobile_id=mid,id=int(data[i])))
	
	samsung=Photo.objects.filter(cname='samsung',category_id=cid,mobile_id=mid)
	
	if request.method == 'POST':
		n = request.POST.get('name')
		complist = request.POST.get('complist')
		cmt = request.POST.get('comment')
		res=Comments.objects.create(mobile=name,category=cate,name=n,comment=cmt, compList = complist)
		if res:
			message='Thank You for the comment'
		else:
			message='No Comment posted'
	form = CommentForm()
	cmmt = Comments.objects.filter(category_id=cid,mobile_id=mid)

	PH_IDs = []
	for eachObj in ph:
		PH_IDs.append(str(eachObj.id))
	print(list(map(int, mid)))
	# print(list(map(int, cid.split(" "))))
	# PH_ID_MID_CID = list(map(int, mid)) + list(map(int, cid)) + PH_IDs
	temp1=[]
	temp1.append(int(mid))
	temp2=[]
	temp2.append(int(cid))
	
	PH_ID_MID_CID = temp1 + temp2 + PH_IDs
	print(PH_ID_MID_CID)
	x=0
	print(x,"xxxxxxxxxx")

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
		'cmmt':cmmt,
		"PH_ID_MID_CID":PH_ID_MID_CID,
		"message":message,
		'x':x
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
def photoHighlight(request,mid,cid):
	img = request.POST.get('selectedimage')
	print("img",imgc)
	photoc=Photo.objects.filter(pk=img,category_id=cid,mobile_id=mid)
	print(photoc,"photoc")
	context={	
		'mid':mid,
		'cid':cid,
        'photo':photoc 
    }
	return render(request,'main/photohighlight.html',context)
# def report(request,mid):
# 	data= Photo.objects.filter(mobile_id=mid)
# 	cats = Category.objects.filter(mobile_id =mid)

# 	print("Catergory =", cats)
# 	cmmt=[]
# 	for i in cats:
# 		print(i)
# 		c=Comments.objects.filter(mobile_id=mid,category_id=i.id)
# 		cmmt.append(c)
# 	print("Comments =", cmmt[0][0].comment)
# 	cmmt = ["Hi", "Hello"]
# 	l=[]
# 	for i in data:
# 		l.append(i.cname)
# 	context ={
# 		'cname':set(l),
# 		'data':data,
# 		'cats': cats,
# 		'cmmt':cmmt
# 	}
# 	return render(request,'main/report.html',context)

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

def report(request,mid):
  data= Photo.objects.filter(mobile_id=mid)
  cats = Category.objects.filter(mobile_id =mid)
  # comm=Comments.objects.filter(mobile_id=mid)
  l,allcomm,comm,cids,catids,comlist	=[],[],[],[],[],[]
  for i in cats:
    c=Comments.objects.filter(mobile_id=mid,category_id=i.id)
    allcomm.append(c)
  for i in allcomm:
    b,cd,cl=[],[],[]
    for j in i:
      b.append(j)
      cd.append(j.category)
      x=j.compList
      x=list(map(int,x.split(", ")))
      print(x,end="-----")
      # print(j.compList,end="**")
      cl.append(x)
    comm.append(b)
    cids.append(cd)
    comlist.append(cl)
  
  for i in cids:
    for j in i:
      catids.append(j.id)

  # print(*comm)
  temp=zip(comm,comlist)
  for i,j in temp:
    print(*i)
    print(*j)
  
  catcom=zip(cats,comm,catids,comlist)  
  for i in data:
    l.append(i.cname)
  print(l)
  context ={
    'cname':set(l),
    'data':data,
    'cats': cats,
    'comm':comm,
    'cc':catcom,
    'mid':mid,
    'comlist':comlist,
    'catids':catids
    # 'cids':cids
  }
  return render(request,'main/report.html',context)

	