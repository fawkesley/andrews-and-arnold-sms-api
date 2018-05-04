# Andrews & Arnold (AAISP) SMS API

## Send an SMS

```
curl -X POST https://<wherever-you-deployed>/api/v1/send/ -H 'Authorization: Bearer <token>' -H "Content-Type: application/json" -d '{"destination": "+447700000000", "message": "hello"}'
```


## Run on heroku

```
heroku config:set VOIP_NUMBER='+44----------'
heroku config:set OUTGOING_VOIP_PASSWORD='<your voip password>'

# comma-separated list of name:token pairs of access tokens
heroku config:set API_TOKENS="pauls-texter:$(uuid)"
```
