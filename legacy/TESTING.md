# TESTING.md
## Testing

### Manual testing

A series of manual tests were undertaken to determine api viability, and test to see if the user 
got the correct details back, as well as this we double and triple checked every endpoint to make 
sure the user needs authentication to access any of these endpoints

|                 TEST                  |              Expected outcome              |              Actual outcome               | Pass/Fail |
| :-----------------------------------: | :----------------------------------------: | :---------------------------------------: | :-------: |
|     POST /auth/register (valid)      | 201 Created, user object, email sent       | 201 Created, user object, email sent      |   Pass    |
|   POST /auth/register (invalid)      | 400 Bad Request, validation errors         | 400 Bad Request, validation errors        |   Pass    |
|    POST /auth/login (valid creds)    | 200 OK, JWT token returned                 | 200 OK, JWT token returned                |   Pass    |
|  POST /auth/login (invalid creds)    | 401 Unauthorized, error message            | 401 Unauthorized, error message           |   Pass    |
| POST /auth/login (unverified email)  | 403 Forbidden, verification prompt         | 403 Forbidden, verification prompt        |   Pass    |
|         POST /auth/logout            | 200 OK, token invalidated                  | 200 OK, token invalidated                 |   Pass    |
|      POST /auth/verify-email         | 200 OK, user status updated                | 200 OK, user status updated               |   Pass    |
| POST /auth/resend-verification       | 200 OK, verification email sent            | 200 OK, verification email sent           |   Pass    |
|          GET /users/me               | 200 OK, user profile returned              | 200 OK, user profile returned             |   Pass    |
|     PATCH /users/me (valid data)     | 200 OK, profile updated                    | 200 OK, profile updated                   |   Pass    |
|   PATCH /users/me (invalid data)     | 400 Bad Request, validation errors         | 400 Bad Request, validation errors        |   Pass    |
|          DELETE /users/me            | 204 No Content, user deleted               | 204 No Content, user deleted              |   Pass    |
|            GET /servers              | 200 OK, list of servers                    | 200 OK, list of servers                   |   Pass    |
|    POST /servers (valid data)        | 201 Created, server returned               | 201 Created, server returned              |   Pass    |
| POST /servers (duplicate name)       | 409 Conflict, error message                | 409 Conflict, error message               |   Pass    |
|   PATCH /servers/:id (is owner)      | 200 OK, server updated                     | 200 OK, server updated                    |   Pass    |
| PATCH /servers/:id (not owner)       | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|  DELETE /servers/:id (is owner)      | 204 No Content, server deleted             | 204 No Content, server deleted            |   Pass    |
| DELETE /servers/:id (not owner)      | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|     GET /servers/:id/channels        | 200 OK, list of channels                   | 200 OK, list of channels                  |   Pass    |
|  POST /channels (admin permission)   | 201 Created, channel returned              | 201 Created, channel returned             |   Pass    |
| POST /channels (no admin rights)     | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
| PATCH /channels/:id (admin)          | 200 OK, channel updated                    | 200 OK, channel updated                   |   Pass    |
| PATCH /channels/:id (not admin)      | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
| DELETE /channels/:id (admin)         | 204 No Content, channel deleted            | 204 No Content, channel deleted           |   Pass    |
| DELETE /channels/:id (not admin)     | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|           GET /categories            | 200 OK, list of categories                 | 200 OK, list of categories                |   Pass    |
|     GET /categories/{id}            | 200 OK, category details                   | 200 OK, category details                  |   Pass    |
| GET /servers?category=xyz            | 200 OK, filtered servers returned          | 200 OK, filtered servers returned         |   Pass    |
|       GET /protected (no auth)       | 401 Unauthorized, error message            | 401 Unauthorized, error message           |   Pass    |
| GET /admin-only (user role)          | 403 Forbidden, access denied               | 403 Forbidden, access denied              |   Pass    |
|      GET /unknown-route              | 404 Not Found, error message               | 404 Not Found, error message              |   Pass    |
|     API error returns JSON object    | Proper JSON error message                  | Proper JSON error message                 |   Pass    |
|      Rate limit exceeded             | 429 Too Many Requests, rate error          | 429 Too Many Requests, rate error         |   Pass    |
|        CORS headers present          | Access-Control-Allow-Origin in headers     | Access-Control-Allow-Origin in headers    |   Pass    |
|  All endpoints require auth (secure) | 401 Unauthorized for unauthenticated users | 401 Unauthorized for unauthenticated users|   Pass    |
| GET /api/account/me/                 | 200 OK, user data returned                 | 200 OK, user data returned                |   Pass    |
| PATCH /api/account/edit_me/          | 200 OK, user updated                       | 200 OK, user updated                      |   Pass    |
| GET /api/account/my_servers/         | 200 OK, servers returned                   | 200 OK, servers returned                  |   Pass    |
| POST /api/account/password_reset/    | 200 OK, email sent                         | 200 OK, email sent                        |   Pass    |
| POST /api/account/password_reset_confirm/ | 200 OK, password updated             | 200 OK, password updated                  |   Pass    |
| POST /api/account/register/          | 201 Created, email sent                    | 201 Created, email sent                   |   Pass    |
| POST /api/account/resend_verification/| 200 OK, email sent                        | 200 OK, email sent                        |   Pass    |
| GET /api/account/verify_email/       | 200 OK, email verified                     | 200 OK, email verified                    |   Pass    |
| GET /api/channels/                   | 200 OK, list of channels                   | 200 OK, list of channels                  |   Pass    |
| POST /api/channels/                  | 201 Created, new channel                   | 201 Created, new channel                  |   Pass    |
| GET /api/channels/{id}/             | 200 OK, channel details                    | 200 OK, channel details                   |   Pass    |
| PUT /api/channels/{id}/             | 200 OK, full update                        | 200 OK, full update                       |   Pass    |
| PATCH /api/channels/{id}/           | 200 OK, partial update                     | 200 OK, partial update                    |   Pass    |
| DELETE /api/channels/{id}/          | 204 No Content, channel deleted            | 204 No Content, channel deleted           |   Pass    |
| GET /api/docs/schema/                | 200 OK, schema returned                    | 200 OK, schema returned                   |   Pass    |
| GET /api/messages/                   | 200 OK, list of messages                   | 200 OK, list of messages                  |   Pass    |
| GET /api/messages/{id}/             | 200 OK, message details                    | 200 OK, message details                   |   Pass    |
| PATCH /api/messages/{id}/           | 200 OK, message updated                    | 200 OK, message updated                   |   Pass    |
| GET /api/servers/                    | 200 OK, list of servers                    | 200 OK, list of servers                   |   Pass    |
| POST /api/servers/                   | 201 Created, new server                    | 201 Created, new server                   |   Pass    |
| GET /api/servers/{id}/              | 200 OK, server details                     | 200 OK, server details                    |   Pass    |
| PUT /api/servers/{id}/              | 200 OK, full update                        | 200 OK, full update                       |   Pass    |
| PATCH /api/servers/{id}/            | 200 OK, partial update                     | 200 OK, partial update                    |   Pass    |
| DELETE /api/servers/{id}/           | 204 No Content, server deleted             | 204 No Content, server deleted            |   Pass    |
| POST /api/servers/{id}/add_member/   | 200 OK, member added                       | 200 OK, member added                      |   Pass    |
| POST /api/servers/{id}/remove_member/| 200 OK, member removed                     | 200 OK, member removed                    |   Pass    |
| POST /api/token/                     | 200 OK, access and refresh tokens returned | 200 OK, access and refresh tokens returned|   Pass    |
| POST /api/token/refresh/            | 200 OK, new access token returned          | 200 OK, new access token returned         |   Pass    |




### Automated tests

Automated testing took place throughout the app, I wrote tests to make sure that the code would fail and then kept testing it until it passed this ensured
that the code was able to do everything I wanted it to do. The only thing i couldn't test as thoroughly was websockets, so instead i used [WebSocket King]() to test
the connection endpoint


### Python validation

All files were validated via pep8 standards and came out okay with no critical errors

![Validation](validation.png)

There were only a few files that had minor style issues, which was due to my setup of vscode, the issues being they were too long, (more than 79 chars) when changing the breakpoint these issues automatically resolved themselves


### Bugs

To date there are no bugs in the backend code, all api endpoints work correctly and the code base is solid and allows the user to acccess the app with no problems

*to note the related front end race condition problem may result in how i setup my usermode but this is unconfirmed so i shall leave that as a fronend issue