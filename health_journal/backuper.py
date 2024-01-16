from datetime import datetime

import boto3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from health_journal import logger
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

    def save_to_s3(self, file, folder="health_backups", timestamp=None):
        """Save a local file to AWS S3 with versioning based on timestamp.

        Args:
            file (Path): Path to the local file.
            s3_file_path (Path): Desired file path on S3 without versioning.
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d")

        versioned_s3_file_path = f"{folder}/{timestamp}/{file.name}"

        try:
            self.s3_client.upload_file(file, self.bucket_name, versioned_s3_file_path)
            logger.info(f"File {file} uploaded to {versioned_s3_file_path} on S3.")
        except Exception as e:
            logger.critical(f"Error uploading {file} to S3: {str(e)}")


class BackUper:
    """
    Class for backuping databases to AWS S3.

    This class uses apscheduler for scheduling backups.
    """

    def __init__(self):
        self.saver = AWSSaver(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            bucket_name=BUCKET_NAME,
        )

        self.scheduler = AsyncIOScheduler()

    def backup(self, databases, hour=24):
        """
        Backup databases to AWS S3 every {hour} hours.

        Args:
            databases (List[DataBase]): list of processors
        """
        self.databases = databases

        self.scheduler.add_job(self._backup, CronTrigger(hour=hour, minute=0))
        self.scheduler.start()

    def _backup(self):
        timestamp = datetime.now().strftime("%Y%m%d")

        for database in self.databases:
            path = database.create_backup()
            self.saver.save_to_s3(path, timestamp=timestamp)
