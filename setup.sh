#bin bash

sudo apt install python3 -y 
sudo apt install python3-pip -y
sudo python3 -m pip install -U spacy 
python3 -m spacy download en_core_web_sm 
