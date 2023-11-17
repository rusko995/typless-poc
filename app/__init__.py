from flask import Flask
from app.errorHandlers import handle_bad_request, handle_internal_server_error, handle_generic_exception, not_found_error

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    app.errorhandler(400)(handle_bad_request)
    app.errorhandler(404)(not_found_error)
    app.errorhandler(500)(handle_internal_server_error)
    app.errorhandler(Exception)(handle_generic_exception)

    from app.models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    from app.routes import routes
    app.register_blueprint(routes)

    return app
