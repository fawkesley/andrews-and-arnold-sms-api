# Andrews & Arnold (AAISP) SMS API

This is a Flask application which provides a JSON API for sending SMS messages through [Andrews and Arnold](https://aa.net.uk/telecoms.html).

It simply proxies the [Andrews and Arnold SMS CGI gateway.](https://control.aa.net.uk/sendsms.cgi)

Motivation:

* The CGI gateway only supports username and password which can be used to make calls and rack up large bills. This proxy stores the single copy of the username and password, and allows accessed based on revokable API tokens. A stolen token can only send SMS messages, not make calls.

* The CGI gateway returns HTTP 200 even if there's an error, which offends me.

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
