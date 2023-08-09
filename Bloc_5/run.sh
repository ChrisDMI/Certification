docker run -it\
 -p 4000:4000\
 -v "$(pwd):/home/app"\
 -e APP_URI="https://chris-mlflow-tracking.herokuapp.com/"\
 -e AWS_ACCESS_KEY_ID=" "\
 -e AWS_SECRET_ACCESS_KEY=" "\
 chrisdmi/mlflowtracker python train.py