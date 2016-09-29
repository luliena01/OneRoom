##Rental Room management system

### Framework
- Flask Python3 (http://flask.pocoo.org/docs/0.11)
- Flask-restful (http://flask-restful-cn.readthedocs.io/en/0.3.4/)
- DBMS : PostgreSQL
- DB famework : SQLAlchemy
- front-end framework : Jinja2
- UI framework : Bootstrap SB Admin2
- Form (DTO) framework : wtforms


### Functions

#### Login
- Encrypted password
Encrypt password with sha256_crypt using passlib.hash and compare with enc passsword in users table.

- Authentication using login session
Saving unique user code in session as session['code'].
Every users have Administrator, Tanent or Guest types in Roles table.
Checking authentication decorators on function -> check if user codes in session have admin, tanent or guest authentication in users table.
```
	@guest_auth
	@tenant_auth
	@admin_auth
```
If a user doesn't have a permission, it changes pages to login page.

#### Board
- Hit
Increasing counter when anyone click defail of content and checks sessions to duplicated users not to include the count.

- Naver editor
The editor only supports HTML5 (drag & drop).
Image upload process
```
1. Send img to server
2. Save img in Template/files as rendom id
3. Response url (download img url with id)
```

- Convert images
Converting image files to small size (Thumbnail) using pillow lib.

- Chart
Bill pages shows bills by user and monthly using Morris.js jQuery based charting plugin.


