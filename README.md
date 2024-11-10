# Steps to setup
1. Clone the repo.
2. Install python and pip
3. Create a python virtual environment using the command
```python -m venv venv```
```source venv/bin/activate  # On Windows use `venv\Scripts\activate` ```
4. Run the below command in the campuscrew-be folder to install required dependencies
```pip install -r requirements.txt```

# Configuring Supabase
1. Get access to the CampusCrew Supabase project.
2. In config.py, update the SUPABASE_URL, SUPABASE_KEY and SECRET_KEY from the values in the portal.
3. The SUPABASE_URL is present in `Project Settings -> API -> Project URL`
4. The SUPABASE_KEY is present in `Project Settings -> API -> Project API Keys -> Public`
5. The SECRET_KEY is present in `Project Settings -> API -> Project API Keys -> Secret`
