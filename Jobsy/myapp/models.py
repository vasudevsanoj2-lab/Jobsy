from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class worker_table(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phoneno=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    status=models.CharField(max_length=100)
    image=models.FileField()
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)


class user_table(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phoneno=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    image=models.FileField()
    LOGIN = models.ForeignKey(login_table,on_delete=models.CASCADE)





class skill_table(models.Model):
    worker_id=models.ForeignKey(worker_table,on_delete=models.CASCADE)
    skill=models.CharField(max_length=100)
    experience=models.IntegerField()

class request_table(models.Model):
    user_id=models.ForeignKey(user_table,on_delete=models.CASCADE)
    skill=models.ForeignKey(skill_table,on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    date=models.DateField()



class payment_table(models.Model):
    user_id=models.ForeignKey(user_table,on_delete=models.CASCADE)
    request=models.ForeignKey(request_table,on_delete=models.CASCADE)
    payment=models.BigIntegerField()
    date=models.DateField()
    status=models.CharField(max_length=100)



class rating_table(models.Model):
    request=models.ForeignKey(request_table,on_delete=models.CASCADE)
    user_id=models.ForeignKey(user_table,on_delete=models.CASCADE)
    rating=models.IntegerField()
    review=models.CharField(max_length=100)
    date=models.DateField()


class user_complaint_table(models.Model):
    user_id=models.ForeignKey(user_table,on_delete=models.CASCADE)
    request=models.ForeignKey(request_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)


class worker_complaint_table(models.Model):
    worker_id=models.ForeignKey(worker_table,on_delete=models.CASCADE)
    request=models.ForeignKey(request_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)

class chat_table(models.Model):
    fromid=models.ForeignKey(login_table,on_delete=models.CASCADE,related_name='hh')
    toid=models.ForeignKey(login_table,on_delete=models.CASCADE,related_name='pl')
    message=models.CharField(max_length=100)
    date=models.DateField()




class feedback_table(models.Model):
    Login_id=models.ForeignKey(login_table,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    date=models.DateField()



class user_work_table(models.Model):
    user_id=models.ForeignKey(user_table,on_delete=models.CASCADE)
    work_name=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    price=models.IntegerField()


class user_work_request_table(models.Model):
    from_request_work=models.ForeignKey(worker_table,on_delete=models.CASCADE)
    work_request=models.ForeignKey(user_work_table,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=100)


class ChatbotFAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()


class Chatbotuser(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()