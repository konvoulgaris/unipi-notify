# unipi-notify
A service that notifies you when new grades are released.

## Table of Contents
* [Example e-mail](#example-e-mail)
* [Quick start](#quick-start)
    * [Requirements](#Requirements)
    * [Configuration](#configuration)
    * [Execution](#execution)
* [Contributing](#contributing)
* [Testing](#testing)
* [Credits](#credits)

## Example e-mail
![Image of e-mail](./images/example_email.png)

## Quick start
This section will show you how to install and run the program.

### Requirements
Make sure you have everything that is mentioned below installed before proceeding to the next step.

```
- docker
- docker-compose
- Google account (or some SMTP service)
```

### Configuration

Open the `docker-compose.yaml` file and locate the environment settings of `unipi-notify` (Starts at line 15).

Change the values of the environment variables and proceed to the next step!

#### Example Configuration

```docker-compose.yaml
version: '3.7'

services:
    unipi-students-api:
        image: konvoulgaris/unipi-students-api
        container_name: unipi-students-api
        restart: always
        ports:
            - 8080:8080
    unipi-notify:
        build: .
        container_name: unipi-notify
        restart: always
        environment:
            - PATH_PREFIX=/usr/src/unipi-notify/
            - API_URL=unipi-students-api
            - REFRESH=30
            - USERNAME=E12345
            - PASSWORD=unipi-password
            - SMTP_ADDRESS=smtp.gmail.com
            - SMTP_SSLPORT=465
            - SMTP_EMAIL=example@gmail.com
            - SMTP_PASSWORD=app-password
        depends_on:
            - unipi-students-api
        volumes:
        - data:/usr/src/unipi-notify/

volumes:
    data:
```

#### Note
+ If you have a Google (Gmail/YouTube) account, you have a access to a [free (although basic) SMTP server](https://support.google.com/a/answer/176600?hl=en).
+ If you use the above-mentioned SMTP server, you will need to create an app password from your [Google account security page](https://myaccount.google.com/apppasswords) and use that as your password later on.
***

### Execution
After doing that, simply run the program using:

```
docker-compose up
```

And... that's it!

(In case you change the environemnt variables after a while, don't forget to rebuild with `docker-compose up --build`.)

## Contributing
Contributions are welcome! Feel free to open an issue or pull requests at any time.

## Testing
While this program was only tested on an Ubuntu 20.04 LTS system, this should run on all platforms that support Docker containers.

## Credits
### Thanks
Special thanks to [Nikos Sklavounos](https://github.com/NickSklA) for creating the [API](https://github.com/NickSklA/unipi-students-api).

### Disclaimer
This service is neither affiliated nor endorsed in any way by the University of Piraeus.
