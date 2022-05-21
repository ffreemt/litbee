# curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
# source .bashrc
# nvm install node
# curl -sL https://deb.nodesource.com/setup_12.x | bash -
wget -c https://deb.nodesource.com/setup_12.x
bash setup_12.x

apt-get install -y nodejs
npm install -g npm@latest
npm install -g nodemon