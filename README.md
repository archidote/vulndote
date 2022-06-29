# Vulndote - Bot

# Installation (Classical)

Add a .env file in the root path of the git project :
```
TELEGRAM_BOT_TOKEN="" # Provide a telegram bot token 
VULNDOTE_API_USERNAME="" # Provide a opencve.io api user
VULNDOTE_API_PASSWORD="" # Provide a opencve.io api password
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY="" Provide a github token (read only public repository)
```
Install the required dependencies :

```
python3.X -m pip install -r requirements.txt
```
Once the following dependencies has been installed, you can run the bot with the two commands :

```
python3.X index.py &
```
# Installation with a python virtual environnement (python venv) 

## Install python3-venv 
```
user@ubuntuu:~$ sudo apt install python3-venv
```
Add a .env file in the root path of the git project :
```
TELEGRAM_BOT_TOKEN="" # Provide a telegram bot token 
VULNDOTE_API_USERNAME="" # Provide a opencve.io api user
VULNDOTE_API_PASSWORD="" # Provide a opencve.io api password
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY="" Provide a github token (read only public repository)
```

## Jump to virtual env

```
user@ubuntuu:~$ cd ~/vulndote
user@ubuntuu:~$ cd ~/vulndote python3 -m venv venv-vulndote
user@ubuntuu:~/vulndote$ source venv-vulndote/bin/activate
(venv-vulndote) user@ubuntuu:~/vulndote$
```
Install the required dependencies into the virtual env :

```
(venv-vulndote) user@ubuntuu:~/vulndote$ python3.X -m pip install -r requirements.txt
```
Once the following dependencies has been installed, you can run the bot with the two commands :

```
(venv-vulndote) user@ubuntuu:~/vulndote$ python3.X index.py &
``` 