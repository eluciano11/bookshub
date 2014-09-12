Bookshub
========

Web page to buy and sell books online in Puerto Rico with categories from elementary, high school, university and beyond.

##Installation

**Note: this project is being done on Unix/Linux distributions, if something goes wrong with your
operating system let us know so we can update the docs for that OS.**

###Python

For this project you will need python 2.7.x installed on your computer.
You can download the python installer [here.](https://www.python.org/downloads/)

**Note: Depending on your Operating system, you may have python already installed.**

To check if you have python installed, you can try the following in the command line.

```bash
python
```

This will get you to the python shell and it also provides the python version that's installed.

###Virtual Environment

This is not necessary, but it is highly recommended. A virtual environment is a place where
you can work separately from your global environment and install everything you want and never
affect your global environment.

To do this in python, you can install `virtualenv` with `easy_install` or `pip`. We recommend `pip`.

```bash
sudo pip install virtualenv
```

To create a `virtualenv`, select a folder where you want to work with the project and do the following:
 
```bash
virtualenv venv
```

That will create a virtual environment for python. To activate it do the following:

```bash
source venv/bin/activate
```

###Dependencies

Now that you are in your venv, let's take care of project dependencies.

In the command line, go to the projects root folder and do the following:

```bash
pip install -r requirements.txt
```

That will install all of the dependencies.

###Environment

This project uses environment variables to keep secret settings secret. To get started, you would need to copy the `.env.example` file to a new file called `.env` in the same directory.

That's it!

###Database

For development, we use sqlite since python comes with the driver and it's Django's default database.
To create the database and run the migrations [South](https://godjango.com/3-introduction-to-south-migrations/) do the following:

```bash
python manage.py syncdb
```

Then for migrations

```bash
python manage.py migrate
```

###Running the project

Now, you can run the server by doing this:

```bash
python manage.py runserver
```

Now you can visit `http://localhost:8000` and you are good to go!

###Testing

You can run unit tests using this command
```bash
python manage.py test --configuration=Testing
```

**For any questions and/or recommendations, please contact the team members.**