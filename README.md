<h1 align="center">
  Employ_Management
 <h3 align="center"><p>Manage your team with ease</p></h3>
</h1>

### Setup
Make sure you python installed on your system
- Clone the github repo using command
  ``` shell
  git clone https://github.com/AbelLouisFernandez/Employ_Management
  ```
- Create a `.env` file in the root directory of your project.
- Add the following lines to the `.env` file, replace with you teamlead gmail and google passkey :
   ```env
   EMAIL_HOST_USER="Enter your gmail here"
   EMAIL_HOST_PASSWORD="Enter your google passkey here"
   ```
- Create a python environment using command
  ```cmd
   python -m venv yourvirtualenviromentname
   ```
- Activate the virtual enviroment by entering following command on cmd
  ```cmd
   yourvirtualenviromentname\scripts\activate
   ```
- Install dependencies using following command
  ```cmd
   pip install requirements.txt
   ```
- Run the django server
  ```cmd
   python manage.py runserver
   ```
