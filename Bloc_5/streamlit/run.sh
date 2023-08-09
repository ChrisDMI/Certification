docker run -it \
-v "$(pwd):/home/app" \
-p 80:4000 \
-e PORT=4000 \
getaround-streamlit