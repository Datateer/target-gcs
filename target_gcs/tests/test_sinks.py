import re
from datetime import datetime

from target_gcs.sinks import GCSSink
from target_gcs.target import TargetGCS


def build_sink(config={}):
    default_config = {"bucket_name": "test-bucket", "credentials_file": "./creds.json"}
    config.update(default_config)
    print(232222, config)
    return GCSSink(
        TargetGCS(config=config), "my_stream", {"properties": {}}, key_properties=config
    )


def test_extraction_timestamp_is_unix_time():
    subject = build_sink()
    assert re.match(r"my_stream_\d+.jsonl", subject.key_name)


def test_key_name_includes_prefix_when_provided():
    subject = build_sink({"key_prefix": "asdf"})
    assert re.match(r"asdf/my_stream", subject.key_name)


def test_key_name_does_not_start_with_slash():
    subject = build_sink({"key_prefix": "/asdf"})
    assert not subject.key_name.startswith("/")


def test_key_name_includes_stream_name_when_naming_convention_not_provided():
    subject = build_sink({"key_naming_convention": "asdf.txt"})
    assert "asdf.txt" == subject.key_name


def test_key_name_includes_stream_name_if_stream_token_used():
    subject = build_sink({"key_naming_convention": "___{stream}___.txt"})
    assert "___my_stream___.txt" == subject.key_name


def test_key_name_includes_default_date_format_if_date_token_used():
    date_format = "%Y-%m-%d"
    subject = build_sink({"key_naming_convention": "file/{date}.txt"})
    assert f"file/{datetime.today().strftime(date_format)}.txt" == subject.key_name


def test_key_name_includes_date_format_if_date_token_used_and_date_format_provided():
    date_format = "%m %d, %Y"
    subject = build_sink(
        {"key_naming_convention": "file/{date}.txt", "date_format": date_format}
    )
    assert f"file/{datetime.today().strftime(date_format)}.txt" == subject.key_name


def test_key_name_includes_timestamp_if_timestamp_token_used():
    subject = build_sink({"key_naming_convention": "file/{timestamp}.txt"})
    print(subject.key_name)
    assert re.match(r"file/\d+.txt", subject.key_name)
