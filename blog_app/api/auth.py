from flask import current_app, abort
from flask_restful import Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from ..models import User
from .parsers import user_post_parser


class AuthApi(Resource):
    def post(self):
        args = user_post_parser.parse_args()
        user = User.query.filter_by(username=args['username']).one()

        if user.check_password(args['password']):
            s = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600
            )
            token = s.dumps({'id': user.id})
            return {'token': token.decode()}
        else:
            abort(401)
