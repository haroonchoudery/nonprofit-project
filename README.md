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

Prerequisites Beforing Starting the Application:  
sudo bash  
mkdir -p /var/log/nonprofit  
/etc/init.d/mysqld start  
cd \<path to the nonprofit-project\>  
source export_paths.sh  
sh setup_db.sh  

Run the Application:  
python \<directory to the nonprofit-project\>/src/webapp.py
