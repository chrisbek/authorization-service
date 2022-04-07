# Authorization Server
A simple, insecure authorization server, partly compatible with the OAuth2.0 protocol, that can be used for 
local testing as part of a set of microservices.
Read the full docs at: [authentication-as-a-service](https://christopher.bekos.click/portfolio/authentication-as-a-service).


## Technical notes
### Key generation
Generate a public/private key set (usually called a "key pair") for the application to use. 
There are a few different ways to generate RSA keys, but one that I like is to use the ssh-keygen tool from openssh:
```
ssh-keygen -t rsa -b 4096 -m pem
```
Enter `keys/key` when asked for the keys' location.

### Running migrations
- Run `poetry shell`
- Preview migration:
```
scripts/migrations.sh migrations preview
```
- Create migration:
```
scripts/migrations.sh migrations create
```
- Apply migration:
```
scripts/migrations.sh migrations migrate
```
