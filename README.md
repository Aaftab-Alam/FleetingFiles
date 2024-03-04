# 📁Fleeting Files

Fleeting Files is a file sharing platform that allows users to create or join existing rooms and share files with each other. The aim of this project is to provide a fast and easy way to share files among multiple users.

## The idea

I came up with the idea for Fleeting Files when I faced a problem in my college lab. I wanted to share some files with my friends, but there was no easy way to do it. All the existing file-sharing services that I tried required me to log in, enter email addresses, or share long URLs or QR codes.   

Sometimes, our teachers wanted to share some files with us in the lab. They would share the files on WhatsApp groups, but to download them on my lab PC, I had to log in to my WhatsApp on the lab PC, which I found really unsafe.   

I needed a simpler, secure and faster solution. This was where the idea for FleetingFiles came from.

## Features

- **File Sharing🚀**: Users can upload any type of file to a room within size limit. Once a file is uploaded, all other users in the room can download that file.
- **Multi-User Rooms👥**: Users can create their own rooms with unique names or join existing ones. All users in a room can share and download files.
- **Room Expiration⏳**: Rooms are automatically deleted from the server after a certain amount of time, making it no longer available to join and download files
- **Secure Access🔒**:  To ensure the security and privacy of shared files, only authorized users will have the ability to download the uploaded files. This feature adds an extra layer of protection, making sure that your files are only accessed by those you trust.

## Example Usage
https://github.com/Aaftab-Alam/FleetingFiles/assets/100439561/297d562b-b550-41c1-b8c8-10d6d6c7c073

## Live Demo
http://13.200.83.177:8000/


## Tech Stack

### Client Side
*HTML, CSS* and *JavaScript* are used to 
implement a user-friendly, minimal and responsive interface where users can create/join room and upload/download files.

### Server Side
**Django :-** Django has been my choice for the backend framework in this application. Django’s ORM has been instrumental in managing database operations efficiently.Its built-in authentication mechanisms have been used to ensure secure access to files.

**SQL** :- SQL has been employed as the database to store user information, room details and file metadata.

**Celery** :- Integrated Celery(a powerful asynchronous job queue), to automatically delete the room after 30 minutes post-creation. It runs in the background and takes off the load from our django app.

**Redis** :- Used as a message broker, to facilitate the communication between Django application and Celery Worker.

**Whitenoise**:- Used to deliver static content as Django server could not serve static files in production environment.

 ### Cloud Technologies
**AWS S3** :- Utilized S3 buckets to store user uploaded files.These files are securely stored and can only be accessed through presigned URLs. These URLs are generated on-demand when a user initiates a download. To enhance security and prevent unauthorized access, these URLs are designed to expire swiftly - just 10 seconds after the download button is clicked.  
Files also directly transferred from Amazon S3 to user. This bypasses the Django server entirely during the file transfer process, significantly reducing the server load.

**AWS EC2** :- Lastly, I deployed the application on AWS EC2, ensuring its accessibility over the internet.

### Development Tools and Practices
**Ruff** :- I used ruff as a quality check tool. It helped maintain the quality of the code by identifying potential issues and suggesting improvements.

**Virtual Environments** :- To manage dependencies and ensure consistency across different stages of development, virtual environments were used. This practice isolated the project’s environment and kept it clean and organized.

**Git** :- was used for source code management. It allowed efficient handling of project versions and ensured the integrity and consistency of the project.

**Environment Variables**:- environment variables were used to handle sensitive data.This practice ensured that confidential information, such as secret keys and database credentials, were kept safe and not exposed in the codebase.





## Run Locally

To get this project up and running you should start by installing Python on your computer. It's advised you create a virtual environment to store the dependencies of your project separately. You can install virtualenv with

```bash
  pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (windows/mac/linux) or windows terminal, run the following command in the base directory of this project

```bash
  virtualenv env
```

That will create a new folder env in your project directory. Next, activate it with this command on windows:

```bash
  env\Scripts\activate
```

Then install the project dependencies with

```bash
  pip install -r requirements.txt
```
Make necessary migrations
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```
Now you need to create a ***.env*** file in the base directory and configure these environment variables:-  
***access_key***=YOUR_AMAZON_ACCESS_KEY  
***secret_key***=YOUR_AMAZON_SECRET_KEY  
***bucket_name***=YOUR_S3_BUCKET_NAME  
***django_secret_key***=YOUR_DJANGO_SECRET_KEY  
***DJANGO_SETTINGS_MODULE***=FleetingFiles.settings.local  

Now you can run the project with this command
```bash
  python manage.py runserver
```

