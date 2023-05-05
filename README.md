# Data Collection Service for the Microbiome Analysis Platform
Data Collection service fetches DNA sequencing data (fastq) from the Sequence Read Archive database and saves them in an S3 bucket.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Install SRA Toolkit: https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit
Install Redis using ```sudo apt-get install redis-server```
Install Supervisor using ```sudo apt-get install supervisor```


## Usage
1. Mount your S3 bucket to the EC2 instance.
1. Provide file paths for FASTERQ_DUMP_PATH, S3_STUDIES_PATH, and S3_SCRATCH_DIR in config/settings.py
2. Start the redis server using ```sudo systemctl start redis```
3. Run the following commands.

```python
source venv/bin/activate  
python3 manage.py runserver 0:8000
```

4. To merge Qiime2 results and generate visualizations send a post request to port 8000. The body of the post request must include json data with the following format:
{
  "run_ids": "SRR18828316 SRR18828317 SRR18828318"
}
