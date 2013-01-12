#!/bin/bash 

TARGET_ENV=py-local
VIRTUALENV_URL="https://raw.github.com/pypa/virtualenv/master/virtualenv.py"

echo -e "Creating virtualenv in $TARGET_ENV."
curl -O $VIRTUALENV_URL
python virtualenv.py --no-site-packages $TARGET_ENV
rm -f virtualenv.py*

echo -e "Successfully created virtual env in $TARGET_ENV\n\n"

if [ -f "requirements.txt" ] 
    then 
       echo -e "Installing dependencies:"
       source $TARGET_ENV/bin/activate
       pip install --upgrade -r requirements.txt 
       echo -e "Done installing dependencies\n\n\n"
fi

echo -e "To activate the virtualenv run:\n\n"
echo -e "     source $TARGET_ENV/bin/activate\n\n"

echo -e "To verify the client works and your app is configured correctly"
echo -e "run the 'get_token.py' script to retrieve an oauth session token.\n\n"
