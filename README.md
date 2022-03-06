
  
# ClassDeck

## Introduction 📜

ClassDeck aims to provide a virtual classroom that breaks the synchronous hurdles of location, place, student limits and cater the knowledge to the learning crowd anytime and anywhere. It is an all in one platform which makes the entire cycle of learning seamless for both educators and students. It also has a whole range of useful features that 
help to make the whole learning process remote and through virtual platforms.

### Features

- Generate Virtual Classrooms Anytime
- Educators can create assignments and quizes 
- Students can view and submit Assignments
- Keep Track of Student's progress
- Enable Collaboration among students on specific topics
- Tools and Utilities for ease of learning
- Whiteboard for uploading useful content and materials
- Events Calender to keep track of schedule

### Tech Stack 💻

</br>

<img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/> <img alt="HTML5" src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>



</br>
</br>

## Instructions to setup & Run:arrow_down::computer:

<details>
<summary>
Step 1: Downloading and Installing the Code Editor
</summary>
<br>
You can download and install any one of the following IDE.
<br><br>
<ul>
<li><a href="https://code.visualstudio.com/">Visual Studio Code</a> (Preferred)</li>
<li><a href="https://www.sublimetext.com/3">Sublime Text 3</a></li>
<li><a href="https://atom.io/">Atom</a></li>
</details>

---

<details>
<summary>
Step 2: Installing Python
</summary>
<br>
Download <a href="https://www.python.org/downloads/">Python Latest Version</a>
<br><br>
<ul>
<li>Make sure to check '<b>Add Python to Path</b>' in the setup window of the Installer.</li>
</ul>

Verify the installation from the Terminal using the following command,

```bash
python --version
```

</details>

---

<details>
<summary>
Step 3: Installing Git
</summary>
<br>
Download <a href="https://git-scm.com/downloads">Git</a>
</details>

---

<details>
<summary>
Step 4: Fork the Repository
</summary>
<br>
Click on <a href="#" target="_self"><img src="https://user-images.githubusercontent.com/58631762/120588030-11cee200-c454-11eb-98ad-060ef99428c5.png" width="16"></img></a> to fork <a href="https://github.com/coding-geek21/classDeck">this</a> repsository
</details>

---

<details>
<summary>
Step 5: Cloning Repository using Git
</summary>
<br>

```bash
git clone https://github.com/'<your-github-username>'/classDeck.git
```

</details>

---

<details>
<summary>
Step 6: Change directory to classDeck
</summary>
<br>

```bash
cd classDeck
```

</details>

---

<details>
<summary>
Step 7: Add reference to the original repository
</summary>
<br>

```bash
git remote add upstream https://github.com/coding-geek21/classDeck.git
```

</details>

---

<details>
<summary>
Step 8: Creating Virtual Environment
</summary>
<br>
Install virtualenv
<br><br>

```bash
pip install virtualenv
```

Creating Virtual Environment named `env`

```bash
virtualenv env
```

To Activate `env`

```bash
source env/Scripts/activate
or
./env/Scripts/activate
```

To deactivate `env`

```bash
deactivate
```

</details>

---

<details>
<summary>
Step 9: Installing Requirements
</summary>
<br>

**Note**: Before installing requirements, Make sure the virtual environment is activated.
<br><br>

```bash
cd classDeck
pip install -r requirements.txt
```

</details>

---

<details>
<summary>
Step 10: Making database migrations
</summary>
<br>

**Note**: Before making database migrations, make sure you've successfully created database.

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

</details>

---

<details>
<summary>
Step 11: Creating superuser to access Admin Panel
</summary>
<br>

```bash
python manage.py createsuperuser
```

</details>

---

<details>
<summary>
Step 12: Create env files from env templates
</summary>
<br>


1. Install Django Environ

```
$ pip install django-environ
```
2. Import environ in settings.py
```
import environ
```
3. Initialise environ
Below your import in settings.py:
```
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
```
4. Create your .env file

In the same directory as settings.py, create a file called ‘.env’

5. Declare your environment variables in .env

Make sure you don’t use quotations around strings.

6. IMPORTANT: Add your .env file to .gitignore

7. Replace all references to your environment variables in settings.py
```
DATABASES = {
‘default’: {
‘NAME’: env(‘DATABASE_NAME’),
‘USER’: env(‘DATABASE_USER’),
‘PASSWORD’: env(‘DATABASE_PASS’),
}
}
```
and 
```
SECRET_KEY = env(‘SECRET_KEY’)
```
---

</details>


---
<details>
<summary>
Step 13: Running the Project in local server
</summary>
<br>
<b>Note:</b> Before running the project in local server, Make sure you activate the Virtual Environment.
<br><br>

```bash
python manage.py runserver
```

<p>Server will be up and running in local host on PORT 8000</p>
</details>

---

## Project Admin 🤓

<br>
<table>
<tr>
<td align="center" ><a href="https://github.com/coding-geek21"><img src="https://avatars.githubusercontent.com/u/53329034?s=400&u=bc78468dc0c164cd9605f7ed16709d35bc25205e&v=4" width=150px height=150px /></a></br> <h4 style="color:white;">Jayapritha N</h4>

</tr>
</table>
<br>