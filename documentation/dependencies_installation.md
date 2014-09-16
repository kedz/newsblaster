Installation steps required for non-privileged/non-root users


Installing RabbitMQ Locally 

Since we do not have root or access to a privileged account we have to do the following steps

1)First download and install Erlang (http://www.erlang.org/download.html)

wget http://www.erlang.org/download/otp_src_17.1.tar.gz

2) Untar & Compile (Provided all system dependencies are meet)

3)Add Erlang to your System Path

/proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/otp_src_17.1/bin

export PATH=$PATH:/proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/otp_src_17.1/bin

4) Download the binary for RabbitMQ (http://www.rabbitmq.com/)

wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.3.5/rabbitmq-server-generic-unix-3.3.5.tar.gz

5)Untar and Add RabbitMQ to Path



Dependencies for Scrappy 


  Running setup.py install for lxml
    /usr/lib/python2.7/distutils/dist.py:267: UserWarning: Unknown distribution option: 'bugtrack_url'
      warnings.warn(msg)
    Building lxml version 3.4.0.
    Building without Cython.
    ERROR: /bin/sh: 1: xslt-config: not found

    ** make sure the development packages of libxml2 and libxslt are installed **

    Using build configuration of libxslt
    building 'lxml.etree' extension




1. Download and Compile libxml2-2.9.1 & libxslt-1.1.28

2. Add to LD_LIBRARY_PATH. Make and install into specific local paths


./configure --prefix=/proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/libxslt_path

Libraries have been installed in:
   /proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/libxslt_path/lib/python2.7/site-packages

./configure --prefix=/proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/libxml_path


Libraries have been installed in:
   /proj/nlpdisk3/nlpusers/newsblaster_project/python_env/lib/python2.7/site-packages

3. Download and compile lxml from source(http://lxml.de/build.html)

python_env)dvc2106@island2:/proj/fluke/nemo/nlpdisk1/nlp/users/newsblaster_project/dependencies/lxml$ python setup.py build --with-cython --with-xslt-config=../libxslt_path/bin/xslt-config

python setup.py install

