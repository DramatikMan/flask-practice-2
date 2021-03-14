from flask import Blueprint, render_template

from ..extensions import rest_api
from .post import PostApi
from .auth import AuthApi


rest_api.add_resource(
    PostApi,
    '/api/post',
    '/api/post/<int:post_id>',
    endpoint='api'
)
rest_api.add_resource(
    AuthApi,
    '/api/auth'
)


bp_api = Blueprint('api', __name__, template_folder='templates/api')


@bp_api.route('/')
def index():
    return render_template('index.html')
