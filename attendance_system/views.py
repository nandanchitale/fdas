from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage

from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from .forms import CreateStudentForm
from .models import Student, Attendence

# from django.views.decorators import gzip

from datetime import date

class StudentRegistration(TemplateView):
    template_name = 'studentRegistration.html'
    def post(self, request, *args, **kwargs):
        data = request.POST.get('image')
        if data:
            print("data recieved")
        else:
            print("false")
        # try:
        #     image_data = get_face_detect_data(data)
        #     if image_data:
        #         return JsonResponse(status=200, data={'image': image_data, 'message': 'Face detected'})
        # except Exception as e:
        #     print(e)
        return JsonResponse(status=400, data={'errors': {'error_message': 'Not detected'}})

def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        # print(request.POST)

        return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})

        stat = False
        try:
            student = Student.objects.get(
                registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'firstname') + " " + studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm': studentForm}
    return render(request, 'login.html', context)


def registerStudent(request):
    studentForm = CreateStudentForm()
    if request.method == 'POST':
        student = Student()
        data = request.POST.get('student_img')
        print(data)
        if data:
            print("data recieved")
        else:
            print("data not recieved")

        student.profile_pic = request.POST.get('student_img')
        if student.profile_pic:
            print("data found.")
        else:
            print("data not found")

        # print(request.POST)

        # return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})

        stat = False
        try:
            student = Student.objects.get(
                registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'firstname') + " " + studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm': studentForm}
    return render(request, 'studentRegistration.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        flag = False

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.info(request, 'Username or password is incorrect')

        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        context = {'studentForm': studentForm}

        if (username == 'admin') and (password == 'admin'):
            flag = True
            #user = authenticate(request, username=username, password=password)

        if flag:
            #login(request, user)
            return render(request, 'studentRegistration.html', context)
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def registerFaculty(request):

    if (request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if(password == confirm_password):
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
            elif User.objects.filter(email=email):
                messages.info(request, 'Username already exists.')
            else:
                user = Professor(
                    username=username,
                    password=password,
                    email=email
                )
                user.save()
                user = User(
                    username=username,
                    password=password,
                    email=email
                )
                user.save()
                print("User created...")
            return render(request, 'index.html', {'name': username})
        else:
            return render(request, 'login.html', {'error': 'Passwords Do not match, try again'})

    else:
        return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(
                registration_id=reg_id, branch=branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form': updateStudentForm,
                       'prev_reg_id': reg_id, 'student': student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendance_system/student_update.html', context)


def updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(
                registration_id=request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(
                data=request.POST, files=request.FILES, instance=student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')
    return render(request, 'attendance_system/student_update.html', context)


def takeAttendence(request):
    if request.method == 'POST':
        details = {
            'branch': request.POST['branch'],
            'year': request.POST['year'],
            'section': request.POST['section'],
            'period': request.POST['period'],
            'faculty': request.user.faculty
        }
        if Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'], section=details['section'], period=details['period']).count() != 0:
            messages.error(request, "Attendence already recorded.")
            return redirect('home')
        else:
            students = Student.objects.filter(
                branch=details['branch'], year=details['year'], section=details['section'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'],
                                            status='Present')
                    attendence.save()
                else:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today(
            )), branch=details['branch'], year=details['year'], section=details['section'], period=details['period'])
            context = {"attendences": attendences, "ta": True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'attendance_system/attendence.html', context)
    context = {}
    return render(request, 'attendance_system/home.html', context)


def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendance_system/attendence.html', context)


def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'attendance_system/facultyForm.html', context)


# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,image = self.video.read()
#         ret,jpeg = cv2.imencode('.jpg',image)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'
#         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def videoFeed(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         print("aborted")

# def getVideo(request):
#     return render(request, 'attendance_system/videoFeed.html')
