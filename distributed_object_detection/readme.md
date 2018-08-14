## distributed yolo

```
docker pull little170/yolo:pc-master
docker pull little170/yolo:pc-worker
```
Run Following Struction

```
docker run --expose=8887 little170/yolo:pc-master python worker.py --ps_hosts=127.0.0.1:8887 --worker_hosts=127.0.0.1:8888,127.0.0.1:8889 --job_name=ps --task_index=0 
docker run --expose=8888 little170/yolo:pc-worker python worker.py --ps_hosts=127.0.0.1:8887 --worker_hosts=127.0.0.1:8888,127.0.0.1:8889 --job_name=worker --task_index=0
docker run --expose=8889 little170/yolo:pc-worker python worker.py --ps_hosts=127.0.0.1:8887 --worker_hosts=127.0.0.1:8888,127.0.0.1:8889 --job_name=worker --task_index=0 
docker run -e MASTER_IP='127.0.0.1' -e MASTER_PORT='8887' little170/yolo:pc-master python yolo.py
```
