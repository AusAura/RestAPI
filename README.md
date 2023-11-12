# RestAPI-JWT-ContactBook
RESTful API built with FastAPI, based on Postgres (SQLAlchemy) + Redis (cache). Both are configured with Docker Compose. 

Contact book with adding, reading, patching, deleting and closest-birthday-calculating functions.

- Tests: Unittest + Pytest. 
- Docs: Sphinx.

1) Authorization and authentication with JWT tokens.
2) FastAPILimiter and SlowAPI to limit number of requests.
3) Pydantic for data validation.
4) App sends verification and reset password emails.
5) Not possible to login without verifying the user via email.
6) Most of the functionality is not available without authentication.
7) Redis used to cache some most common DB requests.
8) Alembic for migrations.

## Functionality:

### email
**1) GET /api/email/confirm/{email_token}**

Confirmed Email -
No more than 10 requests per minute

Parameters:

**email_token** * 
string
	
Responses:

200:
Successful Response
"string"

422:
Validation Error

### contacts
**2) GET /api/contacts/**

Read Contacts -
No more than 10 requests per minute

Parameters:

**skip** -
integer -
Default value : 0

**limit** -
integer -
Default value : 20

Responses:

200:
Successful Response
[
  {
    "fullname": "string",
    "email": "string",
    "phone_number": 0,
    "birthday": "2023-11-12",
    "additional": "string",
    "user_id": 0,
    "avatar": "string"
  }
]


422:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**3) POST /api/contacts/**

Create Contact -
No more than 2 requests per minute

Parameters:
...

Request body:
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

Responses:

201	:
Successful Response
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

**4) GET /api/contacts/bd**

Check Birthdays -
No more than 10 requests per minute

Parameters:

**days_range**
integer
Default value : 7

Responses:

200	:
Successful Response
[
  {
    "fullname": "string",
    "email": "string",
    "phone_number": 0,
    "birthday": "2023-11-12",
    "additional": "string",
    "user_id": 0,
    "avatar": "string"
  }
]


422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**5) GET /api/contacts/{query}**

Read Contact -
No more than 10 requests per minute

Parameters:

**query** *
string

	
Responses:

200	:
Successful Response
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**6) PUT /api/contacts/{contact_id}**
Update Contact
No more than 10 requests per minute

Parameters:

**contact_id** *
integer
	
Request body:
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

Responses:

200	:
Successful Response
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**7) DELETE /api/contacts/{contact_id}**

Remove Contact -
No more than 10 requests per minute

Parameters:

**contact_id** *
integer
	
Responses:

200	:
Successful Response
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**8) PATCH /api/contacts/{contact_id}/avatar**

Update Avatar Contact

Parameters:

**contact_id** *
	
Request body:
file *
string($binary)
	
Responses:

200	:
Successful Response
{
  "fullname": "string",
  "email": "string",
  "phone_number": 0,
  "birthday": "2023-11-12",
  "additional": "string",
  "user_id": 0,
  "avatar": "string"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

### auth
**9) POST /api/auth/signup**

Signup -
No more than 2 requests per minute

Parameters:
...

Request body:
{
  "username": "string",
  "password": "string",
  "email": "string"
}

Responses:

201	:
Successful Response
{
  "user": {
    "id": 0,
    "username": "string",
    "email": "string",
    "created_at": "2023-11-12T16:29:48.633Z"
  },
  "detail": "Successfully created"
}

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}


**10) POST /api/auth/login**

Login -
No more than 10 requests per minute

Parameters:
...

Request body:

grant_type
	
username *
string
	
password *
string
	
scope
string
	
client_id
	
client_secret
	
Responses:

200	:
Successful Response
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}


422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

**11) GET /api/auth/refresh_token**

Refresh Token -
No more than 10 requests per minute

Parameters:
...

Responses:

200	:
Successful Response
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}

**12) POST /api/auth/request_email**

Request Email -
No more than 2 requests per minute

Parameters:
...

Request body:
{
  "email": "user@example.com"
}

Responses:

200	:
Successful Response
"string"

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

**13) POST /api/auth/reset_pwd**

Reset Pwd -
No more than 2 requests per minute

Parameters:
...

Request body:
{
  "email": "user@example.com"
}

Responses:

200	:
Successful Response
"string"

422	:
Validation Error
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

# Docs:
## REST API repository Contacts

async src.repository.contacts.create_contact(body: ContactModel, user: User, db: Session) → Contact

    Creates a new contact.

    Parameters:

            body – Data for contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

async src.repository.contacts.get_contact(query: str, user: User, db: Session) → Contact

    Shows one contact for user

    Parameters:

            query (str) – A part of fullname or email address that is used for query to find the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

async src.repository.contacts.get_contacts(skip: int, limit: int, user: User, db: Session) → List[Contact]

    Shows full list of contacts for user

    Parameters:

            skip (int) –

            limit (int) –

            user (User) –

            db (Session) –

    Return type:

        List[Contact]

async src.repository.contacts.get_upcoming_birthdays(days_range: int, user: User, db: Session) → List[Contact]

    Checks the birthdays in the set range but only to the end of the year.

    Parameters:

            days_range – A range in which bdays will be shown. If days_range > days left until the end of the year, it will search only until the end of it.

            user (User) –

            db (Session) –

    Return type:

        List[Contact]

async src.repository.contacts.remove_contact(contact_id: int, user: User, db: Session) → Contact | None

    Removes the contact by contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact | None

async src.repository.contacts.update_avatar(contact_id: int, url: str, db: Session) → Contact | None

    Updates the avatar URL for contact with contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            url (str) – An URL for the avator on the cloud server..

            db (Session) –

    Return type:

        Contact | None

async src.repository.contacts.update_contact(contact_id: int, body: ContactModel, user: User, db: Session) → Contact | None

    Updates the contact by contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            body – Data for the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact | None

## REST API repository Users

async src.repository.users.confirmed_email(email: str, db: Session) → User

    Confirms email for the user. Empty if not found.

    Parameters:

            token – User email that should be confirmed.

            db (Session) –

    Return type:

        User | []

async src.repository.users.create_user(body: UserModel, db: Session) → User

    Creates the user with the passed data. Empty if fails.

    Parameters:

            body (UserModel) – The passed data.

            db (Session) –

    Return type:

        User | []

async src.repository.users.get_user_by_email(email: str, db: Session) → User

    Returns user that have that email. Empty if fails.

    Parameters:

            email (str) – The email of the user.

            db (Session) –

    Return type:

        User | []

async src.repository.users.update_token(user: User, token: str | None, db: Session) → User

    Refresh token for the user.

    Parameters:

            user (User) – The user.

            token (str) – The passed token value.

            db (Session) –

    Return type:

        User

## REST API routes Contacts

async src.routes.contacts.check_birthdays(request: Request, days_range: int = 7, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Checks the birthdays in the set range but only to the end of the year.

    Parameters:

            days_range – A range in which bdays will be shown. If days_range > days left until the end of the year, it will search only until the end of it.

            user (User) –

            db (Session) –

    Return type:

        List[Contact]

async src.routes.contacts.create_contact(request: Request, body: ContactModel, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Creates a new contact.

    Parameters:

            body – Data for contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

async src.routes.contacts.read_contact(request: Request, query: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Shows one contact for user

    Parameters:

            query (str) – A part of fullname or email address that is used for query to find the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

async src.routes.contacts.read_contacts(request: Request, skip: int = 0, limit: int = 20, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Shows full list of contacts for user

    Parameters:

            skip (int) –

            limit (int) –

            user (User) –

            db (Session) –

    Return type:

        List[Contact]

async src.routes.contacts.remove_contact(request: Request, contact_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Removes the contact by contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

async src.routes.contacts.update_avatar_contact(request: Request, contact_id, file: UploadFile = File(PydanticUndefined), current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Updates the avatar URL for contact with contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            url (str) – An URL for the avator on the cloud server..

            db (Session) –

    Return type:

        Contact | None

async src.routes.contacts.update_contact(request: Request, body: ContactModel, contact_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db))

    Updates the contact by contact_id. Returns None if contact with contact_id does not exist.

    Parameters:

            contact_id (int) – The ID of the contact.

            body – Data for the contact.

            user (User) –

            db (Session) –

    Return type:

        Contact

## REST API routes Auth

async src.routes.auth.login(body: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db))

async src.routes.auth.refresh_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer), db: Session = Depends(get_db))

    Get new access token for user. Or null current refresh token in DB if the one that sent is outdated.

    Parameters:

            credentials (HTTPAuthorizationCredentials) – Data for ‘Authorization’ header that includes ‘Bearer’ and the token.

            db (Session) –

    Return type:

        JSON

async src.routes.auth.request_email(body: RequestEmail, db: Session = Depends(get_db))

    Request for new verification email. Sends it or denies attempt if already confirmed.

    Parameters:

            body (RequestEmail) – A class that contains .email (and possibly something else)

            db (Session) –

    Return type:

        JSON

async src.routes.auth.reset_pwd(body: RequestEmail, db: Session = Depends(get_db))

    Sends an email with reset password. Denies if user does not exist. Requires email address.

    Parameters:

            body (RequestEmail) – A class that contains .email of the user (and possibly something else)

            db (Session) –

    Return type:

        JSON

async src.routes.auth.signup(body: UserModel, db: Session = Depends(get_db))

    Signup user.

    Parameters:

            body (UserModel) – The passed data for signup.

            db (Session) –

    Return type:

        JSON

## REST API routes Email

async src.routes.email.confirmed_email(email_token: str, db: Session = Depends(get_db))

    Confirms email for the user that owns that email_token. Denies if already confirmed.

    Parameters:

            email_token (str) – The email token that was generated in the verification email for the user.

            db (Session) –

    Return type:

        JSON

## REST API service Auth

class src.services.auth.Auth

    Bases: object

    ALGORITHM = 'HS256'

    SECRET_KEY = 'Some_key'

    async create_access_token(data: dict, expires_delta: float | None = None) → str

        Generate new access token.

        Parameters:

                data (dict) – Passed data (email of the user).

                expires_delta (float | None) – Optional TTL.

        Return type:

            str

    async create_email_token(data: dict, expires_delta: float | None = None) → str

        Generate new email token.

        Parameters:

                data (dict) – Passed data (email of the user).

                expires_delta (float | None) – Optional TTL.

        Return type:

            str

    async create_refresh_token(data: dict, expires_delta: float | None = None) → str

        Generate new refresh token.

        Parameters:

                data (dict) – Passed data (email of the user).

                expires_delta (float | None) – Optional TTL.

        Return type:

            str

    async decode_refresh_token(refresh_token: str)

        Decode refresh token and return the user’s email. Raise errors if invalid token or scope.

        Parameters:

            refresh_token (str) – Passed token.
        Return type:

            str

    async get_current_user(token: str = Depends(OAuth2PasswordBearer), db: Session = Depends(get_db))

        Decode access token and return the user. Raise errors if invalid token or scope, wrong email or user. Stores the request for user in Redis cache.

        Parameters:

            token (str) – Passed token.
        Return type:

            User

    async get_email_from_token(email_token: str) → str

        Decode email token and returns it. Raise errors if unprocessable token.

        Parameters:

            token (str) – Passed token.
        Return type:

            str

    get_password_hash(plain_password: str) → str

        Encrypts the password during signup.

        Parameters:

            plain_password (str) – Recieved password.
        Return type:

            str

    oauth2_scheme = <fastapi.security.oauth2.OAuth2PasswordBearer object>

    pwd_context = <CryptContext>

    r = Redis<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

    async reset_password(email: str, email_token: str, db: Session) → None

        Create (on inner algorithm) and set new password for the user in DB. Raise error if user with passed email not found.

        Parameters:

                email (str) – Passed email of the user.

                email_token – Passed email token.

                db (Session) –

        Return type:

            None

    verify_password(plain_password: str, hashed_password: str) → bool

        Verify the password during loging.

        Parameters:

                plain_password (str) – Recieved password.

                hashed_password (str) – Stored encrypted password.

        Return type:

            bool

## REST API service Email

class src.services.email.EmailSchema(*, email: EmailStr)

    Bases: BaseModel

    email: EmailStr

    model_config: ClassVar[ConfigDict] = {}

        Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

    model_fields: ClassVar[dict[str, FieldInfo]] = {'email': FieldInfo(annotation=EmailStr, required=True)}

        Metadata about the fields defined on the model, mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

        This replaces Model.__fields__ from Pydantic V1.

async src.services.email.send_reset(email: str, username: str) → str

    Generates mew password for the user. Sends email to his email address with the new password.

    Parameters:

            email (str) – The email address of the user.

            username (str) – The username.

    Return type:

        bool

async src.services.email.send_verification(body: str, username: str) → bool

    Generates email token for the user, then makes email with it, passes the data to the template. At the end, sends a verification letter to the user’s email.

    Parameters:

            body (str) – The email address of the user.

            db (Session) –

    Return type:

        bool

