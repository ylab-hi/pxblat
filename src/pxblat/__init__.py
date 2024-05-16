from __future__ import annotations

from rich.traceback import install

from .extc import ClientOption, ServerOption, TwoBitToFaOption, UsageStats
from .parser import read
from .server import (
    Client,
    ClientThread,
    Server,
    Status,
    build_index,
    check_port_in_use,
    check_port_open,
    copy_client_option,
    create_client_option,
    create_server_option,
    files,
    find_free_port,
    query_server,
    server_query,
    start_server,
    start_server_mt,
    start_server_mt_nb,
    status_server,
    stop_server,
    wait_server_ready,
)
from .toolkit import fa_to_two_bit, two_bit_to_fa

__version__ = "1.2.1"

install(show_locals=True)


__all__ = [
    "Server",
    "ClientThread",
    "Client",
    "files",
    "server_query",
    "start_server_mt",
    "start_server",
    "status_server",
    "stop_server",
    "create_client_option",
    "query_server",
    "fa_to_two_bit",
    "two_bit_to_fa",
    "create_server_option",
    "check_port_open",
    "start_server_mt_nb",
    "wait_server_ready",
    "find_free_port",
    "check_port_in_use",
    "copy_client_option",
    "Status",
    "read",
    "TwoBitToFaOption",
    "ClientOption",
    "ServerOption",
    "UsageStats",
    "build_index",
]
