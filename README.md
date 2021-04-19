# [Forum (Blog)](https://chengccassgn1.ue.r.appspot.com) deployed in Google App Engine

## Team
Shuo Wang  
Qixiang Cheng

## Info
This is a web application based on python in Flask for a public forum(blog), which connects to the NoSql database in Google Datastore and Google bucket. The website was designed by flask-WTF with the constraint of input account number, account password, upload images and so forth. Besides, users can check the newest relavent posted information, check personal information and modify password.

## It includes the following functions of customer:
### Login/register
Login/logout change the password for the user with the session which is recordered by the server.  
the login information(account number and password) was saved in the google datastore.

### My statement(User page):
Check personal message that is posted in the forum and be available to modify it.

### Forum page:
Be able to check all the details information that is posted by all the users with the most popular 10 ones. It also all people to push massage to the forum with subject, message and image.
image will be saved into Google Bucket.


