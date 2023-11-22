# Social Network Friendship & Authentication Demonstration

<div align="center"><p>
    <a href="https://github.com/CodeHeister/project/pulse">
      <img alt="Last commit" src="https://img.shields.io/github/last-commit/CodeHeister/project?style=for-the-badge&logo=starship&color=8bd5ca&logoColor=D9E0EE&labelColor=302D41"/>
    </a>
    <a href="https://github.com/CodeHeister/project/blob/main/LICENSE">
      <img alt="License" src="https://img.shields.io/github/license/CodeHeister/project?style=for-the-badge&logo=starship&color=ee999f&logoColor=D9E0EE&labelColor=302D41" />
    </a>
    <a href="https://github.com/CodeHeister/project">
      <img alt="Repo Size" src="https://img.shields.io/github/repo-size/CodeHeister/project?color=%23DDB6F2&label=SIZE&logo=codesandbox&style=for-the-badge&logoColor=D9E0EE&labelColor=302D41" />
    </a>
</p></div>

### Table of contents
- [Preview](#preview)
- [Steps for installation](#steps-for-installation)

## Preview

Demo sandbox is available [here](https://project-2gfutgeb.b4a.run) _(__don't use personal passwords__)_

## Steps for installation

1. __Docker__
    - `git clone https://github.com/Avdan-OS/Demo.git`
    - `docker build -t project project`
    - `docker run -d --name=project -p 8000:8000 project`
2. __Shell__
    - `git clone https://github.com/Avdan-OS/Demo.git && cd project`
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install --no-cache-dir -r requirements.txt`
    - `python3 manage.py makemigrations && python3 manage.py migrate`
    - `python3 manage.py runserver 127.0.0.1:8000`

To see result go to [localhost page](127.0.0.1:8000)
