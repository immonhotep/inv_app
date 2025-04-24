# inv_app

A simple python/django inventory management rest API application

API main functions:

User and authorization:

- User creation, extended modification ( admin only)
- Login and logout
- User  update settings for authenticated users
- Password change option for  authenticated users
- JWT Token authorization, and django session authorization, token creation, and refresh

Iventory Management functions:

- Create, modify, delete categories  ( admin only)
- Create, modify, delete distributors ( admin only)
- Create, modify, delete premises  ( admin only)
- Create, modify, delete items
- Create, modify, delete orders 
- Modify item amount according to the orders automatically



Extra functions:
drf-redesign for nicer browsable api
PyJWT for JWT token management and authorization

API URLS:

| Description | Urls | Methods | Authorization |

| --- | --- |

| API summary | http://127.0.0.1:8000/ | GET, HEAD, OPTIONS | for anybody |

| List, manage users | http://127.0.0.1:8000/manage-user/ | GET, POST, HEAD, OPTIONS | admin only, token or session required |

| Detail, update, and delete users | http://127.0.0.1:8000/manage-user/{int:pk}/ | GET, POST, HEAD, OPTIONS | admin only, token, or session required |

| Update User | http://127.0.0.1:8000/update-user/{int:pk} | GET, PUT, PATCH, HEAD, OPTIONS | authenticated users, token or session required |

| Change password | http://127.0.0.1:8000/change-password/ | PUT, PATCH, OPTIONS | authenticated users, token or session required |

| Obtain JWT auth token | http://127.0.0.1:8000/token/ | POST, OPTIONS | for anybody, user and password will require |

| Refresh JWT auth token | http://127.0.0.1:8000/token/refresh/ | POST, OPTIONS | for anybody, valid refress token will require |

| List, create categories | http://127.0.0.1:8000/category/ | GET, POST, HEAD, OPTIONS | admin only, token or session required |

| Detail, update, delete categories | http://127.0.0.1:8000/category/{slug:slug}/ | GET, PUT, DELETE, HEAD, OPTIONS | admin only, token or session required |

| List, create distributors | http://127.0.0.1:8000/distributor/ | GET, POST, HEAD, OPTIONS | admin only, token or session required |

| Detail, update, delete distributors | http://127.0.0.1:8000/distributor/{slug:slug}/ | GET, PUT, DELETE, HEAD, OPTIONS | admin only, token or session required |

| List, create premises | http://127.0.0.1:8000/premises/ | GET, POST, HEAD, OPTIONS | admin only, token or session required |

| Detail, update, delete premises | http://127.0.0.1:8000/premises/{slug:slug}/ | GET, PUT, DELETE, HEAD, OPTIONS | admin only, token or session required |

| List, create items | http://127.0.0.1:8000/item/ | GET, POST, HEAD, OPTIONS  | authenticated users, token or session required |

| Detail, update, delete items | http://127.0.0.1:8000/item/{slug:slug}/ | GET, PUT, DELETE, HEAD, OPTIONS | authenticated users, token or session required |

| List, create order | http://127.0.0.1:8000/order/ | GET, POST, HEAD, OPTIONS | authenticated users, token or session required |

| Detail, update, delete order | http://127.0.0.1:8000/order/{slug:slug}/ | GET, PUT, DELETE, HEAD, OPTIONS | authenticated users, token or session required |



INSTALLATION:

- Clone the repository  ( git clone https://github.com/immonhotep/inv_app.git )
- Create python virtual environment and activate it ( depends on op system, example on linux: virtualenv venv  and source venv/bin/activate )
- Install the necessary packages and django  ( pip3 install -r requirements.txt )
- Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
- Run the application ( python3 manage.py runserver )





