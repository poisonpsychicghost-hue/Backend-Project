- AuthN / AuthZ Tests - 
--Login: '/user/login', POST:
    -No Login Info -
curl -i -X POST http://127.0.0.1:5000/user/login

-H 'Content-Type: application/json'

HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:23:50 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 167
Connection: close

<!doctype html>
<html lang=en>
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>The browser (or proxy) sent a request that this server could not understand.</p>
-Incorrect Auth 'username' -
curl -i -X POST http://127.0.0.1:5000/user/login

-H 'Content-Type: application/json'

-d '{"username": "dev12", "password": "dev12345"}'

HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:22:33 GMT
Content-Type: application/json
Content-Length: 57
Connection: close

{"code":"Unauthorized","message":"Invalid Credentials."}

-Incorrect Auth 'password' -
curl -i -X POST http://127.0.0.1:5000/user/login

-H 'Content-Type: application/json'

-d '{"username": "dev123", "password": "fake_password"}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:22:40 GMT
Content-Type: application/json
Content-Length: 57
Connection: close

{"code":"Unauthorized","message":"Invalid Credentials."}

-Valid Auth -
curl -i -X POST http://127.0.0.1:5000/user/login

-H 'Content-Type: application/json'

-d '{"username": "dev123", "password": "dev12345"}'

HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:22:47 GMT
Content-Type: application/json
Content-Length: 263
Connection: close

{"message":"Login OK. Token Expiry: (2026-11-20 06:22:47.711485)","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwidXNlcm5hbWUiOiJkZXYxMjMiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3OTUxNTU3Njd9.nzpvE1Q_8jLI45QJ8Iq8XSiySBeZp2jGf9TGxhWPF9Y","username":"dev123"}

--Admin '/admin/system-check', GET:

-No Auth Header
curl -i -X GET http://
127.0.0.1:5000/admin/system-check \


HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:28:55 GMT
Content-Type: application/json
Content-Length: 60
Connection: close

{"code":"Unauthorized","message":"No Authorization Header"}

-Non-Admin Valid Token
curl -i -X GET http://127.0.0.1:5000/admin/system-check

-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwidXNlcm5hbWUiOiJ0ZXN0MTIzIiwicm9sZSI6InVzZXIiLCJleHAiOjE3OTUxNTYwOTd9.p-Ts7FUL_39WILPS2o007gWP3TTnimBNikPergcwxvE'
HTTP/1.1 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:29:37 GMT
Content-Type: application/json
Content-Length: 52
Connection: close

{"code":"Forbidden","message":"Admin Access Only."}

-Admin Expired Token
curl -i -X GET http://127.0.0.1:5000/admin/system-check

-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwidXNlcm5hbWUiOiJkZXYxMjMiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3OTQ5NjY3NzJ9.gy7_08XgE_otz_xhl_-WIDuo0zdhJ6vmoVrT-LhEkiE'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:30:52 GMT
Content-Type: application/json
Content-Length: 87
Connection: close

{"code":"Expired_Token","message":"Token Has Expired. Please Re-Login and TryAgain."}

-Admin Valid Token
curl -i -X GET http://127.0.0.1:5000/admin/system-check

-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwidXNlcm5hbWUiOiJkZXYxMjMiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3OTUxNTU3Njd9.nzpvE1Q_8jLI45QJ8Iq8XSiySBeZp2jGf9TGxhWPF9Y'
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.3
Date: Fri, 20 Nov 2026 02:31:38 GMT
Content-Type: application/json
Content-Length: 370
Connection: close

{"user_list":[{"created_at":"Sun, 15 Nov 2026 02:22:49 GMT","id":1,"role":"user","username":"test"},{"created_at":"Sun, 15 Nov 2026 02:23:16 GMT","id":2,"role":"user","username":"hannibal"},{"created_at":"Sun, 15 Nov 2026 03:12:17 GMT","id":3,"role":"admin","username":"dev123"},{"created_at":"Tue, 17 Nov 2026 20:23:47 GMT","id":4,"role":"user","username":"test123"}]}