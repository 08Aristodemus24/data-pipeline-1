FROM apache/airflow:2.10.4

# 1st step is to install the needed libraries we need in our container
# which will be pandas, apache-airflow amazon, pyspark, etc.  
# copy <path from local system> <directory in docker container you want the file or files to be copied in>
COPY ./requirements.txt ./

# once the requirements path is copied to the docker container
# run a pip install
RUN pip install --no-cache-dir -r ./requirements.txt


# 2nd step is to install java development kit
USER root

# Install OpenJDK-17
RUN apt update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-arm64'
RUN export JAVA_HOME