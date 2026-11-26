# Province Service – HTTP & Security Walkthrough

This document describes the current behavior of the `province` endpoints, with a focus on:
- authentication and authorization
- ownership and existence checks
- input validation
- pagination behavior

All examples assume the API is running at `http://127.0.0.1:5000`.

---

## 1. Authentication Guard on Province Routes

### 1.1 Unauthenticated create attempt

**Request**

```bash
curl -i -X POST http://127.0.0.1:5000/province/create
Response

Http
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{"code":"Unauthorized","message":"No Authorization Header"}
Behavior

All province routes require a valid JWT.
If no Authorization header is provided, the API returns 401 Unauthorized with a consistent JSON body:
code: "Unauthorized"
message: "No Authorization Header"
1.2 Invalid token
From the full CRUD walkthrough:

Bash
curl -i -X GET http://127.0.0.1:5000/province/12 \
  -H 'Authorization: Bearer this.token.works'
Response

Http
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{"code":"Unauthorized","message":"Invalid Token."}
Behavior

If a JWT is present but invalid, the API returns 401 Unauthorized with:
code: "Unauthorized"
message: "Invalid Token."
2. Create + List Provinces
2.1 Successful create as admin (user_id = 3)
Request

Bash
curl -i -X POST http://127.0.0.1:5000/province/create \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <admin_token_for_user_3>' \
  -d '{"name": "syria-test", "difficulty": "hard"}'
Response

Http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "created_at": "Mon, 23 Nov 2026 21:55:18 GMT",
  "current_turn": "1",
  "difficulty": "hard",
  "id": 3,
  "message": "Province Creation Successful",
  "name": "syria-test",
  "user_id": 3
}
Behavior

Requires a valid JWT.
Creates a province owned by the authenticated user (user_id taken from JWT).
Returns 201 Created with:
a success message
core province fields: id, name, difficulty, current_turn, created_at, user_id.
2.2 Successful create as normal user (user_id = 4)
Request

Bash
curl -i -X POST http://127.0.0.1:5000/province/create \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <user_token_for_user_4>' \
  -d '{"name": "test-province2", "difficulty": "medium"}'
Response

Http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "created_at": "Mon, 23 Nov 2026 21:57:59 GMT",
  "current_turn": "1",
  "difficulty": "medium",
  "id": 4,
  "message": "Province Creation Successful",
  "name": "test-province2",
  "user_id": 4
}
Behavior

Same behavior as for admin: province is always tied to the authenticated user ID.
Confirms that regular users can create their own provinces.
2.3 List provinces (with and without pagination params)
2.3.1 Default list
Request

Bash
curl -i -X GET http://127.0.0.1:5000/province/list \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response (excerpt)

Http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "List of Provinces for user3",
  "province_list": [
    {
      "created_at": "Mon, 23 Nov 2026 21:55:18 GMT",
      "current_turn": "1",
      "difficulty": "hard",
      "id": 3,
      "name": "syria-test"
    }
  ]
}
Behavior

Returns only provinces owned by the authenticated user.
Response includes:
a descriptive message
a province_list array of province summaries.
2.3.2 Paginated list (after seeding ~50 provinces)
Request – page 1

Bash
curl -i -X GET "http://127.0.0.1:5000/province/list?page=1&per_page=10" \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response (excerpt)

Json
{
  "message": "List of Provinces for user 3",
  "page": 1,
  "pages": 6,
  "per_page": 10,
  "province_list": [ ...10 provinces... ],
  "total": 53
}
Request – last page

Bash
curl -i -X GET "http://127.0.0.1:5000/province/list?page=6&per_page=10" \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response (excerpt)

Json
{
  "message": "List of Provinces for user3",
  "page": 6,
  "pages": 6,
  "per_page": 10,
  "province_list": [
    {"id": 54, "name": "Virginia Maior", ...},
    {"id": 55, "name": "Virginia Wisconsia", ...},
    {"id": 56, "name": "Terra Vulcans", ...}
  ],
  "total": 53
}
Request – page beyond last

Bash
curl -i -X GET "http://127.0.0.1:5000/province/list?page=7&per_page=10" \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response (excerpt)

Json
{
  "message": "List of Provinces for user3",
  "page": 7,
  "pages": 6,
  "per_page": 10,
  "province_list": [],
  "total": 53
}
Behavior

Pagination fields: page, pages, per_page, total.
Requesting beyond the last page returns an empty province_list with the requested page and true pages count.
3. Read by ID and Existence Checks
3.1 Read existing province
Request

Bash
curl -i -X GET http://127.0.0.1:5000/province/3 \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response

Http
HTTP/1.1 200 OK
Content-Type: application/json

{"current_turn":"1","difficulty":"hard","id":3,"name":"syria-test"}
3.2 Read non-existent province
Request

Bash
curl -i -X GET http://127.0.0.1:5000/province/999 \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response

Http
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{"code":"Not Found","message":"Province Not Found"}
Behavior

Valid authenticated users:
200 OK for existing IDs.
404 Not Found for missing IDs with a consistent JSON error:
code: "Not Found"
message: "Province Not Found".
4. Update & Delete: Validation and Errors
4.1 Happy-path update
Request

Bash
curl -i -X PATCH http://127.0.0.1:5000/province/3 \
  -H 'Authorization: Bearer <admin_token_for_user_3>' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Illyria"}'
Response

Http
HTTP/1.1 200 OK
Content-Type: application/json

{"current_turn":"1","difficulty":"hard","id":3,"name":"Illyria"}
4.2 Delete existing province
Request

Bash
curl -i -X DELETE http://127.0.0.1:5000/province/2 \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response

Http
HTTP/1.1 200 OK
Content-Type: application/json

{"code":"Deleted","message":"Province 2 Deleted Successfully"}
4.3 Delete non-existent province
Request

Bash
curl -i -X DELETE http://127.0.0.1:5000/province/999 \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response

Http
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{"code":"Not Found","message":"Province Not Found"}
4.4 Missing JSON body on PATCH
Request

Bash
curl -i -X PATCH http://127.0.0.1:5000/province/3 \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response

Http
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{"code":"Bad Request","message":"Request Body must be JSON"}
4.5 Invalid difficulty value
Request

Bash
curl -i -X PATCH http://127.0.0.1:5000/province/3 \
  -H 'Authorization: Bearer <admin_token_for_user_3>' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Illyria", "difficulty": "EZ"}'
Response

Http
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{"code":"Bad Request","message":"Difficulty must be (\"easy\", \"medium\", or \"hard\")."}
Behavior

Update/delete routes enforce:
existence check (404 Not Found),
JSON body presence (400 Bad Request),
domain validation on fields such as difficulty (400 Bad Request).
5. Admin-Only View of All Users (Cross-Service Security)
From admin/system-check:

Admin request

Bash
curl -i -X GET http://127.0.0.1:5000/admin/system-check \
  -H 'Authorization: Bearer <admin_token_for_user_3>'
Response (excerpt)

Http
HTTP/1.1 200 OK
Content-Type: application/json

{"user_list":[{"id":1,"role":"user","username":"test"}, ... ]}
Non-admin request

Bash
curl -i -X GET http://127.0.0.1:5000/admin/system-check \
  -H 'Authorization: Bearer <user_token_for_user_4>'
Response

Http
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json

{"code":"Forbidden","message":"Admin Access Only."}
Behavior

Admin routes rely on the role claim in the JWT (e.g., g.role == "admin").
Non-admin users receive 403 Forbidden with a consistent error payload.
