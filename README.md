# cz3003-eduventure
Lab Project for NTU CZ3003 - Software Systems Analysis and Design

## Setting up local environment (Windows)

This is a very simplified guide on setting up local environment for Windows

Pre-requisite:

1. Installed `python3`
2. Installed `pip`

### Setting up repository

1. Go to a folder where you want the repository to be in
2. Clone the repository
`git clone https://github.com/adriangohjw/cz3003-eduventure.git`

### Setting up PostgreSQL

PostgreSQL is the relational DBMS of choice in this project
 
1. Download and install PostgreSQL from [Windows installers](https://www.postgresql.org/download/windows/)
 2. Use the following credentials during the installation (otherwise you can update the Config file):
	 1. Username = `postgres` and password = `localhostdbpassword`
 3. Open the psql command-line tool by 
	 1. In the Windows CMD, run the command: `psql -U postgres`  
	 2. Enter password when prompted
	 3. Run the command: `create database "cz3003"`
    
Reference: [Set Up a PostgreSQL Database on Windows](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm)

### Setup virtual environment in project

In Windows CMD, ensure you are in the folder of your repository

1. Run `python –m venv venv`
2. Run `venv\Scripts\activate` 
3. Run `pip install -r requirements.txt`

All required packages should have been installed!
`venv\Scripts\activate` is also the command to enter your

### Setup local database
In Windows CMD, ensure you are in the folder of your repository

1. Run `python models.py db init` 
2. Run `python models.py db migrate`
3. Run `python models.py db upgrade`

## To run the application
`python run.py`
