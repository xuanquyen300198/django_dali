# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
import pandas as pd
import xlwt
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import openpyxl
from io import BytesIO
from django import db
from uploadexcel.models import table_color_fomat
from uploadexcel.models import table_color_tmp
from io import StringIO
import sqlalchemy as sa
# library of img
import cv2
from PIL import Image
import imutils
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import urllib, mimetypes
from wsgiref.util import FileWrapper
from django.http import JsonResponse
# Login
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required 
from .form import CreateUserForm
# Create your views here.

def rgb_of_pixel(img_path, x, y):
    
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

def rgb2hex(r, g, b):
    # return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

@login_required(login_url='login')
def home(request):
    user = request.user
    if request.method == 'POST':
        if 'download_excel' in request.POST:
            # download
            file_path_excel = settings.MEDIA_ROOT +'/'+ "bangMau.xlsx"
            with open(file_path_excel, 'rb') as model_excel:
                result = model_excel.read()
            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=bangMau.xlsx'
            return response
        if 'upload_excel-btn' in request.POST:
            # download
            file_path_excel = settings.MEDIA_ROOT +'/'+ "bangMau.xlsx"
            with open(file_path_excel, 'rb') as model_excel:
                result = model_excel.read()
            response = HttpResponse(result)
            response['Content-Disposition'] = 'attachment; filename=bangMau.xlsx'
            return response
        if  'download_image' in request.POST:
            # download
            file_path = settings.MEDIA_ROOT +'/'+ "result_img.jpg"
            file_wrapper = FileWrapper(open(file_path,'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype )
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % "result_img.jpg"
            return response
    return render(request,'pages/home.html', {"user":user})
def read_data(dataDb,dataIn):
    if len(dataDb) > 0:
        pdConCat = pd.concat([dataDb, dataIn],ignore_index=True)
        return pdConCat
    else :  
        return dataIn

@login_required(login_url='login')
def postImg(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        imgPath = request.FILES['import_img']
        fs = FileSystemStorage()
        filename = fs.save(imgPath.name, imgPath)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url !=None:
            # default
            width=780
            height=420
            y1=0
            y2=420
            x1=580
            x2=780
            img=cv2.imread("."+str(uploaded_file_url))
            (h,w,d) = img.shape
            scaleW = (round(w/780, 3))
            scaleH = (round(h/420, 3))
            scaleDe = 1
            tbc =  1
            if w < 780:
                width=420
                height=780
                y1=0
                y2=780
                x1=220
                x2=420
                scaleW = (round(w/420, 3))
                scaleH = (round(h/780, 3))
            if scaleW > scaleH:
                tbc = round((scaleW-scaleH)/2,3)
                scaleDe = scaleH + tbc
            else:
                tbc = round((scaleH-scaleW)/2,3)
                scaleDe = scaleW + tbc
            img = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255,255,255])  
            img=cv2.resize(img,(width,height)) #resize image            
            roi = img[y1:y2, x1:x2] #region of interest i.e where the rectangles will be
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) #convert roi into gray
            #Blur=cv2.GaussianBlur(gray,(5,5),1) #apply blur to roi
            Canny=cv2.Canny(img,10,50) #apply canny to roi
            #Find my contours
            contours =cv2.findContours(Canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

            cntrRect = []
            for i in contours:
                    epsilon = 0.05*cv2.arcLength(i,True)
                    approx = cv2.approxPolyDP(i,epsilon,True)
                    if len(approx) == 4:                       
                        if cv2.contourArea(i) > 300*scaleDe:
                            M = cv2.moments(i)
                            if M["m00"] != 0:
                                cX = int((M["m10"] / M["m00"]) )
                                cY = int((M["m01"] / M["m00"]) )     
                                (b,r,g) = rgb_of_pixel("."+str(uploaded_file_url),int(int(cX)*scaleW),int(int(cY)*scaleH))                        
                                
                                listHexDali = table_color_fomat.objects.filter(code_hex=rgb2hex(b,r,g).upper()).order_by('number_img').last()
                                if listHexDali !=None:
                                    code_dali = listHexDali.code_dali
                                else:
                                    code_dali = rgb2hex(b,r,g)
                                cv2.putText(img, str(code_dali), (cX + 35, cY+8),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            # save into store
            img2 = cv2.copyMakeBorder(img, 40, 40, 40,40, cv2.BORDER_CONSTANT, value=[255,255,255])  
            cv2.imwrite('./media/result_img.jpg', img2)
            # delete img into media
            if fs.exists(imgPath.name):
                os.remove(os.path.join(settings.MEDIA_ROOT, imgPath.name)) 
            return JsonResponse({"data": "0000"}, status=200)
        return JsonResponse({"data": "1111"}, status=400)
    else:
        # some form errors occured.
        return JsonResponse({"data": "1111"}, status=400)

    # some error occured
    return JsonResponse({"data": "1111"})

@login_required(login_url='login')
def postExcel(request):
    if request.is_ajax and request.method == "POST":
        # dataset = Dataset()
        new_dataLst = request.FILES['import_excle']
        # imported_data = dataset.load(new_dataLst.read(),format='xlsx')
        dfIn = pd.read_excel(new_dataLst)
        # change column
        old_names = dfIn.columns
        new_names = ['code_dali', 'code_hex', 'color', 'code_img',]
        dfIn.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        dfIn.drop('color', axis=1, inplace=True)
        tmp_list = table_color_tmp.objects.all()
        pdTmp = pd.DataFrame([x.as_dict() for x in tmp_list])
        df = read_data(pdTmp,dfIn)

        # output = StringIO()
        # df.to_csv(output, sep=';', header=False, index=False, columns=df.columns)
        # output.getvalue()
        # # jump to start of stream
        # output.seek(0)
        # engine = sa.create_engine("django.db.backends.sqlite3")
        # # Insert df into postgre
        # connection = engine.raw_connection()
        # with connection.cursor() as cursor:
        #     cursor.copy_from(output, "table_color_tmp", sep=';', null="NULL", columns=(df.columns))
        #     connection.commit()

        df = df.drop_duplicates( subset = ['code_dali', 'code_img','code_img'], keep = 'last').reset_index(drop = True) 

        # insert table tmp
        for itemImg in df.itertuples():
            itemImg = table_color_tmp.objects.create(
                code_hex=itemImg.code_hex,
                code_dali=itemImg.code_dali,
                code_img= itemImg.code_img
                )
            itemImg.save()

        # totalImg = len(df.groupby('code_img'))

        # filter rows group by code_hex and code_img
        daliData = df.groupby(['code_dali','code_img']).size().reset_index(name='count')
        # # count code_hex By code_img
        daliData['code_img'] = daliData.groupby('code_dali').transform('count')
        dataExport1=daliData.drop_duplicates('code_dali')
        dataExport1 = dataExport1.sort_values(by=['code_img'], ascending=False)
        dataExport1.drop('count', axis=1, inplace=True)
        
        
        # filter rows group by code_hex and code_dali
        hexDaliData = df.groupby(['code_hex','code_dali']).size().reset_index(name='count')
        # join hexDaliData dataExport1
        dataExport2 = pd.merge(hexDaliData, dataExport1, how="left", on=["code_dali", "code_dali"])
        # dataExport2['countImg'] = dataExport2['code_img'].map(lambda a: format((a / float(totalImg))*100, '.2f') + "%")
        dataExport2.drop('count', axis=1, inplace=True)
        # delete 
        table_color_fomat.objects.all().delete()
        # insert table format
        for itemImg in dataExport2.itertuples():
            itemImg = table_color_fomat.objects.create(
                code_hex=itemImg.code_hex,
                code_dali=itemImg.code_dali,
                number_img= itemImg.code_img
                )
            itemImg.save()
        # rename to export
        old_names1 = dataExport1.columns
        new_names1 = ['mã màu dali', 'số ảnh']
        dataExport1.rename(columns=dict(zip(old_names1, new_names1)), inplace=True)
        dataExport1.reset_index(drop=True, inplace=True)
        old_names2 = dataExport2.columns
        new_names2 = ['mã màu hex', 'số màu dali','số ảnh']
        dataExport2.rename(columns=dict(zip(old_names2, new_names2)), inplace=True)
        dataExport2.reset_index(drop=True, inplace=True)
        # export excel
        with pd.ExcelWriter('./media/bangMau.xlsx') as writer:  
            dataExport1.to_excel(writer, sheet_name='Sheet1')
            dataExport2.to_excel(writer, sheet_name='Sheet2')
        return JsonResponse({"data": "0000"})
    else:
        # some form errors occured.
        return JsonResponse({"data": "1111"}, status=400)

    # some error occured
    return JsonResponse({"data": "1111"})

def loginPage(request):
    if  'login' in request.POST:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            if request.method == 'POST':
                username = request.POST.get('username')
                password =request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Tài khoản hoặc mật khẩu không chính xác !')

            context = {}
            return render(request, 'pages/login.html', context)
    return render(request, 'pages/login.html')
def logoutUser(request):
	logout(request)
	return redirect('login')

def registerPage(request):
	if  request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')
			
		context = {'form':form}
		return render(request, 'pages/register.html', context)