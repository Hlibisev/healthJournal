import logging
from datetime import datetime

import boto3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from health_journal.processors.base import BackUpable
from health_journal.settings_secret import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME


class AWSSaver:
    """
    Class for saving files to AWS S3.

    Args:

    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, region_name="us-east-1"):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.bucket_name = bucket_name

    def save_to_s3(self, local_file_path, s3_file_path):
        """Save a local file to AWS S3 with versioning based on timestamp.

        Args:
            local_file_path (str): Path to the local file.
            s3_file_path (str): Desired file path on S3 without versioning.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        versioned_s3_file_path = f"{s3_file_path.rstrip('/')}-{timestamp}.csv"

        try:
            self.s3_client.upload_file(local_file_path, self.bucket_name, versioned_s3_file_path)
            logging.info(f"File {local_file_path} uploaded to {versioned_s3_file_path} on S3.")
        except Exception as e:
            logging.critical(f"Error uploading {local_file_path} to S3: {str(e)}")


class BackUper:
    """
    Class for backuping processors to AWS S3.

    This class everyday saves processors in csv format to AWS S3.
    """

    def __init__(self):
        self.saver = AWSSaver(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            bucket_name=BUCKET_NAME,
        )

        self.scheduler = AsyncIOScheduler()

    def backup_everyday(self, processors):
        self.processors = [p for p in processors if isinstance(p, BackUpable)]
        logging.info(f"Found {len(self.processors)} processors to backup. {self.processors}")

        self.scheduler.add_job(self._backup, CronTrigger(hour=10, minute=0))
        self.scheduler.start()

    def _backup(self, processor):
        for processor in self.processors:
            path = processor.create_backup()
            self.saver.save_to_s3(path, path)
