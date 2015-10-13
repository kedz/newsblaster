NB_HOME=""
if [ -z "$NB_HOME" ]; then
    NB_HOME="$HOME/newsblaster_home"
    mkdir -p "$NB_HOME"
    set NB_HOME
    echo "Setting NB_HOME to $NB_HOME."
else
    echo "Override default NB_HOME with user variable $NB_HOME"
    #Set to users 
    NB_HOME=$NB_HOME
fi 


BIN_DIR="$NB_HOME/bin"
SRC_DIR="$NB_HOME/src"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Create bin directory to be used by NewsBlaster
if [ ! -d $BIN_DIR ]; then
    echo "Creating bin directory"
    mkdir -p "$BIN_DIR"
fi


export PATH=$BIN_DIR:$PATH

# Creates install  dependencies directory
if [ ! -d $SRC_DIR ]; then
    echo "Creating source directory"
    mkdir -p "$SRC_DIR"
fi

#-------------------------------------------------------#
# Start installing and compiling required sources here.  #
#-------------------------------------------------------#
# This was done because of installation on Columbia servers

if [ ! -f $NB_HOME/lib/libxml2.a ]; then
        cd "$SRC_DIR"
    curl -O http://xmlsoft.org/sources/libxml2-2.9.1.tar.gz
    tar zxvf libxml2-2.9.1.tar.gz
    cd libxml2-2.9.1
    ./configure --prefix=$NB_HOME
    make
    make install
fi

if [ ! -f $NB_HOME/lib/libxslt.a ]; then
        cd "$SRC_DIR"
    curl -O http://xmlsoft.org/sources/libxslt-1.1.28.tar.gz
    tar zxvf libxslt-1.1.28.tar.gz
    cd libxslt-1.1.28
    ./configure --prefix=$NB_HOME
    make
    make install
fi


#-------------------------------------------------------#
# Install MongoDB  #
#-------------------------------------------------------#

if [ ! -f "$BIN_DIR/mongo" ]; then
    cd "$SRC_DIR"
    rmq_temp=""

    if [ "$(uname)" == "Darwin" ]
    then
        echo "Downloading MongoDB For OSX"
        curl -O https://fastdl.mongodb.org/osx/mongodb-osx-x86_64-3.0.6.tgz
        tar zxvf mongodb-osx-x86_64-3.0.6.tgz 
        cd mongodb-osx-x86_64-3.0.6
        rmq_temp=`pwd`

    elif [ "$(expr substr $(uname -s ) 1 5 )" == "Linux" ]
    then
        # Linux
        echo "Downloading MongoDB For Linux"
        curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz
        tar zxvf mongodb-linux-x86_64-3.0.6.tgz
    
        cd mongodb-linux-x86_64-3.0.6
        rmq_temp=`pwd`
    fi

    # OSX


    DATA_DIR="$NB_HOME/data/db"
    mkdir -p "$DATA_DIR"
    
    ln -s "$rmq_temp/bin/mongo" "$BIN_DIR/mongo"
    ln -s "$rmq_temp/bin/mongod" "$BIN_DIR/mongod"
    
    #Start mongodb
    $BIN_DIR/mongod --dbpath $DATA_DIR --fork --logpath "$DATA_DIR/mongodb.log"
    # Wait on start
    $BIN_DIR/mongo --nodb $DIR/setup/mongo_wait.js
    #Setup Indices
    $BIN_DIR/mongo newsblaster --eval "db.articles.ensureIndex({'title':1})"
    
    #Stop mongodb
    $BIN_DIR/mongod --dbpath $DATA_DIR --shutdown

fi


#Exports
export LD_LIBRARY_PATH=$NB_HOME/lib
set LD_LIBRARY_PATH
export LIBRARY_PATH=$NB_HOME/lib
export C_INCLUDE_PATH=$NB_HOME/include:$NB_HOME/include/libxml2
export CPLUS_INCLUDE_PATH=$NB_HOME/include/libxslt/:$NB_HOME/include/libexslt

cd $NB_HOME
if [ ! -d $NB_HOME/venv ]; then
        pip install virtualenv
        virtualenv venv
fi

source venv/bin/activate
pip install lxml
pip install -U setuptools
pip install -U cython
pip install service_identity
pip install scrapy
pip install pyyaml
pip install scrapyd
#pip install Celery
pip install requests
pip install -U numpy scipy scikit-learn
pip install BeautifulSoup
pip install pymongo
pip install goose-extractor
pip install beautifulsoup4

# Fix required for Celery. Remove after package created from master
git clone https://github.com/celery/celery.git
cd celery
pip install -r requirements/dev.txt
python setup.py install

# Install sumpy
https://github.com/kedz/sumpy.git
cd sumpy 
python setup.py install
