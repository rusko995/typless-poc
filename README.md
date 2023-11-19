# Typless PoC

This project is a Flask-based web application that utilizes the Typless API for document processing.

These instructions will help you set up and run the project on your local machine for development and testing purposes.


## Pre-requisites
- **Python3** - https://www.python.org/downloads/
    - **pip** and **make** (should be included inside Python3)
- **Typless** account - register on https://app.typless.com
    - You should train the data inside the Typless portal before using this applicaion
    - Documentation and examples for Typless can be found here: https://docs.typless.com

## Usage and instalation
- Clone repository and enter the newly created folder:
    - `git clone https://github.com/rusko995/typless-poc.git`
    - `cd typless-poc`

- Install necessary packages to the virtual environment: `make install`
- Go to the **app/config.py** and add your Typless token in a format: `TYPLESS_API_KEY = "Token ########################"` (where you replace #characters with your token).
    - To obtain the API key visit the Settings page inside [Typless portal](https://app.typless.com)
- Run application: `make run`
- By defaul the application is accessible at: http://127.0.0.1:5000 (as this is poc the debugging mode is on)
- On the page you can upload the invoice file and then click "PROCESS". Program will return the extracted data which you can save to the local database with clicking the "SAVE" button. As written before - you must train the data fot the same supplier as you uploaded the invoice in the Typless portal first.
- Accepted file formats are: `pdf`, `jpg`, `png`, `tiff`
- Some testing invoices are available inside `tests/files` - you can play around with them. 

## Database
There is a simple SQLite database incuded in the project (some data is already inside). If you want to have a fresh state just delete the `instance/database.db` file and re-run the project.

## Automatic testing
You can run automatic backend tests with: `make test`


Have fun!