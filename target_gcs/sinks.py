"""GCS target sink class, which handles writing streams.
Opens an I/O stream pointed to a blob in the GCS bucket
As messages are received from the source, they are streamed to the bucket. As the max batch size is reached, the queue is emptied and written to the I/O streams

"""
from collections import defaultdict
from datetime import datetime
import json
import time

from google.cloud.storage import Client
from singer_sdk.sinks import RecordSink
from smart_open import open


class GCSSink(RecordSink):
    """GCS target sink class."""

    max_size = 1000  # Max records to write in one batch

    def __init__(self, target, stream_name, schema, key_properties):
        super().__init__(
            target=target,
            stream_name=stream_name,
            schema=schema,
            key_properties=key_properties,
        )
        self._gcs_write_handle = None
        self.key_name = self.build_key_name(self.config)

    def build_key_name(self, config):
        extraction_timestamp = round(time.time())
        key_name = self.config.get(
            "key_naming_convention",
            f"{self.stream_name}_{extraction_timestamp}.{self.output_format}",
        )
        key_name = f'{self.config.get("key_prefix", "")}/{key_name}'.replace("//", "/")
        if key_name.startswith("/"):
            key_name = key_name[1:]
        date = datetime.today().strftime(self.config.get("date_format", "%Y-%m-%d"))
        key_name = key_name.format_map(
            defaultdict(
                str, stream=self.stream_name, date=date, timestamp=extraction_timestamp
            )
        )
        return key_name

    @property
    def gcs_write_handle(self):
        """opens a stream for writing to the target cloud object"""
        if not self._gcs_write_handle:
            credentials_path = self.config.get("credentials_file")
            self._gcs_write_handle = open(
                f'gs://{self.config.get("bucket_name")}/{self.key_name}',
                "wb",
                transport_params=dict(
                    client=Client.from_service_account_json(credentials_path)
                ),
            )
        return self._gcs_write_handle

    @property
    def output_format(self):
        """In the future maybe we will support more formats"""
        return "jsonl"

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record.

        Developers may optionally read or write additional markers within the
        passed `context` dict from the current batch.
        """
        self.gcs_write_handle.write(
            f"{json.dumps(record, default=str)}\n".encode("utf-8")
        )
