# Data Collection Service for the Microbiome Analysis Platform
Data Collection service fetches DNA sequencing data (fastq) from the Sequence Read Archive database and saves them in an S3 bucket.

## Installation

Create an EC2 instance on AWS using the Qiime2 image. Please refer to https://docs.qiime2.org/ for details.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Install the SRA Toolkit: https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit

Install Redis 
```sudo apt-get install redis-server```

Install Supervisor 
```sudo apt-get install supervisor```

Install nginx 
```sudo apt install nginx```

Create directories for gunicorn
```sudo mkdir -pv /var/{log,run}/gunicorn/```

Change ownership of the folders
```sudo chown -cR qiime2:qiime2 /var/{log,run}/gunicorn/```

Copy the celery.conf file to /etc/supervisor/celery.conf

Create a log folder for celery
```sudo mkdir /var/log/celery```



## Usage
1. Mount your S3 bucket to the EC2 instance.
2. Provide file paths for FASTERQ_DUMP_PATH, S3_STUDIES_PATH, and S3_SCRATCH_DIR in config/settings.py
3. Start the redis server using ```sudo systemctl start redis```
4. Start supervisor ```sudo supervisord -c /etc/supervisor/celery.conf```
5. Navigate to the project folder ```cd DataCollectionService/```  
6. Run the following commands.

```python
source venv/bin/activate  
sudo service nginx start
gunicorn -c config/dev.py
```

4. To fetch DNA sequencing data from SRA send a post request to port 8000. The body of the post request must include json data with the following format:
{
  "run_id": "SRR18828316"
}
