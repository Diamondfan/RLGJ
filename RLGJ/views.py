# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from RLGJ.models import ZzfkjVisit, Kaqin
from django.views.decorators.cache import cache_control, never_cache
import json
import math
import numpy as np
import cv2
import os
import time
import datetime
import face_recognition


# Create your views here.

def OnCompare(request):
    data = json.loads(request.body)
    src_frame = np.array(data['img'])
    cv2.imwrite('./static/tmp.jpg', src_frame)
    src_img = face_recognition.load_image_file('./static/tmp.jpg')
    src_face_encoding = face_recognition.face_encodings(src_img)[0]
    
    kaoqin_list = ZzfkjVisit.objects.filter(state=1)

    for person in kaoqin_list: 
        # Load the jpg files into numpy arrays
        tgt_image = face_recognition.load_image_file(person.idcardimg)
        tgt_face_encoding = face_recognition.face_encodings(tgt_image)[0]

        results = face_recognition.compare_faces([tgt_face_encoding], src_face_encoding, tolerance=0.6)
        if results[0]:
            passtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            Kaqin.objects.create(idcard=person.idcard, passtime=passtime)
            return HttpResponse(person.name)

    menjin_list = ZzfkjVisit.objects.filter(state=0)
    for person in menjin_list: 
        # Load the jpg files into numpy arrays
        tgt_image = face_recognition.load_image_file(person.idcardimg)
        tgt_face_encoding = face_recognition.face_encodings(tgt_image)[0]

        results = face_recognition.compare_faces([tgt_face_encoding], src_face_encoding, tolerance=0.6)
        if results[0]:
            return HttpResponse(person.name)
    return HttpResponse('False')

def OnAdd(request):
    #不加入考勤， state=0
    try:
        data = json.loads(request.body)
        new_name = data['name']
        new_idcard = data['id']
        frame = data['img']
        save_dir = 'static/'+new_idcard
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        timestamp = time.localtime(time.time())
        now = time.strftime('%Y%m%d_%H%M%S', timestamp)
        addtime = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
        idcardImg = os.path.join('static/', new_idcard, now+'.jpg')
        cv2.imwrite(idcardImg, np.array(frame))
        try:
            ZzfkjVisit.objects.create(name=new_name, idcard=new_idcard, idcardimg=idcardImg, state=0, isblacklist=0, addtime=addtime)
            return HttpResponse('门禁人脸库更新成功！')
        except:
            return HttpResponse("门禁人脸数据库更新失败！")
    except:
        return HttpResponse('数据传输失败！')

def OnAddOne(request):
    #不加入考勤， state=0
    try:
        data = json.loads(request.body)
        new_name = data['name']
        new_idcard = data['id']
        frame = data['img']
        save_dir = 'static/'+new_idcard
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        timestamp = time.localtime(time.time())
        now = time.strftime('%Y%m%d_%H%M%S', timestamp)
        addtime = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
        idcardImg = os.path.join('static/', new_idcard, now+'.jpg')
        cv2.imwrite(idcardImg, np.array(frame))
        
        try:
            ZzfkjVisit.objects.create(name=new_name, idcard=new_idcard, idcardimg=idcardImg, state=1, isblacklist=0, addtime=addtime)
            return HttpResponse('考勤数据库更新成功！')
        except:
            return HttpResponse("考勤数据库更新失败！")
    except:
        return HttpResponse('数据传输失败！')

@never_cache
def OnSelect(request):
    try:
        try:
            query_id = request.GET['id']
            query_time = request.GET['time']
            query_month, query_day, query_year = query_time.split('/')
            query_t = datetime.date(int(query_year), int(query_month), int(query_day))

            back_list = Kaqin.objects.filter(idcard__contains=query_id).filter(passtime__startswith=query_t)
            back_data = []
            for back in back_list:
                back_data.append({'id':back.idcard, 'passtime':str(back.passtime).split('+')[0]})
            c = {'data': back_data}
            return HttpResponse(json.dumps(c), content_type='application/json')
        except:
            currpage = int(request.GET['currpage'])
            num_perpage = 5
            img = []
            try:
                query_name = request.GET['name']
                if query_name == 'null':
                    all_list = ZzfkjVisit.objects.filter(state=1)
                elif len(query_name)==18:
                    all_list = ZzfkjVisit.objects.filter(state=1).filter(idcard__contains=query_name)
                else:
                    all_list = ZzfkjVisit.objects.filter(state=1).filter(name__contains=query_name)
            except:
                all_list = ZzfkjVisit.objects.filter(state=1)
           
            totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
            if currpage != totalpage:
                ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
            else:
                ID_list = all_list[(currpage-1)*num_perpage:]
        
            for ID in ID_list:
                ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
                img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard, 'addtime':str(ID.addtime).split('+')[0], 'status':ID.state})
            c = {"currpage":currpage, 'totalpage':totalpage, "img":img }
            return HttpResponse(json.dumps(c), content_type="application/json")
    except:
        t = loader.get_template('OnSelect.html')
        c = {}
        return HttpResponse(t.render(c))

@never_cache
def OnDeleteOne(request):
    try:
        try:
            delete_id = request.GET['id']
            delete_img = ZzfkjVisit.objects.get(id=delete_id)
            delete_dir = delete_img.idcardimg
            delete_idcard = delete_img.idcard
            delete_passtime = Kaqin.objects.filter(idcard__contains=delete_idcard)
            if os.path.exists(delete_dir):
                os.remove(delete_dir)
            delete_img.delete()
            for x in delete_passtime:
                x.delete()
            return HttpResponse("delete success")
        except:
            currpage = int(request.GET['currpage'])
            num_perpage = 5
            img = []
            try:
                query_name = request.GET['name']
                if query_name == 'null':
                    all_list = ZzfkjVisit.objects.filter(state=1)
                elif len(query_name)==18:
                    all_list = ZzfkjVisit.objects.filter(state=1).filter(idcard__contains=query_name)
                else:
                    all_list = ZzfkjVisit.objects.filter(state=1).filter(name__contains=query_name)
            except:
                all_list = ZzfkjVisit.objects.filter(state=1)
           
            totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
            if currpage != totalpage:
                ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
            else:
                ID_list = all_list[(currpage-1)*num_perpage:]
        
            for ID in ID_list:
                ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
                img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard, 'id':ID.id, 'addtime':str(ID.addtime).split('+')[0]})
            c = {"currpage":currpage, 'totalpage':totalpage, "img":img}
            return HttpResponse(json.dumps(c), content_type="application/json")
    except:
        t = loader.get_template('deleteOne.html')
        c = {}
        return HttpResponse(t.render(c))

@never_cache
def OnMessage(request):
    try:
        currpage = int(request.GET['currpage'])
        num_perpage = 5
        img = []
        try:
            query_name = request.GET['name']
            if query_name == 'null':
                all_list = ZzfkjVisit.objects.filter(state=0)
            elif len(query_name)==18:
                all_list = ZzfkjVisit.objects.filter(state=0).filter(idcard__contains=query_name)
            else:
                all_list = ZzfkjVisit.objects.filter(state=0).filter(name__contains=query_name)
        except:
            all_list = ZzfkjVisit.objects.filter(state=0)
           
        totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
        if currpage != totalpage:
            ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
        else:
            ID_list = all_list[(currpage-1)*num_perpage:]
        
        for ID in ID_list:
            ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
            img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard, 'addtime': str(ID.addtime).split('+')[0], 'status':ID.state})
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
            if os.path.exists(delete_dir):
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
                    all_list = ZzfkjVisit.objects.filter(state=0)
                elif len(query_name)==18:
                    all_list = ZzfkjVisit.objects.filter(state=0).filter(idcard__contains=query_name)
                else:
                    all_list = ZzfkjVisit.objects.filter(state=0).filter(name__contains=query_name)
            except:
                all_list = ZzfkjVisit.objects.filter(state=0)
           
            totalpage = int(math.ceil(float(len(all_list)) / num_perpage))
            if currpage != totalpage:
                ID_list = all_list[(currpage-1)*num_perpage:currpage*num_perpage]
            else:
                ID_list = all_list[(currpage-1)*num_perpage:]
        
            for ID in ID_list:
                ID.idcardimg = '/static/'+'/'.join(ID.idcardimg.split('/')[-2:])+'/'
                img.append({'img':ID.idcardimg, 'name':ID.name, 'id_card':ID.idcard, 'id':ID.id, 'addtime':str(ID.addtime).split('+')[0]})
            c = {"currpage":currpage, 'totalpage':totalpage, "img":img}
            return HttpResponse(json.dumps(c), content_type="application/json")
    except:
        t = loader.get_template('delete.html')
        c = {}
        return HttpResponse(t.render(c))


