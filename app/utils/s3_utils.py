import boto3
import base64
import uuid
import logging

from botocore.config import Config
from botocore.exceptions import ClientError, ConnectTimeoutError

from app.services.utils.collection import settings
from app.utils import context_vars
from app.utils.config import get_settings
from app.utils.errors import ServerError

settings = get_settings()
settings.configure_logging()
logger = logging.getLogger(__name__)
request_id_context = context_vars.request_id_context


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
        endpoint_url=settings.s3_endpoint_url,
        config=Config(
            connect_timeout=settings.connect_timeout,
            read_timeout=settings.read_timeout,
            retries=settings.retry_config,
        ),
    )


async def upload_to_s3(
    image_data: str, filename: str, content_type: str = "image/png"
) -> str:
    s3_client = get_s3_client()

    try:
        try:
            s3_client.head_bucket(Bucket=settings.s3_bucket_name)
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                logger.info(
                    f"Bucket {settings.s3_bucket_name} not exist. Creating..."
                )
                s3_client.create_bucket(Bucket=settings.s3_bucket_name)
            else:
                logger.error(
                    f"Could not connect to S3 endpoint (maybe VPN is disconnected): {str(e)}",
                    extra={"request_id": request_id_context.get()},
                )
                raise ServerError(
                    code=500,
                    usr_msg="there was an error validating the bucket",
                    e=e,
                )

        image_bytes = base64.b64decode(image_data)
        key = f"layers/{uuid.uuid4()}_{filename}"

        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=image_bytes,
            ContentType=content_type,
        )
        url = f"{settings.s3_endpoint_url}/{settings.s3_bucket_name}/{key}"
        return url

    except ConnectTimeoutError as e:
        logger.error(
            f"Could not connect to S3 endpoint (maybe VPN is disconnected): {str(e)}",
            extra={"request_id": request_id_context.get()},
        )
        raise ServerError(
            code=500,
            usr_msg="Connection to S3 failed — check your VPN connection",
            e=e,
        )

    except ClientError as e:
        logger.error(
            f"Failed to upload image to S3: {str(e)}",
            extra={"request_id": request_id_context.get()},
        )
        raise ServerError(
            code=500, usr_msg="Failed to upload image to S3", e=e
        )
