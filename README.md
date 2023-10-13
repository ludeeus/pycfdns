# Manage DNS Records hosted by Cloudflare

_[Cloudflare] DNS API Python Wrapper._

## Quick start

### Installation

```bash
python3 -m pip install pycfdns
```

### Example usage

```python
...
import aiohttp
from pycfdns import Client
...
    async with aiohttp.ClientSession() as client_session:
        client = Client(api_token="abc123", client_session=client_session)
        zones = await client.list_zones()
        print(zones)
...
```

## API

Below is a quick overview of the classes and methods that are available in this package.

This package uses [`mypy`] to ensure it is strictly typed, and all API modesl are created as [`TypedDict`] objects.

Anything that is not exported in the base of the module (in the [`__init__.py`](pycfdns/__init__.py) file) are considered internal to this package and will change wihtout any notice, yoo should consider not using anything not found there.

### Client

The [`Client` class][Client] is your entrypoint to this package, this is what's providing the methods described below.

This method accepts the folowing arguments:

Argument | Type | Description
--|--|--
`api_token` | `str` | This is your personal API token to interface with the [Cloudflare API], you can generate this token here: <https://developers.cloudflare.com/api/tokens/create>
`client_session` | `ClientSession` | This neesd to be an instance of `ClientSession` from the [`aiohttp`] pacakge.
`timeout` | `int \| None` | This determines how long an API call can use (in seconds) before it times out, the default is `10` seconds.

#### List Zones

The [`Client.list_zones` method][list_zones_method] can be used to list all zones available with the `api_token` passed to the [`Client` object][Client].

This method takes no arguments.

```python
...
client = Client(session=session, api_token="abc123")
zones = await client.list_zones()
...
```

The `zones` variable in this example will be a list of [`ZoneModel` objects][ZoneModel].

#### List Records

The [`Client.list_dns_records` method][list_dns_records_method] can be used to list all records within a zone.

This method accepts the folowing arguments:

Argument | Type | Description
--|--|--
`zone_id` | `str` | The ID of the zone to list records for.
`name` | `str \| None` | If this is passed in it will only match record matching the name.
`type` | `str \| None` | If this is passed in it will only match record matching the type.


```python
...
client = Client(api_token="abc123", client_session=client_session)
records = await client.list_dns_records()
...
```

The `records` variable in this example will be a list of [`RecordModel` objects][RecordModel].

#### Update Record

The [`Client.update_dns_record` method][update_dns_record_method] can be used to update a record in a zone.

This method accepts the folowing arguments:

Argument | Type| Description
--|--|--
`zone_id` | `str` | The ID of the zone the record exist in.
`record_id` | `str` | The ID of the record to list records for.
`record_name` | `str` | The name of the record.
`record_type` | `str` | The type of the record.
`record_content` | `str` | The content of the record.
`record_comment` | `str \| None` | The comment of the record.
`record_proxied` | `bool \| None` | The proxied state of the record.
`record_tags` | `list[str] \| None` | The tags of the record.
`record_ttl` | `int \| None` | The TTL value of the record.

```python
...
client = Client(api_token="abc123", client_session=client_session)
record = await client.update_dns_record(zone_id="abc123", record_id="abc123", record_name="abc", record_content="1.1.1.1", record_type="A")
...
```

The `record` variable in this example will be a [`RecordModel` object][RecordModel] representing the updated record.


### Exceptions

This package have 2 defined exceptions:

- [`AuthenticationException`], this will be raised when the Cloudflare API returns a status code assosiated with authentication issues.
- [`ComunicationException`], this will be raised when there are issues communicating with the [Cloudflare API].


## Versioning

This package follows the [SemVer] framework to determine how to set the version.

## Publishing

This package is published to [PyPI] when a new [GitHub] release is made.

The publishing itself is handled in [GitHub actions] with [this workflow][release_workflow].

[A history of release actions can be found here][release_history].

There is no fixed schedule for when a new version is published.


## Disclaimer

_This Python wrapper for the Cloudflare API is an independent project and is not endorsed, sponsored, or affiliated with Cloudflare, Inc. The use of Cloudflare's name, trademarks, and other intellectual property is for descriptive purposes only. All rights to Cloudflare's name, trademarks, and other intellectual property belong to Cloudflare, Inc. Use this wrapper at your own risk and ensure that you abide by Cloudflare's terms of service and API usage guidelines._

<!-- Links -->
[Cloudflare]: https://www.cloudflare.com/
[Cloudflare API]: https://developers.cloudflare.com/api/
[`mypy`]: https://www.mypy-lang.org/
[`aiohttp`]: https://docs.aiohttp.org/en/stable/
[`TypedDict`]: https://peps.python.org/pep-0589/
[SemVer]: https://semver.org/
[PyPi]: https://pypi.org/project/pycfdns/
[GitHub]: https://github.com/
[GitHub actions]: https://github.com/features/actions

[release_workflow]: https://github.com/ludeeus/pycfdns/blob/main/.github/workflows/publish.yml
[release_history]: https://github.com/ludeeus/pycfdns/actions/workflows/publish.yml

[Client]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3AClient+path%3Apycfdns%2Fclient.py&type=code
[list_zones_method]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3Alist_zones+path%3Apycfdns%2Fclient.py&type=code
[list_dns_records_method]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3Alist_dns_records+path%3Apycfdns%2Fclient.py&type=code
[update_dns_record_method]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3Aupdate_dns_record+path%3Apycfdns%2Fclient.py&type=code

[`AuthenticationException`]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3AAuthenticationException+path%3Apycfdns%2Fexceptions.py&type=code
[`ComunicationException`]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3AComunicationException+path%3Apycfdns%2Fexceptions.py&type=code

[ZoneModel]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3AZoneModel+path%3Apycfdns%2Fmodels.py&type=code
[RecordModel]: https://github.com/search?q=repo%3Aludeeus%2Fpycfdns+symbol%3ARecordModel+path%3Apycfdns%2Fmodels.py&type=code