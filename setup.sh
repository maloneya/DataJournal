#bin bash

sudo apt install python3 -y 
sudo apt install python-pip -y
sudo pip install -U spacy -y
python -m spacy download en_core_web_sm 
