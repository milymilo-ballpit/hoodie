# Hoodie

## Hoodie is a self-hosted IP grabber

> I'm a dev, not a lawyer. Please consult your local laws before deploying. 
> I'm not responsible for your actions in any way whatsoever. Use at own risk.

## Quickstart:

- Pull the project
- Install dependencies - `pipenv install`
- Create .env file from .env.example
  - Get API keys for external services (google maps, shodan, ipinfo)
  - Deploy a Redis Server
  - Configure the database
- Build front-end (w. js info grabber) - `cd ./static/front-end/ && npm i && npm build`
- Continue as usual django deploy (migrate, colectstatic, createsuperuser)
