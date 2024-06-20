# middleware.py
def open_access_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Credentials"] = True
        return response
    return middleware