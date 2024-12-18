import os
import sys
from dotenv import load_dotenv

load_dotenv()

LOCAL_DIR = os.getenv("LOCAL_DIR")
sys.path.append(f"{LOCAL_DIR}/high-entropy-oxide/share")
import share

REMOTE_DIR = os.getenv("REMOTE_DIR")
WORK_DIR = os.getenv("WORK_DIR")
JOB_USER = os.getenv("JOB_USER")
INIT_NUM = os.getenv("INIT_NUM")
BO_NUM = os.getenv("BO_NUM")

share.make_instance(LOCAL_DIR, REMOTE_DIR, WORK_DIR, JOB_USER, INIT_NUM, BO_NUM)
