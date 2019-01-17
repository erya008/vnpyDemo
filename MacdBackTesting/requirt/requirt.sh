pyenv local 2.7.8
pyenv global 2.7.8
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source  ~/.zshrc
pyenv local anaconda2-4.0.0
sudo mongod &
