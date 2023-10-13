"""pycfdns models."""
from typing import Generic, TypedDict, TypeVar

T = TypeVar("T")


class _IdName(TypedDict):
    id: str
    name: str


class _CodeMessage(TypedDict):
    code: int
    message: str


class _ResultInfo(TypedDict):
    count: int
    page: int
    per_page: int
    total_count: int
    total_pages: int


class _Owner(_IdName):
    type: str


class ResponseModel(TypedDict, Generic[T]):
    errors: list[_CodeMessage]
    messages: list[_CodeMessage]
    success: bool
    result_info: _ResultInfo
    result: T


class _ZoneMeta(TypedDict):
    cdn_only: bool
    custom_certificate_quota: int
    dns_only: bool
    foundation_dns: bool
    page_rule_quota: int
    phishing_detected: bool
    step: int


class _RecordMeta(TypedDict):
    auto_added: bool
    managed_by_apps: bool
    managed_by_argo_tunnel: bool
    source: str


class ZoneModel(TypedDict):
    account: _IdName
    activated_on: str
    created_on: str
    development_mode: int
    id: str
    meta: _ZoneMeta
    modified_on: str
    name: str
    original_dnshost: str
    original_name_servers: list[str]
    original_registrar: str
    owner: _Owner
    vanity_name_servers: list[str]


class RecordModel(TypedDict):
    content: str
    name: str
    proxied: bool
    type: str
    comment: str
    created_on: str
    id: str
    locked: bool
    meta: _RecordMeta
    modified_on: str
    proxiable: bool
    tags: list[str]
    ttl: int
    zone_id: str
    zone_name: str
