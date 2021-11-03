# CS23 Main

# Repairel
An online retail store which enables customers to make well informed decisions on shoe purchases through its transparency as well as ethics and sustainability scoring system, helping to make a positive impact on the environment and people alike.

## Setting up: Initial stage
In making this web application, several packages are required to be installed for it to function correctly. Before beginning, make sure to clone the repository and access the proper directory.

```
$ git clone https://stgit.dcs.gla.ac.uk/team-project-h/2021/cs23/cs23-main
$ cd cs23-main
```

### Setting up: Creating and activating the virtual environment
Assuming Anaconda is being used, enter the following into the command prompt:
```
$ conda create -n repairel python=3.10.0
$ conda activate repairel
```

### Setting up: Installing the necessary package dependencies
To make sure of using the right packages and versions required to run the web application, install them by entering the following into the command prompt:

```
(repairel)$ pip install -r requirements.txt
```

### Setting up: Making migrations and migrating
Make sure that the current directory is where file manage.py is located and enter the following in the command prompt:

```
(repairel)$ python manage.py makemigrations repairel
(repairel)$ python manage.py migrate
```

## Running the web application
It's simple. Enter the following line into the command prompt:

```
(repairel)$ python manage.py runserver
```

After that, access the following link to begin browsing the web application: http://127.0.0.1:8000/