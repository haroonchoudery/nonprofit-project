**W205 Final Project**

This project aims at providing a way to measure the performance of organizations in non-profit sector.  

Dependencies Requirements:  
pip install Flask  
pip install mysql-connector  
pip install ijson  
pip install lxml  
yum install mysql-server  
yum install mysql  
yum install git  

Environment Requirement:  
Amazon Linux AMI 2016.09.0.20161028 x86_64 HVM GP2  

Database Setup Instructions:  
sh \<path to the nonprofit-project\>/setup_db.sh  

Server Setup Instructions:  
sudo /etc/init.d/mysqld start  
sudo python \<directory to the nonprofit-project\>/src/webapp.py
