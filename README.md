
# 📁Fleeting Files (WIP)

Fleeting Files is a file sharing platform that allows users to create or join existing rooms and share files with each other. The aim of this project is to provide a fast and easy way to share files among multiple users.

## Features

- **File Sharing🚀**: Users can upload any type of file to a room. Once a file is uploaded, all other users in the room can download that file.
- **Multi-User Rooms👥**: Users can create their own rooms or join existing ones. All users in a room can share and download files.
- **File Expiration⏳**: Uploaded files are automatically deleted from the server after a certain amount of time, making them no longer available for download.


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

