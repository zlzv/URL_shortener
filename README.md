# URL Shortener

### API Methods

#### Errors
-------------

```json
{
	"err": 3,
	"msg": "Wrong username or password"
}
```
- 1 - Unknown error
- 2 - Missing parameter in request
- 3 - Wrong username or password
- 4 - Link does not exist
- 5 - Links not found


#### Authentication
-------------
###### `POST api/auth`
Returns JSON web token (JWT)

| Parameter  | Example |
| ------------- | ------------- |
| username  | admin  |
| password  | 12345  |

###### Response
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImV4cCI6MTU1NTYxNjkyNiwiaWF0IjoxNTU1NjE2MDI2LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTU1NjE2MDI2LCJpZGVudGl0eSI6MTAwMDEsImp0aSI6IjYyMmMzOTlmLTI4MjgtNGVlNy1hNWNiLTc5MmFjODU0MWMzYiIsInVzZXJfY2xhaW1zIjp7InVzZXJfaWQiOjEwMDAxfX0.b1d1wr-o-JvKjwsFNfsiJBiWqDJ-vI-Kb-vaxhHKSBw"
}
```

#### Registration
-------------
###### `POST api/join`


| Parameter  | Example |
| ------------- | ------------- |
| username  | Ivan  |
| password  | 12345  |

###### Response
```json
{
  "success": "true",
  "msg": "User has been successfully registered"
}
```

#### Create a short link
-------------
###### `POST api/short`

| Parameter  | Example |
| ------------- | ------------- |
| url  | example.com  |

Header: "Authorization: Bearer {JWT}"

###### Response
```json
{
  "short": "url-shortener.domain/2Wc",
  "long": "example.com",
  "url_end": "2Wc"
}
```

#### Get information about a link
-------------
###### `POST api/info`

| Parameter  | Example |
| ------------- | ------------- |
| url_end  | 2Wc  |

Header: "Authorization: Bearer {JWT}"

###### Response
```json
{
  "short": "url-shortener.domain/2Wc",
  "long": "example.com",
  "views": 3,
  "created_at": "Sun, 14 Apr 2019 23:40:47 GMT"
}
```

#### Get all links belongs to a user
-------------
###### `POST api/all`

| Parameter  | Example |
| ------------- | ------------- |
| -  | -  |

Header: "Authorization: Bearer {JWT}"

###### Response
```json
{
  "data": [
    {
      "short": "url-shortener.domain/2Wc",
	  "long": "example.com",
	  "created_at": "Sun, 14 Apr 2019 23:40:47 GMT",
      "views": 3
    },
    {
      "short": "url-shortener.domain/2Be",
	  "long": "example.com/abc",
	  "created_at": "Sun, 14 Apr 2019 23:21:58 GMT",
      "views": 0
    }
  ]
}
```

#### Delete a link
-------------
###### `POST api/delete`

| Parameter  | Example |
| ------------- | ------------- |
| url_end  | 2Wc  |

Header: "Authorization: Bearer {JWT}"

###### Response
```json
{
  "success": "true",
  "msg": "Link has been successfully deleted"
}
```
