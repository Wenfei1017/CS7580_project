# CS7580-Happyfive

### Contributing to this Project

1. clone repo to local machine
```
git clone git@github.com:sodapeng/CS7580-Happyfive.git
```
1. create branch for changes on local
```
git checkout -b <branch_name>
```
1. push branch with changes to remote
```
git push -u origin <branch_name>
```

### Running Locally
1. activate virtualenv (make sure pipenv is installed)
```
pipenv shell
```

2. install the packages
```
pipenv install
```

3. start the project
```
python run.py
```
4. exit virtualenv
```
exit
```

### Deploying to Production
1. Install Heroku CLI
- https://devcenter.heroku.com/articles/getting-started-with-python#set-up
1. Test locally (visiting application at http://localhost:5000):
```
heroku local
```
1. Add modified files to the local git repository:
```
git add .
```
1. Commit the changes to the repository:
```
git commit -m "commit message"
```
1. Deploy:
```
git push heroku master
```
1. Final check:
```
heroku open
```

### Swagger
1. Run the app  

2. swagger UI can be opened with URL on Local or Heroku: 
- http://127.0.0.1:5000/apidocs/
- https://eventmanager-happyfive.herokuapp.com/apidocs/

### Run Test/Debugger
1. Pytest:   
* Basic usage: 
```
    - Run all tests in project: python -m pytest   
    - Run all tests in a test file: python -m pytest [test path]
        eg. python -m pytest tests/users/test_users.py
    - Run a single test in a test file: python -m pytest [test path]::[test name]  
        eg. python -m pytest tests/users/test_users.py::test_create_user 
```

* Show test result information: python -m pytest [test path] -s  
```
    eg. python -m pytest tests/users/test_users.py::test_get_create_user -s
```
2. Python Debugger:
* Typical usage： 
``` 
    import pdb; pdb.set_trace() 
```

* Common commands:
```
    h   help    print the list of available commands  
    s   step    execute the current line, stop at the first possible occasion  
    n   next    continue execution until the next line in the current function is reached or it returns  
    r   return  continue execution until the current function returns  
    q   quit    quit from the debugger
```  
[Link for more commands](https://docs.python.org/2/library/pdb.html)  

3. Test Coverage:  
* method-1  
```
coverage run -m pytest  
```  
* method-2  
```
1. coverage run run.py
2. control + c  //stop running
3. coverage report eventmanager/*
```  