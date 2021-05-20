"""
Module for creating error handlers
"""
from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)


@error_pages.app_errorhandler(404)
def error_404(error):
    """ Function that simply renders 404 error page """
    return render_template('error_pages/404.html'), 404


@error_pages.app_errorhandler(500)
def error_500(error):
    """ Function that simply renders 500 error page """
    return render_template('error_pages/500.html'), 500
