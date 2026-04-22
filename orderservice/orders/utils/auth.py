# concept (not final code yet)

def get_user_from_request(request):
    token = request.headers["Authorization"]
    user = decode_token(token)
    return user