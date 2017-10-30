# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from RLGJ.models import ZzfkjVisit
from django.views.decorators.cache import cache_control, never_cache
import json
import math
import numpy as np
import cv2
import os
import time
import face_recognition


# Create your views here.

def OnCompare(request):
    data = json.loads(request.body)
    src_frame = np.array(data['img'])
    cv2.imwrite('./static/tmp.jpg', src_frame)
    src_img = face_recognition.load_image_file('./static/tmp.jpg')
    src_face_encoding = face_recognition.face_encodings(src_img)[0]
    all_list = ZzfkjVisit.objects.all()

    for person in all_list: 
        # Load the jpg files into numpy arrays
        tgt_image = face_recognition.load_image_file(person.idcardimg)
        tgt_face_encoding = face_recognition.face_encodings(tgt_image)[0]

        results = face_recognition.compare_faces([tgt_face_encoding], src_face_encoding)
        if results[0]:
            return HttpResponse('True')
    return HttpResponse('False')

def OnAdd(request):
    try:
        data = json.loads(request.body)
        new_name = data['name']
        new_idcard = data['id']
        frame = data['img']
        save_dir = './static/'+new_idcard
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        idcardImg = './static/'+new_idcard+'/'+now+'.jpg'
        cv2.imwrite(idcardImg, np.array(frame))
        
        try:
            ZzfkjVisit.objects.create(name=new_name, idcard=new_idcard, idcardimg=idcardImg)
            return HttpResponse('数据库更新成功！')
        except:
            return HttpResponse("数据库更新失败！")
    except:
        return HttpResponse('数据传输失败！')

@never_cache
def OnMessage(request):
    try:
        currpage = int(request.GET['currpage'])
        num_perpage = 5
        img = []
        try:
            query_name = request.GET['name']
            if query_name == 'null':
                all_list = ZzfkjVisit.objects.all()
            elif len(query_name)==18:
                all_list = ZzfkjVisit.objects.filter(idcard__contains=query_name)
            else:
                all_list = ZzfkjVisit.objects.filter(name__contains=query_name)
        except:
            all_list = ZzfkjVisit.objects.all()
           
        totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
        if currpage != totalpage:
            ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
        else:
            ID_list = all_list[(currpage-1)*num_perpage:]
        
        for ID in ID_list:
            ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
            img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard})
        c = {"currpage":currpage, 'totalpage':totalpage, "img":img}
        return HttpResponse(json.dumps(c), content_type="application/json")
    except:
        t = loader.get_template('OnMessage.html')
        c = {}
        return HttpResponse(t.render(c))
    
@never_cache
def OnDelete(request):
    try:
        try:
            delete_id = request.GET['id']
            delete_img = ZzfkjVisit.objects.get(id=delete_id)
            delete_dir = delete_img.idcardimg
            os.remove(delete_dir)
            delete_img.delete()
            return HttpResponse("delete success")
        except:
            currpage = int(request.GET['currpage'])
            num_perpage = 5
            img = []
            try:
                query_name = request.GET['name']
                if query_name == 'null':
                    all_list = ZzfkjVisit.objects.all()
                elif len(query_name)==18:
                    all_list = ZzfkjVisit.objects.filter(idcard__contains=query_name)
                else:
                    all_list = ZzfkjVisit.objects.filter(name__contains=query_name)
            except:
                all_list = ZzfkjVisit.objects.all()
           
            totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
            if currpage != totalpage:
                ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
            else:
                ID_list = all_list[(currpage-1)*num_perpage:]
        
            for ID in ID_list:
                ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
                img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard, 'id':ID.id})
            c = {"currpage":currpage, 'totalpage':totalpage, "img":img}
            return HttpResponse(json.dumps(c), content_type="application/json")
    except:
        t = loader.get_template('delete.html')
        c = {}
        return HttpResponse(t.render(c))

