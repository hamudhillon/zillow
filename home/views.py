from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from home.models import Clans
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from home.zillow_ui import zillow_get

from sendgrid.helpers.mail import *
import sendgrid
SENDGRID_API = "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"
FROM_EMAIL = 'deepak.dhanjal12@gmail.com'
FROM_NAME = 'Pubg'




def sendEmail( to_email, email_content):
    try:
        connection = sendgrid.SendGridAPIClient(api_key=SENDGRID_API)
        mail = Mail()
        mail.from_email = Email(FROM_EMAIL, FROM_NAME)
        personalization = Personalization()
        personalization.add_to(Email(to_email))
        mail.add_personalization(personalization)
        mail.subject = "Pubg by Dhanjal"
        
        mail.add_content(Content("text/html", email_content))
        send_mail = connection.send(mail)
        print(send_mail)

    except:
        print('Errr')

def getemailcontent():
    filepath = 'room.html'
    filecnt = open(filepath, 'r')
    emailcontent = filecnt.read()
    
    room_id = '2365566'
    emailcontent = emailcontent.replace('{{roomid}}', room_id)
    # print(emailcontent)
    return emailcontent






def postblog(request):
    msg = None
    if request.method=='POST':
        obj_blog = Clans()
        obj_blog.user_id = request.user.id
        obj_blog.title = request.POST.get("txt_title")
        obj_blog.description = request.POST.get("txt_desc")
        obj_blog.save()
        msg = "Data Saved Successfully"
    return render(request, 'blogpost.html' ,{"msg1":msg})


# @login_required(login_url='/login/')
def all_users(request):
    if request.method=='GET':
        print(request.method)
        obj_blogsall = Clans.objects.all()
        print(obj_blogsall)
    return render(request,'allblogs.html', {'blogs_all':obj_blogsall})


def all_clans(request):
    if request.method=='GET':
        print(request.method)
        obj_blogsall = User.objects.all()
        print(obj_blogsall)
    return render(request,'allblogs.html', {'blogs_all':obj_blogsall})


# @login_required(login_url='/login/')
def update_blogger(request):
    msg = None
    if request.method == 'GET':
        blog_id = request.GET.get('id')

        print(blog_id)
        objblog = Clans.objects.get(pk=int(blog_id))

    if request.method == 'POST':
        blog_id = request.POST.get('hdn_id')
        objblog = Clans.objects.get(pk = int(blog_id))
        objblog.title = request.POST.get("txt_title")
        objblog.description = request.POST.get("txt_desc")
        objblog.save()
        msg = 'Data Updated Successfully'
    return render(request,"updateblog.html",{"msg1":msg,"objblg":objblog})

def SendRoom_ID(request):
    msg = None
    if request.method == 'GET':
        blog_id = request.GET.get('id')
        objblog = Clans.objects.get(pk=int(blog_id))

    if request.method == 'POST':
        blog_id = request.POST.get('hdn_id')
        objblog = Clans.objects.get(pk = int(blog_id))
        objblog.roomid = request.POST.get("txt_room")

        obj = request.POST.get("txt_room")
        print(obj)

        objblog.save()

        to_email = objblog.user.email
        print(to_email)
        email = getemailcontent()
        sendEmail(to_email, email)
        msg = 'Data Updated Successfully'
    return render(request,"sendroom.html",{"msg1":msg,"objblg":objblog})



def UploadSourceFile(request):
    msg = None
    objblog = None
    return render(request,"profile.html",{"objblg":objblog})

def ProcessCsvFiles(request):
    
    print('Hreee')
    data = {}
    print(request.method)
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed with processing
    try:
        csv_file = request.FILES["csv_file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponse('Csv Error')
    #if file is too large, return message
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponse('Csv Error')
        
        
        try:
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split(" ")
            for line in lines:
                print(line)
                import json
                data=zillow_get(line)
                # print(type(data))
                print(data)
            return HttpResponse(data)
            
        except:
            return HttpResponse('Error')

    except:
        return HttpResponse('Error')


def ProfileViewer(request):
    msg = None
    if request.method == 'GET':
        blog_id = request.GET.get('id')
        objblog = Clans.objects.get(pk=int(blog_id))

        msg = 'Data Updated Successfully'
    return render(request,"profile.html",{"msg1":msg,"objblg":objblog})



@login_required(login_url='/login/')
def delid(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        objS  = Clans.objects.get(pk=int(id))
        objS.delete()
    return HttpResponseRedirect('/list/')


def register(request):

    try:
        msg = None
        if request.method=="POST":
            password = request.POST.get('txt_password')
            retype_password = request.POST.get('txt_password2')
            print(password)
            print(request.POST.get('txt_username'))
            Email = request.POST.get('txt_email')
            usern = request.POST.get('txt_email')

            objusr = User()
            objusr.username = request.POST.get('txt_username')
            objusr.first_name = request.POST.get('txt_username')
            objusr.email = request.POST.get('txt_email')

            payment = request.POST.get('txt_payment')
            clan = request.POST.get('txt_clan')
            phone_num = request.POST.get('txt_phone')

            if len(phone_num)==0:
                msg = 'Phone is Required'

            elif len(clan)==0:
                msg = 'Clan Name is Required'

            clan_exists = Clans.objects.filter(name =clan).count()
            if clan_exists>0:
                msg = 'Clan Already exists'

            user_exists = User.objects.filter(email =Email).count()
            if user_exists>0:
                msg = 'Email Already exists'

            username_exists = User.objects.filter(username =usern).count()
            if username_exists>0:
                msg = 'Username Already exists'
                
            elif password!=retype_password:
                msg = 'Password Didnt Match'

            elif '@' not in Email:
                msg = 'Invalid Email!'

            elif payment !='100':
                msg = 'Please Pay 100INR to Join'

            listcount = User.objects.count()
            if listcount>25:
                msg = 'Limit Exceded For The Day'
                
            objusr.set_password(password)
            objusr.date_joined = datetime.now()
            objusr.is_active= True
            objusr.is_superuser=False
            objusr.is_staff= False
            objusr.save()

            obj_clan = Clans()
            obj_clan.user = objusr
            obj_clan.name = clan
            obj_clan.phone = request.POST.get('txt_phone')
            obj_clan.payment = payment
            obj_clan.save()

    except:
        return HttpResponse('Internal Server Error')
        

    return render(request,'register.html',{"msg1":msg})


def login1(request):
    msg= None
    if request.method=="POST":
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        objuser = authenticate(username = username, password= password)
        if objuser is not None:
            if objuser.is_active:
                login(request,objuser)
                return HttpResponseRedirect('/postblog/')
        else:
            msg = 'Wrong Password'
    return render(request,'login.html',{"msg1":msg})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

