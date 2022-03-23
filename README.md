# Repairel
An online retail store which enables customers to make well informed decisions on shoe purchases through its transparency as well as ethics and sustainability scoring system, helping to make a positive impact on the environment and people alike.

## Setting up: Initial stage
In making this web application, several packages are required to be installed for it to function correctly. Before beginning, make sure to clone the repository and access the proper directory. Originally, the project was worked on using Gitlab and thus stored in a Gitlab repository

To clone the repository from Gitlab, add the following commands to your terminal:
```
$ git clone https://stgit.dcs.gla.ac.uk/team-project-h/2021/cs23/cs23-main
$ cd cs23-main
```
To clone the repository from Github, add the following commands to your terminal (this will be the normal standard post-handover stage):
```
$ git clone https://github.com/Repairel/repairel-shopify
$ cd repairel-shopify
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
(repairel)$ python manage.py makemigrations
(repairel)$ python manage.py migrate
```

### Connecting to Shopify
In order for Django to connect with Shopify's backend API, a file named keys.py must be placed within the directory named repairelapp. The path to this keys.py file should ultimately look something similar to this once added:

> cs23-main/repairelapp/keys.py

After adding this file to your local directory, a connection with the Shopify API should result and Django will now successfully be connected to Shopify. However, for security reasons, the keys.py file should only be distributed to trusted individuals and never committed to the repository directly. As such, we have included in the Git ignore file to avoid such accidents happening. As such, please only share this this file with trusted developers.

## Running the web application
It's simple. Enter the following line into the command prompt:

```
(repairel)$ python manage.py runserver
```

After that, access the following link to begin browsing the web application: http://127.0.0.1:8000/

### Deployment via Amazon Web Services
Presently, the site is hosten on AWS using Elastic Beanstalk. In order to deploy new updates manually to the website, ensure that you install AWS CLI:
```
(repairel)$ pip3 install awscli --upgrade --user
```

To check if you have installed AWS CLI, you can run the following command which show you the current version installed if you were successful:
```
(repairel)$ aws --version
```

(Optional in case AWS doesn't seem to have installed): Sometimes you need to configure your environmental variables for things to work. AWS provides comprehensive details on how to achieve this in the following [page](https://docs.aws.amazon.com/cli/v1/userguide/install-windows.html)

In order to be able to make manual deployments, you first need to configure the AWS CLI by running:
```
(repairel)$ aws configure
```

The terminal should prompt you asking for information similar to the below:
> AWS Access Key ID [None]:

> AWS Secret Access Key [None]:

> Default region name [None]:

> Default output format [None]:

This information is sensitive and, as such, should only be transferred to trusted inviduals directly and not shared or stored on the repository.

To configure a profile named repairel, enter the following into the terminal:
```
(repairel)$ aws configure --profile repairel
```

Once things are configured, you should now be able to push all the latest changes on the main repository to the live website. To do this, simply run:
```
(repairel)$ eb deploy
```

Give the deployment a few moments to complete. Once it does, the live website should now be updated to reflect the most update version of the code found in the main repository. Congratulations on deploying your changes.

### Additional: Running tests
Tests are provided, and to run them simply enter the following into the terminal:

```
(repairel)$ python manage.py test
```

### Contributors and Team Coach
This project was developed and maintained by a group of level 3 students from the university of Glasgow as part of a two-semester group project. 

* P. Roman (2480607p@student.gla.ac.uk)
* E. Morad (2465064e@student.gla.ac.uk)
* H. Lewis (2472305h@student.gla.ac.uk)
* A. Nadim (2508859a@student.gla.ac.uk)

The project was supervised under the care of a level 4 student.

* C. Calum (2393272c@student.gla.ac.uk)

### Software Specification for Future developers
A core part of professional professional software development is a convenient software specification to support future developers to build on this project to improve and refine upon the work already done. Consequently, a software specification document shall be passed on, explaining the current code base's key structure and architecture, as well as it's principle functionality.

