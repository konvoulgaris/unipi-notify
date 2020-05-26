# unipi-notify
A service that notifies you when new grades are released.

## Table of Contents
***
* [Example e-mail](#example-e-mail)
* [Quick start](#quick-start)
    * [Requirements](#Requirements)
    * [Edit configuration files](#edit-configuration-files)
    * [Example configuration files](#example-configuration-files)
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

### Edit configuration files
Go to the config folder and rename  
`smtp.example.json -> smtp.json`  
and  
`user.example.json -> user.json`  
with the details of your SMTP server and Unipi account respectively.

#### Note
+ If you have a Google account, you have a [free basic SMTP server](https://support.google.com/a/answer/176600?hl=en) already included.
+ If you use the above-mentioned SMTP server, you will need to create an app password from your [Google account security page](https://myaccount.google.com/security) and use that as your password.

***

### Example configuration files (Google account)
Your configuration files should look like this.

*smtp.json*
```json
{
    "address": "smtp.gmail.com",
    "ssl_port": 465,
    "email": "john@gmail.com",
    "password": "app password"
}
```
*user.json*
```json
{
    "username": "E12345",
    "password": "unipi password"
}
```

***

After doing that, simply run the app using:

```
sudo docker-compose up
```

And... that's it!

## Testing
While this was only tested on an Ubuntu 20.04 LTS system, this should run on all platform thanks to Docker.

## Credits
### Thanks
Special thanks to [Nikos Sklavounos](https://github.com/NickSklA) for creating the API.

### Disclaimer
This service is neither affiliated nor endosered in any way by the University of Piraeus. This was created solely for convience purposes.
