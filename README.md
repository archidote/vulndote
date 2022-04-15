# Vulndote - Bot

# Installation (Classical)

Add to your ~/.*rc depending of your shell version the following env variables :
```
nano ~/.bashrc 
# OR 
nano ~/.zshrc
```
```
export TELEGRAM_BOT_TOKEN="" # Provide a telegram bot token 
export VULNDOTE_API_USERNAME="" # Provide a opencve.io api user
export VULNDOTE_API_PASSWORD="" # Provide a opencve.io api password
export GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY="" Provide a github token (read only public repository)
```
To save these variable directly in your current shell, run the following command :
```
source .bashrc 
# OR 
source .zshrc
```
Install the required dependencies :

```
python3.X -m pip install -r requirements.txt
```
Once the following dependencies has been installed, you can run the bot with the two commands :

```
python3.X index.py &
```
# Installation with a python virtual environnement (venv) 

## Install python3-venv 
```
user@ubuntuu:~$ sudo apt install python3-venv
```
Add to your ~/.*rc depending of your shell version the following env variables :
```
user@ubuntuu:~$ nano ~/.bashrc 
# OR 
user@ubuntuu:~$ nano ~/.zshrc
```
```
export TELEGRAM_BOT_TOKEN="" # Provide a telegram bot token 
export VULNDOTE_API_USERNAME="" # Provide a opencve.io api user
export VULNDOTE_API_PASSWORD="" # Provide a opencve.io api password
export GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY="" Provide a github token (read only public repository)
```
To save these variable directly in your current shell, run the following command :
```
user@ubuntuu:~$ source .bashrc 
# OR 
user@ubuntuu:~$ source .zshrc
```
## Jump to virtual env

```
user@ubuntuu:~$ cd ~/vulndote
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