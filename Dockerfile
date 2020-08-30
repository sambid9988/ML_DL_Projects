FROM continuumio/anaconda3:4.4.0
COPY . /c/Users/John/Documents/churn_doc
EXPOSE 5000
WORKDIR /c/Users/John/Documents/churn_doc
RUN pip install -r requirements.txt
CMD python flask_app.py