from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
import razorpay
# Create your views here.
def login(request):
    return render(request,'login.html')

def login_post(request):
    user_name=request.POST['textfield']
    password=request.POST['textfield2']

    ob=login_table.objects.filter(username=user_name,password=password)
    if ob.exists():
        obb=login_table.objects.get(username=user_name,password=password)
        request.session['lid']=obb.id
        if obb.type=='admin':
            from django.contrib import auth
            ob1 = auth.authenticate(username='admin123', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            request.session['lid']=obb.id
            return HttpResponse('''<script>alert('welcome to admin page');window.location='/admin_page'</script>''')
        if obb.type=='user':
            from django.contrib import auth
            ob1 = auth.authenticate(username='admin123', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            request.session['lid'] = obb.id
            return HttpResponse('''<script>alert('welcome to user page');window.location='/user_page'</script>''')
        if obb.type=='worker':
            from django.contrib import auth
            ob1 = auth.authenticate(username='admin123', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            request.session['lid'] = obb.id
            return HttpResponse('''<script>alert('welcome to worker page');window.location='/worker_page'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/';</script>''')

    else:
         return HttpResponse('''<script>alert('Please enter username and password');window.location='/';</script>''')


@login_required(login_url='/')
def accept_worker(request,id):
    request.session['wid']=id
    ob=login_table.objects.get(id=id)
    ob.type='worker'
    ob.save()
    return HttpResponse('''<script>alert('accept successfully');window.location='/verify_worker';</script>''')


@login_required(login_url='/')
def reject_worker(request,id):
    request.session['wid']=id
    ob=login_table.objects.get(id=id)
    ob.type='reject'
    ob.save()
    return HttpResponse('''<script>alert('reject successfully');window.location='/verify_worker';</script>''')


@login_required(login_url='/')
def admin_page(request):
    return render(request,'admin/adminpage.html')


@login_required(login_url='/')
def verify_worker(request):
    ob=worker_table.objects.all()
    return render(request,'admin/verifyworker.html',{'value':ob})

@login_required(login_url='/')
def view_worker_rating(request):
    ob=rating_table.objects.all()
    return render(request,'admin/viewworkerrating.html',{'value':ob})

@login_required(login_url='/')
def view_complaint(request):
    ob=user_complaint_table.objects.all()
    return render(request,'admin/viewcom.html',{'value':ob})



@login_required(login_url='/')
def view_worker_details(request,id):
    request.session['wid']=id
    worker = user_complaint_table.objects.filter(
        request__skill__worker_id_id=id
    ).first()

    return render(request, 'admin/worker_details.html', {'worker': worker})



@login_required(login_url='/')
def admin_block_worker(request,id):
    request.session['wid']=id
    worker=worker_table.objects.get(id=request.session['wid'])
    worker.LOGIN.type = 'blocked'
    worker.LOGIN.save()

    return HttpResponse(
        "<script>alert('Worker blocked successfully');window.location='/view_complaint'</script>"
    )

@login_required(login_url='/')
def admin_unblock_worker(request,id):
    request.session['wid']=id
    worker=worker_table.objects.get(id=request.session['wid'])
    worker.LOGIN.type = 'worker'
    worker.LOGIN.save()

    return HttpResponse(
        "<script>alert('Worker unblocked successfully');window.location='/view_complaint'</script>"
    )

@login_required(login_url='/')
def send_reply(request,id):
    request.session['cid']=id
    ob=user_complaint_table.objects.get(id=id)
    return render(request,'admin/reply.html')

@login_required(login_url='/')
def send_reply_post(request):
    reply=request.POST['textarea']

    ob=user_complaint_table.objects.get(id=request.session['cid'])
    ob.reply=reply
    ob.save()
    return HttpResponse('''<script>alert('reply send successfully');window.location='/view_complaint'</script>''')


# ========================================


def worker_registration(request):
    return render(request,'worker/workerregpage.html')

def worker_registration_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield2']
    phoneno=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield5']
    pin=request.POST['textfield6']
    image=request.FILES['fileField']
    username=request.POST['textfield7']
    password=request.POST['textfield8']

    if login_table.objects.filter(username=username).exists():
        return HttpResponse(
            "<script>alert('Username already exists');window.location='/worker_registration';</script>"
        )

    from django.core.files.storage import FileSystemStorage
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type='pending'
    ob.save()


    obb=worker_table()
    obb.name=name
    obb.email=email
    obb.phoneno=phoneno
    obb.place=place
    obb.post=post
    obb.pin=pin
    obb.image=fp
    obb.LOGIN=ob
    obb.save()
    return HttpResponse('''<script>alert('worker register successfully');window.location='/';</script>''')

@login_required(login_url='/')
def worker_page(request):
    return render(request,'worker/workerpage.html')


@login_required(login_url='/')
def view_rating(request):
    ob=rating_table.objects.filter(request__skill__worker_id__LOGIN_id=request.session['lid'])
    return render(request,'worker/viewrating.html',{'val':ob})

@login_required(login_url='/')
def manage_skill_worker(request):
    ob = skill_table.objects.filter(worker_id__LOGIN_id=request.session['lid'])
    return render(request,'worker/manageskill.html',{'val':ob})

@login_required(login_url='/')
def add_new(request):
    return render(request, 'worker/addnew.html')

@login_required(login_url='/')
def add_post(request):
      skill=request.POST['textfield']
      experience=request.POST['textfield2']
      ob=skill_table()
      ob.skill=skill
      ob.experience=experience
      ob.worker_id=worker_table.objects.get(LOGIN_id=request.session['lid'])
      ob.save()
      return HttpResponse('''<script>alert('skill added successfully');window.location='/worker_page';</script>''')

@login_required(login_url='/')
def delete_skill(request,id):
    ob=skill_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('skill deleted successfully');window.location='/manage_skill_worker';</script>''')

@login_required(login_url='/')
def edit_skill(request,id):
    request.session['sid']=id
    ob = skill_table.objects.get(id=id)
    return render(request,'worker/edi.html',{'val':ob})


@login_required(login_url='/')
def edit_skill_post(request):
    skill = request.POST['textfield']
    experience = request.POST['textfield2']
    ob = skill_table.objects.get(id=request.session['sid'])
    ob.skill = skill
    ob.experience = experience
    ob.worker_id = worker_table.objects.get(LOGIN_id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert('skill added successfully');window.location='/manage_skill_worker';</script>''')


@login_required(login_url='/')
def view_skill_request(request):
    ob=request_table.objects.filter(skill__worker_id__LOGIN_id=request.session['lid'])
    return render(request,'worker/viewskillreq.html',{'value':ob})

@login_required(login_url='/')
def accept_skill_request(request,id):
    request.session['vid']=id
    ob=request_table.objects.get(id=id)
    ob.status='accept'
    ob.save()
    return HttpResponse('''<script>alert('accepted successfully');window.location='/view_skill_request';</script>''')


@login_required(login_url='/')
def reject_skill_request(request,id):
    request.session['vid']=id
    ob=request_table.objects.get(id=id)
    ob.status='reject'
    ob.save()
    return HttpResponse('''<script>alert('rejected successfully');window.location='/view_skill_request';</script>''')


@login_required(login_url='/')
def update_status(request,id):
    request.session['rid']=id
    ob=request_table.objects.get(id=id)
    return render(request,'worker/update.html')


@login_required(login_url='/')
def update_status_post(request):
    status=request.POST['textarea']
    ob=request_table.objects.get(id=request.session['rid'])
    ob.status=status
    ob.save()
    return HttpResponse('''<script>alert('updated successfully');window.location='/view_skill_request';</script>''')




@login_required(login_url='/')
def view_payment(request):
    ob = payment_table.objects.filter(request__skill__worker_id__LOGIN_id=request.session['lid'])
    return render(request, 'worker/viewpay.html', {'val': ob})




@login_required(login_url='/')
def send_complaint(request,id):
    request.session['wid']=id
    return render(request,'worker/sendcomplaint.html')

@login_required(login_url='/')
def send_complaint_post(request):
    complaint=request.POST['textarea']
    ob = worker_complaint_table()
    ob.reply='pending'
    import datetime
    ob.date=datetime.datetime.today().now()
    ob.request=request_table.objects.get(id=request.session['wid'])
    ob.worker_id=worker_table.objects.get(LOGIN_id=request.session['lid'])
    ob.complaint=complaint
    ob.save()
    return HttpResponse('''<script>alert('send successfully');window.location='/worker_page';</script>''')

@login_required(login_url='/')
def view_complaint_worker(request):
    ob=worker_complaint_table.objects.filter(worker_id__LOGIN_id=request.session['lid'])
    return render(request,'worker/viewcomplaint.html',{'val':ob})

@login_required(login_url='/')
def reply_worker(request,id):
    request.session['rid']=id
    ob=worker_complaint_table.objects.get(id=id)
    return render(request,'worker/sndrply.html',{'val':ob})


@login_required(login_url='/')
def reply_worker_post(request):
    reply=request.POST['textarea']
    ob=worker_complaint_table.objects.get(id=request.session['rid'])
    ob.reply=reply
    ob.save()
    return HttpResponse('''<script>alert('reply send successfully');window.location='/view_complaint_worker';</script>''')



@login_required(login_url='/')
def send_feedback_worker(request):
    # request.session['fid']=id
    return render(request,'worker/sendfeed.html')

@login_required(login_url='/')
def send_feedback_worker_post(request):
    feedback=request.POST['textarea']
    ob=feedback_table()
    import datetime
    ob.date = datetime.datetime.today().now()
    ob.Login_id = login_table.objects.get(id=request.session['lid'])
    ob.feedback=feedback
    ob.save()
    return HttpResponse('''<script>alert('send successfully');window.location='/worker_page';</script>''')


@login_required(login_url='/')
def view_workdetails(request):
    ob=user_work_table.objects.all()
    return render(request,'worker/workdetails.html',{'value':ob})


@login_required(login_url='/')
def send_work_request(request,id):
    request.session['wid']=id

    ob = user_work_request_table()
    import datetime
    ob.date = datetime.date.today()
    ob.status = "pending"
    ob.work_request = user_work_table.objects.get(id=request.session['wid'])
    ob.from_request_work = worker_table.objects.get(LOGIN_id=request.session['lid'])
    ob.save()

    return HttpResponse("<script>alert('Send successfully');window.location='/view_workdetails';</script>")


@login_required(login_url='/')
def view_workrequest_status(request):
    ob=user_work_request_table.objects.all()
    return render(request,'worker/viewreqsts.html',{'val':ob})

@login_required(login_url='/')
def incomingcomplaintworker(request):
    ob=user_complaint_table.objects.filter(request__skill__worker_id__LOGIN_id=request.session['lid'])
    return render(request, 'worker/incomingcomplaintworker.html', {'value': ob})

@login_required(login_url='/')
def incomingreplyworker(request,id):
    request.session['cid']=id
    ob=user_complaint_table.objects.get(id=id)
    return render(request, 'worker/wcreply.html')

@login_required(login_url='/')
def incomingreplyworker_post(request):
    reply = request.POST['textarea']
    ob = user_complaint_table.objects.get(id=request.session['cid'])
    ob.reply = reply
    ob.save()
    return HttpResponse('''<script>alert('reply send successfully');window.location='/incomingcomplaintworker'</script>''')


#user

def user_registration(request):
    return render(request,'user 3/userreg.html')

def user_registration_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield2']
    phoneno=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield5']
    pin=request.POST['textfield6']
    image=request.FILES['file']
    username=request.POST['textfield7']
    password=request.POST['textfield8']

    if login_table.objects.filter(username=username).exists():
        return HttpResponse(
            "<script>alert('Username already exists');window.location='/user_registration';</script>"
        )

    from django.core.files.storage import FileSystemStorage
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type='user'
    ob.save()


    obb=user_table()
    obb.name=name
    obb.email=email
    obb.phoneno=phoneno
    obb.place=place
    obb.post=post
    obb.image=fp
    obb.pin=pin
    obb.LOGIN=ob
    obb.save()
    return HttpResponse('''<script>alert('user register successfully');window.location='/';</script>''')

@login_required(login_url='/')
def user_page(request):
    return render(request,'user 3/userpage.html')


@login_required(login_url='/')
def send_rating(request,id):
    request.session['rid']=id
    ob = request_table.objects.get(id=id)
    return render(request,'user 3/rati.html',{'value':ob})

@login_required(login_url='/')
def send_rating_post(request):
    rating=request.POST['textfield7']
    review=request.POST['textarea2']
    ob=rating_table()
    import datetime
    ob.date = datetime.datetime.today().now()
    ob.user_id = user_table.objects.get(LOGIN_id=request.session['lid'])
    ob.request = request_table.objects.get(id=request.session['rid'])
    ob.rating=rating
    ob.review=review
    ob.save()
    return HttpResponse('''<script>alert('submitted successfully');window.location='/user_page';</script>''')


@login_required(login_url='/')
def send_complaint_user(request,id):
    request.session['wid']=id
    return render(request,'user 3/comp.html')

@login_required(login_url='/')
def send_complaint_user_post(request):
    complaint=request.POST['textarea']
    ob = user_complaint_table()
    ob.reply='pending'
    import datetime
    ob.date=datetime.datetime.today().now()
    ob.request=request_table.objects.get(id=request.session['wid'])
    ob.user_id=user_table.objects.get(LOGIN_id=request.session['lid'])
    ob.complaint=complaint
    ob.save()
    return HttpResponse('''<script>alert('send successfully');window.location='/user_page';</script>''')


# def view_reply_user(request):
#     ob=user_complaint_table.objects.all()
#     return render(request, 'user 3/viewrep.html',{'value': ob})


@login_required(login_url='/')
def view_reply_user(request):
    uid = request.session['lid']


    user = user_table.objects.get(LOGIN_id=uid)


    ob = user_complaint_table.objects.filter(user_id=user)

    return render(request, 'user 3/viewrep.html', {'value': ob})



# @login_required(login_url='/')
# def view_skill(request):
#     ob=skill_table.objects.all()
#     return render(request, 'user 3/viewski.html',{'value': ob})

@login_required(login_url='/')
def view_skill(request):
    ob=skill_table.objects.all()
    return render(request, 'user 3/viewski.html',{'value': ob})


@login_required(login_url='/')
def user_send_request(request,id):
    request.session['sid']=id
    ob=skill_table.objects.get(id=id)
    return render(request,'user 3/send_request.html')

@login_required(login_url='/')
def user_send_request_post(request):
    description=request.POST['textarea']
    ob = request_table()
    ob.description=description
    ob.skill=skill_table.objects.get(id=request.session['sid'])
    ob.user_id = user_table.objects.get(LOGIN_id=request.session['lid'])
    ob.status='pending'
    import datetime
    ob.date = datetime.datetime.today().now()
    ob.save()
    return HttpResponse('''<script>alert('requested successfully');window.location='/user_page';</script>''')


@login_required(login_url='/')
def send_feedback(request):
    # request.session['fid']=id
    return render(request,'user 3/feed.html')


@login_required(login_url='/')
def send_feedback_post(request):
    feedback=request.POST['textarea']
    ob=feedback_table()
    import datetime
    ob.date = datetime.datetime.today().now()
    ob.Login_id = login_table.objects.get(id=request.session['lid'])
    ob.feedback=feedback
    ob.save()
    return HttpResponse('''<script>alert('send successfully');window.location='/user_page';</script>''')



@login_required(login_url='/')
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return render(request,'login.html')




@login_required(login_url='/')
def view_request_status_user(request):
    ob=request_table.objects.filter(user_id__LOGIN_id=request.session['lid'])
    return render(request, 'user 3/viewrequest.html',{'val':ob})





@login_required(login_url='/')
def make_request_payment(request, id):
    req = request_table.objects.get(id=id)

    # For example, let's assume payment amount is fixed per request or based on some logic
    amount = 500  # ₹500 per request, you can change this or calculate dynamically
    amount_paise = amount * 100  # Razorpay expects amount in paise

    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    payment = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'payment': payment,
        'request_obj': req,
        'amount': amount,
        'razorpay_key': "rzp_test_SROSnyInFv81S4",
    }

    return render(request, 'user 3/pay.html', context)

@login_required(login_url='/')
def request_payment_success(request):
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        req = request_table.objects.get(id=request_id)

        # For example, set amount again
        amount = 500  # same logic as in make_request_payment

        # Save payment
        import datetime
        payment_table.objects.create(
            user_id=req.user_id,
            request=req,
            payment=amount,
            date=datetime.datetime.today().date(),
            status='Paid'
        )

        # Optionally, update request status
        req.status = 'Paid'
        req.save()

        return render(request, 'user 3/request_payment_success.html', {
            'request_obj': req,
            'amount': amount
        })



# def work_details(request):
#     ob = user_work_table.objects.all()
#     return render(request,'user 3/workdet.html',{'value':ob})


@login_required(login_url='/')
def work_details(request):

    uid = request.session['lid']


    user = user_table.objects.get(LOGIN_id=uid)


    ob = user_work_table.objects.filter(user_id=user)

    return render(request, 'user 3/workdet.html', {'value': ob})



@login_required(login_url='/')
def Add_newwork(request):
    return render(request, 'user 3/newwo.html')



@login_required(login_url='/')
def add_newwork_post(request):
    # ob = user_work_table()
    # work_name = request.POST['textfield']
    # details= request.POST['textfield2']
    # date=request.POST['textfield3']
    # time=request.POST['textfield4']
    # price=request.POST['textfield5']

    # ob.experience = experience
    # ob.user_id = user_table.objects.get(LOGIN_id=request.session['lid'])
    # ob.save()
    # return HttpResponse('''<script>alert('work added successfully');window.location='/work_details';</script>''')
    work_name = request.POST['textfield']
    details= request.POST['textfield2']
    date=request.POST['textfield3']
    time=request.POST['textfield4']
    price=request.POST['textfield5']

    obb=user_work_table()
    obb.user_id=user_table.objects.get(LOGIN_id=request.session['lid'])
    obb.work_name=work_name
    obb.details=details
    obb.date=date
    obb.time=time
    obb.price=price
    obb.save()
    return HttpResponse('''<script>alert('work added successfully');window.location='/work_details';</script>''')


@login_required(login_url='/')
def delete(request,id):
    ob=user_work_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('work deleted successfully');window.location='/work_details';</script>''')

@login_required(login_url='/')
def edit(request,id):
    request.session['sid']=id
    ob = user_work_table.objects.get(id=id)
    return render(request,'user 3/edt.html',{'val':ob})

# def edit_post(request):
#     # Get the ID stored in session from edit()
#     id = request.session['sid']
#
#     # Fetch the existing row
#     obb = user_work_table.objects.get(id=id)
#
#     # Update the fields
#     obb.work_name = request.POST['textfield']
#     obb.details = request.POST['textfield2']
#     obb.date = request.POST['textfield3']
#     obb.time = request.POST['textfield4']
#     obb.price = request.POST['textfield5']
#
#     # Save changes
#     obb.save()
#
#     return HttpResponse('''<script>alert('Updated successfully');window.location='/work_details';</script>''')


# def edit_post(request):
#     work_name=request.POST['textfield']
#     details = request.POST['textfield2']
#     date = request.POST['textfield3']
#     time = request.POST['textfield4']
#     price = request.POST['textfield5']
#
#     obb = user_work_table()
#     obb.user_id = user_table.objects.get(LOGIN_id=request.session['lid'])
#     obb.work_name = work_name
#     obb.details = details
#     obb.date = date
#     obb.time = time
#     obb.price = price
#     obb.save()
#     return HttpResponse('''<script>alert('submitted successfully');window.location='/work_details';</script>''')


@login_required(login_url='/')
def edit_post(request):
    work_name = request.POST['textfield']
    details = request.POST['textfield2']
    date = request.POST['textfield3']
    time = request.POST['textfield4']
    price = request.POST['textfield5']


    obb = user_work_table.objects.get(id=request.session['sid'])


    obb.work_name = work_name
    obb.details = details
    obb.date = date
    obb.time = time
    obb.price = price

    obb.save()
    return HttpResponse('''<script>alert('Updated successfully');window.location='/work_details';</script>''')


@login_required(login_url='/')
def view_workrequest(request):
    ob = user_work_request_table.objects.filter(work_request__user_id__LOGIN_id=request.session['lid'])
    return render(request, 'user 3/viewworkre.html', {'val': ob})


@login_required(login_url='/')
def Accept(request,id):
    request.session['wid']=id
    ob=user_work_request_table.objects.get(id=id)
    ob.status='Accepted'
    ob.save()
    return HttpResponse('''<script>alert('accepted successfully');window.location='/view_workrequest';</script>''')

@login_required(login_url='/')
def Reject(request,id):
    request.session['wid']=id
    ob=user_work_request_table.objects.get(id=id)
    ob.status='Rejected'
    ob.save()
    return HttpResponse('''<script>alert('rejected successfully');window.location='/view_workrequest';</script>''')



# ===========================================

from django.http import JsonResponse
@login_required(login_url='/')
def worker_chat_withuser(request):
    worker = worker_table.objects.get(LOGIN_id=request.session['lid'])
    skills = skill_table.objects.filter(worker_id=worker)

    accepted_requests = request_table.objects.filter(
        skill__in=skills,
        status="accepted"
    )

    return render(request, "worker/fur_chat.html", {
        "val": accepted_requests
    })





@login_required(login_url='/')
def chatview(request):
    worker = worker_table.objects.get(LOGIN_id=request.session['lid'])
    skills = skill_table.objects.filter(worker_id=worker)

    ob = request_table.objects.filter(
        skill__in=skills,
        status="accept"
    )

    d = []
    seen_loginids = set()

    for i in ob:
        loginid = i.user_id.LOGIN.id   # FIXED (correct login foreign key)

        if loginid not in seen_loginids:
            r = {
                "name": i.user_id.name,
                "email": i.user_id.email,
                "phone": i.user_id.phoneno,
                "skill": i.skill.skill,
                "description": i.description,
                "date": str(i.date),
                "loginid": i.user_id.LOGIN.id,
                "photo": i.user_id.image.url if i.user_id.image else ""
            }
            d.append(r)
            seen_loginids.add(loginid)

    from django.http import JsonResponse
    return JsonResponse(d, safe=False)







@login_required(login_url='/')
def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat_table()
    ob.fromid=login_table.objects.get(id=request.session['lid'])
    ob.toid=login_table.objects.get(id=id)
    ob.message=msg
    import datetime
    ob.date=datetime.datetime.today().date().strftime("%Y-%m-%d")
    ob.save()

    return JsonResponse({"task":"ok"})



@login_required(login_url='/')
def coun_msg(request,id):
    ob1=chat_table.objects.filter(fromid__id=id,toid__id=request.session['lid'])
    ob2=chat_table.objects.filter(fromid__id=request.session['lid'],toid__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.fromid.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=user_table.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image.url,"user_lid":obu.LOGIN.id})

# ==========================================================

from django.http import JsonResponse


@login_required(login_url='/')
def user_chat_withworker(request):
    user = user_table.objects.get(LOGIN_id=request.session['lid'])

    accepted_requests = request_table.objects.filter(
        user_id=user,
        status="accept"
    )

    return render(request, "user 3/fur_chat.html", {
        "val": accepted_requests
    })




@login_required(login_url='/')
def u_chatview(request):
    user = user_table.objects.get(LOGIN_id=request.session['lid'])

    ob = request_table.objects.filter(
        user_id=user,
        status="accept"
    )

    d = []
    seen_worker_ids = set()

    for i in ob:
        worker = i.skill.worker_id  # worker object

        if worker.id not in seen_worker_ids:
            r = {
                "name": worker.name,
                "email": worker.email,
                "phone": worker.phoneno,
                "skill": i.skill.skill,
                "description": i.description,
                "date": str(i.date),
                "loginid": worker.LOGIN.id,
                "photo": worker.image.url if worker.image else ""
            }
            d.append(r)
            seen_worker_ids.add(worker.id)

    return JsonResponse(d, safe=False)




@login_required(login_url='/')
def u_coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat_table()
    ob.fromid=login_table.objects.get(id=request.session['lid'])
    ob.toid=login_table.objects.get(id=id)
    ob.message=msg
    import datetime
    ob.date=datetime.datetime.today().date().strftime("%Y-%m-%d")
    ob.save()

    return JsonResponse({"task":"ok"})



@login_required(login_url='/')
def u_coun_msg(request,id):
    ob1=chat_table.objects.filter(fromid__id=id,toid__id=request.session['lid'])
    ob2=chat_table.objects.filter(fromid__id=request.session['lid'],toid__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.fromid.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=worker_table.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image.url,"user_lid":obu.LOGIN.id})



@login_required(login_url='/')
def view_feedback(request):
    ob = feedback_table.objects.all()
    print(ob)
    return render(request,'user 3/website_feedback.html', {'val': ob})

@login_required(login_url='/')
def worker_view_feedback(request):
    ob = feedback_table.objects.all()
    print(ob)
    return render(request, 'worker/website_feedback.html', {'val': ob})




# def chatbot(request):
#     return render(request, 'worker/chatbot.html')
#
# def chatbot_reply(request):
#     user_msg = request.GET.get('msg', '').lower()
#
#     faqs = ChatbotFAQ.objects.all()
#
#     for faq in faqs:
#         if user_msg in faq.question.lower():
#             return JsonResponse({'reply': faq.answer})
#
#     return JsonResponse({
#         'reply': "Sorry, I couldn't understand that. Please contact JOBSY support."
#     })

@login_required(login_url='/')
def chatbot(request):
    faqs = ChatbotFAQ.objects.all()
    return render(request, 'worker/chatbot.html', {'faqs': faqs})

@login_required(login_url='/')
def chatbot_reply(request):
    qid = request.GET.get('qid')

    try:
        faq = ChatbotFAQ.objects.get(id=qid)
        return JsonResponse({'reply': faq.answer})
    except ChatbotFAQ.DoesNotExist:
        return JsonResponse({
            'reply': "Sorry, I couldn't understand that. Please contact JOBSY support."
        })

@login_required(login_url='/')
def user_chatbot(request):
    faqs = Chatbotuser.objects.all()
    return render(request, 'user 3/chatbot.html', {'faqs': faqs})

@login_required(login_url='/')
def user_chatbot_reply(request):
    qid = request.GET.get('qid')

    try:
        faq = Chatbotuser.objects.get(id=qid)
        return JsonResponse({'reply': faq.answer})
    except Chatbotuser.DoesNotExist:
        return JsonResponse({'reply': "Sorry, I couldn't understand that."})



@login_required(login_url='/')
def incoming_complaints(request):
    ob=worker_complaint_table.objects.filter(request__user_id__LOGIN_id=request.session['lid'])
    return render(request,'user 3/incomingcomplaints.html',{'value':ob})

@login_required(login_url='/')
def incomingcomplaintreply(request,id):
    request.session['cid']=id
    ob=worker_complaint_table.objects.get(id=id)
    return render(request, 'user 3/incomingcomplaintreply.html')

@login_required(login_url='/')
def incomingcomplaintreply_post(request):
    reply=request.POST['textarea']
    ob = worker_complaint_table.objects.get(id=request.session['cid'])
    ob.reply = reply
    ob.save()
    return HttpResponse('''<script>alert('reply send successfully');window.location='/incoming_complaints'</script>''')
