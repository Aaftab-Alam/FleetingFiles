
# 📁Fleeting Files (WIP)

FleetingFiles is a file-sharing platform that lets you share files with multiple users in a matter of seconds. No need to log in, sign up, or enter your email address. Just create or join a room, set a password, and invite your friends. You can upload and download any file you want, as long as it is within the room’s size limit. Fleeting Files is perfect for situations where you need to quickly share files with others, such as in a college lab, a group project, or a work meeting. Fleeting Files is fast, easy, and secure.

## The idea

I came up with the idea for Fleeting Files when I faced a problem in my college lab. I wanted to share some files with my friends, but there was no easy way to do it. All the existing file-sharing services required me to log in, enter email addresses, or share long URLs or QR codes.   

Sometimes, our teachers wanted to share some files with us in the lab. They would share the files on WhatsApp groups, but to download them on my lab PC, I had to log in to my WhatsApp on the lab PC, which I found really unsafe.   

I needed a simpler, secure and faster solution. This was where the idea for FleetingFiles came from.

## Features

- **File Sharing🚀**: Users can upload any type of file to a room. Once a file is uploaded, all other users in the room can download that file.
- **Multi-User Rooms👥**: Users can create their own rooms or join existing ones. All users in a room can share and download files.
- **Room Expiration⏳**: Rooms are automatically deleted from the server along with all its files after a certain amount of time, making them no longer available for download.


## Run Locally

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```bash
  pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (windows/mac/linux) or windows terminal, run the following command in the base directory of this project

```bash
  virtualenv env
```

That will create a new folder env in your project directory. Next activate it with this command on windows:

```bash
  env\Scripts\activate
```

Then install the project dependencies with

```bash
  pip install -r requirements.txt
```

Now you can run the project with this command
```bash
  python manage.py runserver
```

