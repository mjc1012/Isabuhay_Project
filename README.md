# Isabuhay_Project

To deploy this project, follow these steps:
1. Install postgresql from "https://www.postgresql.org/download/"
2. Install pgAdmin from "https://www.pgadmin.org/download/"
3. Create a AWS Account
4. Create a database in Amazon RDS
5. Create a server in pgAdmin
6. Connect the server with your database in Amazon RDS
7. Change the values of the DATABASE dictionary in settings.py to match the values of your database in Amazon RDS
8. if you are having trouble with steps 1-7, watch this video "https://www.youtube.com/watch?v=3HPq12w-dww&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=22"
9. Create a Google Cloud Platform Account
10. Enable Cloud Vision API
11. Create Service Account
12. Create a new key and download the json file
13. If you are having trouble with steps 9-12, watch this video "https://www.youtube.com/watch?v=3HPq12w-dww&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=22"
14. Create an AWS S3 Bucket
15. Get the Bucket name and place that as the value for AWS_STORAGE_BUCKET_NAME in settings.py 
16. Change permission of bucket so it will be accesible
17. Create a new user in Amazon IAM
18. Have add an attachment policy named "AmazonS3FullAccess" to the user
19. Get the user's Access Key Id and Secret Access Key and place those as values for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in settings.py
20. if you are having trouble with steps 14-19, watch this video "https://www.youtube.com/watch?v=3HPq12w-dww&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=22"
21. Upload the project to your Github account
22. Go to Railwapp.app
23. Start a new project 
24. Connect your Github account to Railway
25. Select the github project to deploy
26. Add the generate url from Railway to the lists CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS in settings.py
25. Add the Google Application Credientials as a variable in Railway
26. Deploy the project in Railway
27. if you are having trouble with deploying in Railway, watch this video "https://www.youtube.com/watch?v=do0otUW7454"
28. The admin's username is "admin" and the password is "corral123"

To run this project locally, follow these steps:
1. Follow the steps 1-20 above
2. Add the Google Application Credientials as an environment variable of your pc
3. Install virtual environment. Type in your command prompt "pip install virtualenv"
4. Create a virtual enviroment. Type in your command prompt "virtualenv envName"
5. Activate the virtual environment. Go to the path of the virtual environment in the command prompt then type "Scripts\activate"
6. Install all the libraries in the requirements.txt file. Type in the command prompt "pip install -r requirements.txt"
7. Type in the command prompt "python manage.py runserver"
8. The admin's username is "admin" and the password is "corral123"
