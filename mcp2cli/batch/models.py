"""Data models for batch operations."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from mcp2cli.config.models import ServerConfig


@dataclass
class BatchEntry:
    """A single MCP server entry for batch conversion."""

    name: str
    package: str
    type: str  # "npm" or "pip"
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> BatchEntry:
        """Create a BatchEntry from a dict (as read from servers.json)."""
        return cls(
            name=d["name"],
            package=d.get("package", ""),
            type=d.get("type", "npm"),
            command=d.get("command", "npx"),
            args=d.get("args", []),
            env=d.get("env", {}),
        )

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dict."""
        d: dict = {
            "name": self.name,
            "package": self.package,
            "type": self.type,
            "command": self.command,
            "args": self.args,
        }
        if self.env:
            d["env"] = self.env
        return d

    def to_server_config(self) -> ServerConfig:
        """Convert to a ServerConfig for scanning."""
        return ServerConfig(
            name=self.name,
            command=self.command,
            args=self.args,
            env=self.env,
        )


@dataclass
class BatchResult:
    """Result of a single server's batch conversion."""

    name: str
    status: str  # "success" | "failed" | "skipped"
    error: str | None = None
    tool_count: int = 0
    version: str | None = None


def load_batch_input(path: Path) -> list[BatchEntry]:
    """Load batch entries from a JSON file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")
    return [BatchEntry.from_dict(d) for d in data]


def save_batch_input(entries: list[dict], path: Path) -> None:
    """Save batch entries to a JSON file."""
    path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
