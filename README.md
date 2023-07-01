# Collabforum_with-loadbalancer
This collaboration forum is made using django framework connected to a Postgresql database.
Here, Postgresql database acts as central database server where the backend servers are connected to it, whose connection is specified in their settings file.
Do not forget to make changes in the postgresql config files to allow the backend servers to make connection to it.
Note: This master-slave architecture of loadbalancers, backend servers and central database server is not for windows but you can run the servers along with database on windows. 
Moreover for linux, I have also added a playbook for configuring the django servers as backend servers and also for configuring the loadbalancer using haproxy whose configuration file is added here as well.
You will also need to add a file on /etc/system/system/ which is by the name django.service (which i have added, make changes in it accordingly) for making django service run by systemd. 
Rest will be taken care by the Playbook.
Take care and happy learning...
