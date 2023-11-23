from rest_framework.exceptions import APIException

class PermissionDenied(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'

class IsAuthenticated(APIException):
    status_code = 403
    default_detail = 'You are already authenticated.'
    default_code = 'authenticated'
    redirect_to_index = True

class IsNotAuthenticated(APIException):
    status_code = 403
    default_detail = 'You need to be authenticated first.'
    default_code = 'not_authenticated'
    redirect_to_login = True
