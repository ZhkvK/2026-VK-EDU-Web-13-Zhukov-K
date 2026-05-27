from urllib.parse import parse_qsl

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    get_params = parse_qsl(environ.get('QUERY_STRING', ''))

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    post_params = parse_qsl(request_body)

    response = f"GET параметры:\n{get_params}\n\nPOST параметры:\n{post_params}\n"
    return [response.encode('utf-8')]