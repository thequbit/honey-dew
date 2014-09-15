import json
import datetime
import urllib

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    #MyModel,
    Users,
    Tasks,
    )


@view_config(route_name='login.json')
def login(request):
    response = {'success': False}
#    try:
    if True:

         username = request.GET['username']
         password = request.GET['password']

         # remove url encoding:
         username = urllib.unquote(username).decode('utf8')
         password = urllib.unquote(password).decode('utf8')

         success,user = Users.login_user(
             DBSession,
             username,
             password,
         )

         if success == True:
             response['token'] = user.token
             response['name'] = user.name
             response['success'] = True
    
#    except:
#        pass
    
    resp = json.dumps(response)
    return Response(resp,content_type="application/json")

@view_config(route_name='get_tasks.json')
def get_tasks(request):
    response = {'success': False}
#    try:
    if True:

         token = request.GET['token']

         tasks = Tasks.get_tasks(
             DBSession,
             token,
         )

         print "\n\n"
         print tasks
         print "\n\n"

         ret_tasks = []
         if tasks != None:
             for task_id, creator_id, owner_id, title, content, due_datetime, \
                     completed, notes, creator_name in tasks:
                 ret_tasks.append({
                     'creator_id': creator_id,
                     'owner_id': owner_id,
                     'title': title,
                     'content': content,
                     'due_datetime': str(due_datetime),
                     'completed': completed,
                    'creator_name': creator_name,
                 })

         response['tasks'] = ret_tasks
         response['success'] = True

#    except:
#        pass

    resp = json.dumps(response)
    return Response(resp,content_type="application/json")

@view_config(route_name='get_created_tasks.json')
def get_created_tasks(request):
    response = {'success': False}
#    try:
    if True:
         token = request.GET['token']

         tasks = Tasks.get_created_tasks(
             DBSession,
             token,
         )

         ret_tasks = []
         for task_id, creator_id, owner_id, title, content, due_datetime, \
                 completed, notes, creator_name in tasks:
             ret_tasks.append({
                 'creator_id': creator_id,
                 'owner_id': owner_id,
                 'title': title,
                 'content': content,
                 'due_datetime': str(due_datetime),
                 'completed': completed,
                 'creator_name': creator_name,
             })

         response['tasks'] = ret_tasks
         response['success'] = True

#    except:
#        pass

    resp = json.dumps(response)
    return Response(resp,content_type="application/json")


@view_config(route_name='create_task.json')
def create_task(request):

    response = {'success': False}
#    try:
    if True:

         token = request.GET['token']
         owner_id = request.POST['owner_id']
         title = request.POST['title']
         content = request.POST['content']
         due_datetime = datetime.datetime.strptime(
             request.POST['due_datetime'],
             "%Y-%m-%d",
         )

         task = Tasks.create_task(
             session = DBSession,
             owner_id = owner_id,
             token = token,
             title = title,
             content = content,
             due_datetime = due_datetime,
         )

         response['task_id'] = task.id
         response['success'] = True

#    except:
#        pass

    resp = json.dumps(response)
    return Response(resp,content_type="application/json")

@view_config(route_name='get_users.json')
def get_users(request):

    response = {'success': False}
#    try:
    if True:

         token = request.GET['token']

         users = Users.get_users(
             session = DBSession,
             token = token,
         )

         ret_users = []
         for user_id, name in users:
             ret_users.append({
                 'user_id': user_id,
                 'name': name,
             })

         response['users'] = ret_users
         response['success'] = True

#    except:
#        pass

    resp = json.dumps(response)
    return Response(resp,content_type="application/json")

