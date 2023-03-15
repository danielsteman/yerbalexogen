# Yerbal Exogen
This ridiculous name was generated by [Nameflix](https://namelix.com/). I started this project because I want to do my own analysis on Fitbit data. And also because I wanted to build something with `vue` and `visx`. `FastAPI` is familiar and I chose it for development speed.

## Register
Register your app [here](https://dev.fitbit.com/apps) and get a client ID and secret.

## Environment variables
```
CLIENT_ID
CLIENT_SECRET
```

## Install backend dependencies
Make sure you have installed `virtualenv` and Python 3.10.
```
cd backend
virtualenv venv
. venv/bin/activate
pip install -r requirements-dev.txt
```

## Install frontend dependencies
Make sure you have installed a Javascript package manager, I'm using `yarn`.
```
cd frontend
yarn install
```

## Start local backend server
`uvicorn backend.main:app --reload`

## Start local frontend server
`yarn --cwd frontend/ dev`