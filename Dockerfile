FROM python:3.8.10
RUN mkdir /app
copy ./ /app

WORKDIR /app
RUN ls
RUN cd ta-lib
   && ./configure --prefix=/usr
   && make
  sudo make install
RUN pip install -r requirements.txt  
RUN cd ~
CMD ["python","monitoring.py"]