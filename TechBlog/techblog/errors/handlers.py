from flask import Blueprint, render_template

# Creating blueprint for errors
errors = Blueprint('errors', __name__)

# event handler for error raised (app_errorhandler)
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404  # 404 is error code response


@errors.app_errorhandler(403)
def error_403(error):
    # 403 is error code response
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    # 500 is error code response
    return render_template('errors/500.html'), 500