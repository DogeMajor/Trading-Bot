apt-get update
apt-get install python-pip -y
apt-get install python-dev -y

pip install numpy
apt-get install python-scipy -y
pip install pandas
#apt-get install python-matplotlib -y #Only needed for visual representation
pip install -U scikit-learn
pip install --upgrade \
https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.1-cp27-none-linux_x86_64.whl

apt-get update
apt-get install firefox -y
apt-get install xvfb firefox -y  #Adds geckodriver below!!!
wget https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz
sh -c 'tar -x geckodriver -zf geckodriver-v0.16.1-linux64.tar.gz -O > /usr/bin/geckodriver'
chmod +x /usr/bin/geckodriver
rm geckodriver-v0.16.1-linux64.tar.gz

apt-get install git -y

pip install selenium
