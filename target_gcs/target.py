"""GCS target class."""

from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_gcs.sinks import GCSSink


class TargetGCS(Target):
    """Sample target for GCS."""

    name = "target-gcs"
    config_jsonschema = th.PropertiesList(
        th.Property("credentials_file", th.StringType, required=True),
        th.Property("bucket_name", th.StringType, required=True),
        th.Property("key_prefix", th.StringType, required=False),
        th.Property("key_naming_convention", th.StringType, required=False),
    ).to_dict()
    default_sink_class = GCSSink
