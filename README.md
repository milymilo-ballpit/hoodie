# Hoodie

## Hoodie is a self-hosted IP grabber

> I'm a dev, not a lawyer. Please consult your local laws before deploying. I'm not responsible for your actions in any way whatsoever. Use at own risk.

So, basically since grabify started displaying a confirmation button before redirection I was in need of a solid IP grabber. This is an effort of 2 long days of intensive engieering. It logs everything I found viable to log, it also consults ipinfo and shodan to retrieve even more information on the target.

WIP, at the moment it needs some interface improvements and more configuration options.

## Quickstart:

- Pull the project
- Install dependencies - `pipenv install`
- Build front-end (w. js info grabber) - `cd ./static/front-end/ && npm i && npm build`
- Continue as usual django deploy (migrate, colectstatic, createsuperuser)

## Usage:

- You can create grab links directly from the admin panel, or at the route /c/ (short for create, to try and avoid detection with directory busting)
- You can also view links and data from the admin panel, or at the route /l/
- At the moment, other actions such as deleting and updating links/entries are only supported via the django admin.
