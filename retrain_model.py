import os
os.chdir('backend/model')
exec(open('train_model.py').read())