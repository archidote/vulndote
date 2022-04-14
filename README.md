# Vulndote - Bot

# Installation 

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
cd assets/ressources/
python3.X -m pip install -r requirements.txt
```
Once the following dependencies has been installed, you can run the bot with the two commands :

```
cd ../../
python3.X index.py &
```