# HelloBye
Simple Start and Shutdown Script for Prometheus Targets

Configuration
=============
1. Add these following snippet to `prometheus.yml`:
    
    ```json
    - job_name: 'AUTOSCALING-SERVERS'
      file_sd_configs:
      - files:
        - 'autoscale.json'
    ```
    
2. Add `autoscale.json`:
`vim /etc/prometheus/autoscale.json`
    
    ```json
    []
    ```
    
    `chmod 755 /etc/prometheus/autoscale.json`
    
3. Add `hellobye_listener.py` to Prometheus Server:
    
    ```json
    cd /opt/prometheus
    vim hellobye_listener.py
    ```
    
4. `vim /etc/systemd/system/hellobye.service`
    
    ```python
    systemctl daemon-reload
    systemctl enable hellobye
    systemctl start hellobye
    ```
