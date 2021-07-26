from django.shortcuts import redirect, render, HttpResponse
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import default_storage
import pyrebase
from pyrebase.pyrebase import Storage
from home.ignorethis.firebasedetails import firebasedetails
import json
import pandas
import smtplib

def mail_func(rec, msg):
    sender = "cfgteam19@gmail.com"
    password = "Rootuser@2021"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, rec, msg)
    print("done")

firebaseConfig = firebasedetails()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()
passing = {}
context1 = []
context2 = []
# skills = ""
# # # Create your views here.
# # def index(request):
# #     return render(request,'index1.html')

def index(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        try:
            if role== 'Volunteer':
                context1 = []
                auth.sign_in_with_email_and_password(username,password)
                users = db.child('Volunteers').order_by_child('firstname').get()
                for person in users.each():
                    if person.val()['email'] == username:
                        context1.append( 
                            {"name": person.val()['firstname'],
                            "email": person.val()['email'],
                            "image": person.val()['image'],
                            "contact": person.val()['contact'],
                            "interests": person.val()['interests'],
                            }
                        )
                        global skills
                        skills = person.val()['interests']
                passing = {'context': context1 }
                return render(request,'user.html',passing)

            elif role=='Corporate':
                context = []
                auth.sign_in_with_email_and_password(username,password)
                users = db.child('Corporates').order_by_child('name').get()
                for person in users.each():
                    if person.val()['email'] == username:
                        context.append( 
                            {"name": person.val()['name'],
                            "email": person.val()['email'],
                            "contact": person.val()['contact'],
                            "interests": person.val()['interests'],
                            }
                        )
                passing = {'context': context }
                return render(request,'user.html',passing)


            elif role=='NGO':
                context2 = []
                auth.sign_in_with_email_and_password(username,password)
                users = db.child('Ngos').order_by_child('name').get()
                for person in users.each():
                    if person.val()['email'] == username:
                        context2.append( 
                            {"name": person.val()['name'],
                            "email": person.val()['email'],
                            "contact": person.val()['contact'],
                            "interests": person.val()['interests'],
                            }
                        )
                passing = {'context': context2 }
                return render(request,'ngo_myProfile.html',passing)

            elif role=='Admin':
                auth.sign_in_with_email_and_password(username,password)
                return render(request, 'adminPortal.html')
        
        except Exception as e:
            print(e)
            return render(request, 'index.html')

            
    return render(request, 'index.html')


def registervol(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        location = request.POST.get('location')
        availability = request.POST.get('availability')
        linkedin = request.POST.get('linkedin')
        interests = request.POST.get('Interests')
        password = request.POST.get('password')
        SchoolID = request.POST.get('SchoolID')
        corporation = request.POST.get('corporation')
        WorkEmail = request.POST.get('WorkEmail')
        if len(request.FILES) != 0:
            image = request.FILES['image']
            image_save = default_storage.save(image.name, image)
            storage.child(contact).put("static/images/" + image.name) 
            delete = default_storage.delete(image.name)
            fileURL = storage.child(contact).get_url(None)
        
        data = {
            'firstname':firstname,
            'lastname': lastname, 
            'email':email,
            'contact':contact,
            'image':fileURL,
            'gender':gender,
            'birthday':birthday,
            'location':location,
            'availability': availability,
            'linkedin':linkedin,
            'interests': interests,
            }
        db.child('Volunteers').child(contact).set(data)
        auth.create_user_with_email_and_password(email,password)
        messages.success(request, 'Your message has been sent!')
        return redirect('/')

    return render(request,'registerVolunteer.html')


def registerngo(request):
    if request.method == "POST":
        name = request.POST.get('name')
        website = request.POST.get('website')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        year = request.POST.get('year')
        about = request.POST.get('about')
        interests = request.POST.get('Interests')
        role = request.POST.get('role')
        password = request.POST.get('password')
        data = {
            'name':name,
            'email':email,
            'contact':contact,
            'website':website,
            'year':year,
            'about':about,
            'interests':interests,
            }
        if role == 'corporate':
            db.child('Corporates').child(contact).set(data)
        elif role == 'ngo':
            db.child('Ngos').child(contact).set(data)
        auth.create_user_with_email_and_password(email,password)
        messages.success(request, 'Your message has been sent!')
        return redirect('/')

    return render(request,'registration-ngo.html')


def plotgraph(request):
    people = db.child('Volunteers').order_by_child('location').get()
    try:
        for person in people.each():
            print(person)
    except:
        print('error')

    return redirect('/')


def plots():
    a = []
    data = db.child('Volunteers').get()
    for key, value in data.val().items():
        element = value['location']
        a.append(element.lower())
    freq = {}
    for item in a:
        if(item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    print(freq)
    json_object = json.dumps(freq, indent=2)
    print(json_object)


plots()


def home(request):
    people = []
    users = db.child('Ngos').order_by_child('name').get()
    try:
        for person in users.each():
            if person.val()['interests'] == skills:
                people.append( 
                                {"name": person.val()['name'],
                                "email": person.val()['email'],
                                "contact": person.val()['contact'],
                                "interests": person.val()['interests'],
                                }
                            )
    except:
        people = []
    passing = {'people': people }
    print(skills)
    print(people)
    return render(request,'home.html',passing)


def homengo(request):
    if request.method == "POST":
        msg = request.POST.get('msg')
        skills = request.POST.get('skills')

        people = []
        users = db.child('Volunteers').order_by_child('firstname').get()
        try:
            for person in users.each():
                if person.val()['interests'] == skills:
                    try:
                        mail_func(person.val()['email'],msg)
                        print('mail sent')
                    except:
                        print('mail not sent')
        except:
            print('no emails') 

    return render(request,'index.html')

#Adding other required HTML files

def charts_view(request):
    return render(request, 'charts.html')

def corporate_view(request):
    return render(request, 'corporate.html')

def ngoAnalysis_view(request):
    return render(request, 'ngoAnalysis.html')

def tables_view(request):
    return render(request, 'tables.html')


def home_user(request):
    return render(request, 'home_user.html')


