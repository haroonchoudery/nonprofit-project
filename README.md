**W205 Final Project**

This project aims at providing a way to measure the performance of organizations in non-profit sector.  

Running Environments:  
Amazon Linux AMI 2016.09.0.20161028 x86_64 HVM GP2 

Dependencies:  
pip install Flask  
pip install mysql-connector  
pip install ijson  
pip install lxml  
yum install mysql-server  
yum install mysql  
yum install git   

Prerequisites Beforing Starting the Application:  
To avoid permission issues, we recommend you to run this app as root. We also assume that you setup the mysql server at the same host.  
sudo bash  
mkdir -p /var/log/nonprofit  
/etc/init.d/mysqld start  
cd \<path to the nonprofit-project\>  
source export_paths.sh  

For the first time running, please also populate the databse. This script will populate your database with 500 items by default:  
sh setup_db.sh  

Run the Application. It will use port 80 by default:  
python \<directory to the nonprofit-project\>/src/webapp.py  

Smoke Check:  
curl localhost/status
It is working!
