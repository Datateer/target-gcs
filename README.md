# target-gcs

`target-gcs` is a Singer target for GCS.

Build with the [Meltano Target SDK](https://sdk.meltano.com).

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install target-gcs
```

## Supported formats

JSONL is the only supported output format

## Configuration

### Accepted Config Options

| Property              | Env variable                     | Type   | Required | Default       | Description                                                                                                                                                                                                                                                                                      |
| --------------------- | -------------------------------- | ------ | -------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| credentials_file      | TARGET_GCS_CREDENTIALS_FILE      | string | yes      | None          | Path to the google cloud credentials file                                                                                                                                                                                                                                                        |
| bucket_name           | TARGET_GCS_BUCKET_NAME           | string | yes      | n/a           | The name of the GCS bucket                                                                                                                                                                                                                                                                       |
| date_format           | TARGET_GCS_DATE_FORMAT           | string | no       | %Y-%m-%d      | If `{date}` token is used in key_naming_convention, the date will be formatted with this format string                                                                                                                                                                                           |
| key_prefix            | TARGET_GCS_KEY_PREFIX            | string | no       | None          | A static prefix before the generated key names. If this and `key_naming_convention` are both provided, they will be combined.                                                                                                                                                                    |
| key_naming_convention | TARGET_GCS_KEY_NAMING_CONVENTION | string | no       | `{timestamp}` | A prefix to add to the beginning of uploaded files. The following tokens are supported: `date`, `stream`, and `timestamp`. The date format in `date_format` will be used based on [python date format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) |

Property Type Required? Description
aws_access_key_id String No S3 Access Key Id. If not provided, AWS_ACCESS_KEY_ID environment variable will be used.
aws_secret_access_key String No S3 Secret Access Key. If not provided, AWS_SECRET_ACCESS_KEY environment variable will be used.

A full list of supported settings and capabilities for this
target is available by running:

```bash
target-gcs --about
```

### Configure using environment variables

This Singer target will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your target requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `target-gcs` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-gcs --version
target-gcs --help
# Test using the "Carbon Intensity" sample:
tap-carbon-intensity | target-gcs --config /path/to/target-gcs-config.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_gcs/tests` subfolder and
then run:

```bash
poetry run pytest
```

You can also test the `target-gcs` CLI interface directly using `poetry run`:

```bash
poetry run target-gcs --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-gcs
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-gcs --version
# OR run a test `elt` pipeline with the Carbon Intensity sample tap:
meltano elt tap-carbon-intensity target-gcs
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano SDK to
develop your own Singer taps and targets.
