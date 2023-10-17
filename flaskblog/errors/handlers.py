from flask import render_template, request, Blueprint
errors=Blueprint('errors','__name__')

@errors.app_errorhandler(404)
def error_404(errors):
    return render_template('errors/404.html'),404


@errors.app_errorhandler(403)
def error_403(errors):
    return render_template('errors/404.html'),403


@errors.app_errorhandler(500)
def error_500(errors):
    return render_template('errors/404.html'),500