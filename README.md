# rpi3

## Install nvm
To install nvn do the following

```
sudo apt update -y && sudo apt upgrade -y
git clone https://github.com/creationix/nvm.git ~/.nvm
sudo echo "source ~/.nvm/nvm.sh" >> ~/.bashrc && sudo echo "source ~/.nvm/nvm.sh" >> ~/.profile
```

Close the terminal and repopen it

Check that nvm is installed with `nvm --version`


## Install nodejs
Run the following

`nvm install lts/dubnium`


# Install smbus
Run the following

```
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```

Then open the Raspbian config page with `sudo raspi-config` and enable 
the I2C channel in the Interface Options
To test the I2C run `sudo i2cdetect -y 1`

# Come lanciare il programma
python3 server.py

# Come far partire in automatico il programma al boot
sudo systemctl enable rpi3.service
sudo systemctl start rpi3.service

# Come fare il restart del programma
sudo systemctl restart rpi3.service

# Come verificare lo stato del programma
sudo systemctl status rpi3.service

