FROM python:2

RUN apt-get update
RUN apt-get install -y libfreetype6-dev libxft-dev libblas-dev liblapack-dev liblapacke-dev
RUN pip install paho-mqtt
RUN pip install numpy==1.10.4
RUN pip install matplotlib

WORKDIR heatmap/
ADD heat_map_pub.py /

CMD ["python","./heat_map_pub.py"]
