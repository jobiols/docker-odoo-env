#Generating distribution archives

verificar que tengamos las ultimas versiones

    python3 -m pip install --user --upgrade setuptools wheel
    python3 -m pip install --user --upgrade twine
 
ejecutar en el directorio donde esta setup.py
    
    python3 setup.py sdist bdist_wheel
    
# Uploading the distribution archives
    
    twine upload dist/*
    
luego el proyecto se puede ver en

    https://pypi.org/project/docker-odoo-env/

#Installing your newly uploaded package

    pip install docker-odoo-env
    

    