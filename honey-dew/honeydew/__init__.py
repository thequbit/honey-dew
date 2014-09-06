from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)


    config.add_route('login.json','login.json')
    config.add_route('get_tasks.json','get_tasks.json')
    config.add_route('get_created_tasks.json', 'get_created_tasks.json')
    config.add_route('create_task.json','create_task.json')
    config.add_route('get_users.json', 'get_users.json')

    #config.add_route('home', '/')


    config.scan()
    return config.make_wsgi_app()
