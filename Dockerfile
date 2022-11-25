FROM python:3.8-slim
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends build-essential gcc wget

# Make sure we use the virtualenv:
RUN python -m venv /opt/venv
RUN /opt/venv/bin/python -m pip install --upgrade pip
ENV PATH="/opt/venv/bin:$PATH"

#hdf5
RUN cd ; wget https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-1.13/hdf5-1.13.3/src/hdf5-1.13.3.tar.gz
RUN cd ; tar zxf hdf5-1.13.3.tar.gz
RUN cd ; mv hdf5-1.13.3 hdf5-setup
RUN cd ; cd hdf5-setup ;  ./configure --prefix=/usr/local/
RUN cd ; cd hdf5-setup ;  make &&  make install

# cleanup
RUN cd ; rm -rf hdf5-setup
RUN apt-get -yq autoremove
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install numpy
WORKDIR /opt
# TA-Lib
COPY . /opt

RUN cd ta-lib/ && \
  ./configure --prefix=/usr --build=aarch64-unknown-linux-gnu && \
  make && \
  make install

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN ls
#RUN pip install -r requirements.txt

CMD ["python","/opt/main.py"]