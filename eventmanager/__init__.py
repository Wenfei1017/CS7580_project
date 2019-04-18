from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from eventmanager.config import Config, swagger_template
from flasgger import Swagger
from flask_caching import Cache
from flask_migrate import Migrate
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
cache = Cache()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # http://flask-sqlalchemy.pocoo.org/2.3/contexts/
    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    swagger = Swagger(app, template=swagger_template)
    migrate.init_app(app, db)

    cache_servers = os.environ.get('MEMCACHIER_SERVERS')
    if cache_servers is None:
        cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    else:
        cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
        cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
        cache.init_app(app,
                       config={'CACHE_TYPE': 'saslmemcached',
                               'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                               'CACHE_MEMCACHED_USERNAME': cache_user,
                               'CACHE_MEMCACHED_PASSWORD': cache_pass,
                               'CACHE_OPTIONS': {'behaviors': {
                                   # Faster IO
                                   'tcp_nodelay': True,
                                   # Keep connection alive
                                   'tcp_keepalive': True,
                                   # Timeout for set/get requests
                                   'connect_timeout': 2000,  # ms
                                   'send_timeout': 750 * 1000,  # us
                                   'receive_timeout': 750 * 1000,  # us
                                   '_poll_timeout': 2000,  # ms
                                   # Better failover
                                   'ketama': True,
                                   'remove_failed': 1,
                                   'retry_timeout': 2,
                                   'dead_timeout': 30}}})

    from eventmanager.registrations.routes import registrations
    from eventmanager.reviews.routes import reviews
    from eventmanager.users.routes import users
    from eventmanager.sponsors.routes import sponsors
    from eventmanager.main.routes import main
    from eventmanager.events.routes import events
    app.register_blueprint(reviews)
    app.register_blueprint(registrations)
    app.register_blueprint(users)
    app.register_blueprint(sponsors)
    app.register_blueprint(main)
    app.register_blueprint(events)

    # recreate db structure for testing
    # db.drop_all()
    # db.create_all()
    # db.session.commit()

    return app
