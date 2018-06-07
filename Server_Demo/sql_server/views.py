# coding=utf-8
from django.http import HttpResponse
from sql_server.models import DatabaseDriver
import json

def show_database(request):
    if request.method == 'GET':
        datbase_driver = DatabaseDriver()
        student_list_obj = datbase_driver.list()
        student_list = []
        count = 1
        for student in student_list_obj:
            student_info = {
                'stt': str(count),
                'id': str(student.id),
                'name': student.name,
                'birthday': student.birthday,
                'class': student.class_name,
            }
            count = count + 1
            student_list.append(student_info)
        result = {
            'db': student_list,
        }
        return HttpResponse(json.dumps(result), content_type='application/json')

def query(request):
    if request.method =='POST':
        name = request.POST.get('name',None)
        birthday = request.POST.get('birthday', None)
        class_name = request.POST.get('class', None)

        database = DatabaseDriver()
        database.add_student(name=name,birthday=birthday,class_name=class_name)
        result = {
            'result': 'success',
        }
        return HttpResponse(json.dumps(result),content_type='application/json')