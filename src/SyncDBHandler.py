from abc import ABC, abstractmethod
import os
from utils import Logger
logger = Logger.setup_logger(__name__)

class SyncError(Exception):
    """Custom exception for synchronization errors."""
    pass

class SyncDB(ABC):

    @abstractmethod
    def sync_from_cloud(self, **kwargs) -> None:
        """Abstract method to sync data from the cloud storage."""
        pass

class SyncS3DBHandler(SyncDB):

    def __init__(self, aws_s3_bucket) -> None:
        self.aws_s3_bucket = aws_s3_bucket

    def sync_from_cloud(
        self,
        s3_prefix: str,
        local_folder: str
    ) -> None:
        # List objects in the bucket with the specified prefix
        objects = self.aws_s3_bucket.objects.filter(Prefix=s3_prefix)
        
        for obj in objects:
            # Check if the object is in the root directory (no '/' at the end of the key) and has only one level depth
            if obj.key.count('/') == 1:
                local_file_path = os.path.join(local_folder, os.path.basename(obj.key))
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                try:
                    self.aws_s3_bucket.download_file(obj.key, local_file_path)
                    logger.info(f"Downloaded {obj.key} to {local_file_path}")
                except Exception as e:
                    logger.error(f"Error downloading {obj.key}: {e}", exc_info=True)
                    raise SyncError(f"Error downloading {obj.key}: {e}")

        logger.info(f"Sync from S3: {s3_prefix} to Local: {local_folder} .............Done")