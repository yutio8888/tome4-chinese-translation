"""Version manifest loading and validation."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import ConfigurationError


DEFAULT_VERSION = "tome-1.7.6"
SUPPORTED_SCHEMA_VERSION = 1


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"{label} must be a non-empty relative path")
    if "\\" in value or "\x00" in value:
        raise ConfigurationError(
            f"{label} must be a normalized relative path: {value!r}"
        )
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ConfigurationError(f"{label} must be a normalized relative path: {value!r}")
    if len(value) >= 2 and value[0].isalpha() and value[1] == ":":
        raise ConfigurationError(
            f"{label} must be a normalized relative path: {value!r}"
        )
    return value


@dataclass(frozen=True)
class RepositorySpec:
    name: str
    env: str
    default: str
    commit: str
    required: bool

    def resolve(self, root: Path) -> Path:
        configured = os.environ.get(self.env)
        if configured:
            candidate = Path(configured).expanduser()
            if not candidate.is_absolute():
                raise ConfigurationError(f"{self.env} must be an absolute path")
        else:
            candidate = root / self.default
        return candidate.resolve()


@dataclass(frozen=True)
class SourceMount:
    git_path: str
    mount: str


@dataclass(frozen=True)
class ProtectedSourceRoot:
    name: str
    env: str
    repository: str
    relative_path: str
    access: str

    def path(self, manifest: "Manifest") -> Path:
        configured = os.environ.get(self.env)
        if configured:
            candidate = Path(configured).expanduser()
            if not candidate.is_absolute():
                raise ConfigurationError(f"{self.env} must be an absolute path")
            return candidate
        return manifest.repository_path(self.repository) / self.relative_path


@dataclass(frozen=True)
class ProtectedSource:
    root: str
    path_env: str
    directory_candidates: tuple[str, ...]
    mount: str


@dataclass(frozen=True)
class ComponentSpec:
    id: str
    translation: str
    copy_fragment: str | None
    source_repository: str | None
    sources: tuple[SourceMount, ...]
    protected_source: ProtectedSource | None
    source_baseline: SourceBaseline | None
    extract_by_default: bool
    official_locale: str | None
    full_output: str | None
    addon_eligible: bool


@dataclass(frozen=True)
class RuntimeSpec:
    luajit_env: str
    luarocks_root_env: str
    luarocks_root_default: str
    lua_version: str
    lpeg_runtime_version: str
    lpeg_rock_version: str
    required_modules: tuple[str, ...]


@dataclass(frozen=True)
class ExtractorSpec:
    repository: str
    commit: str
    git_path: str
    max_stack: int
    preserve_duplicate_occurrences: bool


@dataclass(frozen=True)
class ExternalRequirement:
    id: str
    reason: str


@dataclass(frozen=True)
class SourceBaseline:
    kind: str
    extractor_commit: str
    snapshot_sha256: str
    tdef_count: int


@dataclass(frozen=True)
class ReleaseLayer:
    id: str
    artifact_profile: str
    components: tuple[str, ...]
    external_requirements: tuple[str, ...]
    status: str
    notes: str


@dataclass(frozen=True)
class Manifest:
    path: Path
    raw_bytes: bytes
    root: Path
    schema_version: int
    version: str
    locale: str
    repositories: dict[str, RepositorySpec]
    protected_source_roots: dict[str, ProtectedSourceRoot]
    runtime: RuntimeSpec
    extractor: ExtractorSpec
    components: tuple[ComponentSpec, ...]
    manual_definitions: tuple[str, ...]
    addon_external_requirements: tuple[ExternalRequirement, ...]
    release_layers: tuple[ReleaseLayer, ...]
    terminology: str
    policy: str

    def component(self, component_id: str) -> ComponentSpec:
        for component in self.components:
            if component.id == component_id:
                return component
        valid = ", ".join(component.id for component in self.components)
        raise ConfigurationError(
            f"unknown component {component_id!r}; expected one of: {valid}"
        )

    def repository_path(self, name: str) -> Path:
        try:
            spec = self.repositories[name]
        except KeyError as error:
            raise ConfigurationError(f"unknown repository {name!r}") from error
        return spec.resolve(self.root)

    def protected_root_path(self, name: str) -> Path:
        try:
            spec = self.protected_source_roots[name]
        except KeyError as error:
            raise ConfigurationError(f"unknown protected source root {name!r}") from error
        return spec.path(self)

    @property
    def protected_repositories(self) -> frozenset[str]:
        return frozenset(
            root.repository for root in self.protected_source_roots.values()
        )


def _required_mapping(data: dict[str, Any], key: str, label: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"{label}.{key} must be an object")
    return value


def _required_string(data: dict[str, Any], key: str, label: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"{label}.{key} must be a non-empty string")
    return value


def _boolean(
    data: dict[str, Any], key: str, label: str, *, default: bool = False
) -> bool:
    value = data.get(key, default)
    if type(value) is not bool:
        raise ConfigurationError(f"{label}.{key} must be a boolean")
    return value


def _integer(value: Any, label: str, *, minimum: int | None = None) -> int:
    if minimum is None:
        requirement = "an integer"
    elif minimum == 1:
        requirement = "a positive integer"
    elif minimum == 0:
        requirement = "a non-negative integer"
    else:
        requirement = f"an integer >= {minimum}"
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ConfigurationError(f"{label} must be {requirement}")
    return value


def _full_oid(value: str, label: str) -> str:
    if len(value) not in (40, 64) or any(char not in "0123456789abcdef" for char in value):
        raise ConfigurationError(f"{label} must be a full lowercase Git object ID")
    return value


def _sha256(value: str, label: str) -> str:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ConfigurationError(f"{label} must be a lowercase SHA-256 digest")
    return value


def load_manifest(
    *, version: str = DEFAULT_VERSION, manifest_path: str | Path | None = None
) -> Manifest:
    root = repository_root()
    path = (
        Path(manifest_path).expanduser().resolve()
        if manifest_path is not None
        else root / "i18n" / "versions" / f"{version}.json"
    )
    try:
        raw_bytes = path.read_bytes()
    except OSError as error:
        raise ConfigurationError(f"cannot read version manifest: {path}") from error
    try:
        data = json.loads(raw_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(f"invalid JSON version manifest: {path}: {error}") from error
    if not isinstance(data, dict):
        raise ConfigurationError("version manifest root must be an object")
    schema_version = _integer(data.get("schema_version"), "manifest.schema_version")
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        raise ConfigurationError(
            "manifest.schema_version is unsupported: "
            f"expected {SUPPORTED_SCHEMA_VERSION}, found {schema_version}"
        )

    repositories_data = _required_mapping(data, "repositories", "manifest")
    repositories: dict[str, RepositorySpec] = {}
    for name, value in repositories_data.items():
        if not isinstance(value, dict):
            raise ConfigurationError(f"repositories.{name} must be an object")
        repositories[name] = RepositorySpec(
            name=name,
            env=_required_string(value, "env", f"repositories.{name}"),
            default=_required_string(value, "default", f"repositories.{name}"),
            commit=_full_oid(
                _required_string(value, "commit", f"repositories.{name}"),
                f"repositories.{name}.commit",
            ),
            required=_boolean(value, "required", f"repositories.{name}"),
        )

    runtime_data = _required_mapping(data, "runtime", "manifest")
    modules = runtime_data.get("required_modules")
    if not isinstance(modules, list) or not all(
        isinstance(module, str) and module for module in modules
    ):
        raise ConfigurationError("runtime.required_modules must be a string array")
    runtime = RuntimeSpec(
        luajit_env=_required_string(runtime_data, "luajit_env", "runtime"),
        luarocks_root_env=_required_string(
            runtime_data, "luarocks_root_env", "runtime"
        ),
        luarocks_root_default=_required_string(
            runtime_data, "luarocks_root_default", "runtime"
        ),
        lua_version=_required_string(runtime_data, "lua_version", "runtime"),
        lpeg_runtime_version=_required_string(
            runtime_data, "lpeg_runtime_version", "runtime"
        ),
        lpeg_rock_version=_required_string(
            runtime_data, "lpeg_rock_version", "runtime"
        ),
        required_modules=tuple(modules),
    )

    extractor_data = _required_mapping(data, "extractor", "manifest")
    max_stack = _integer(
        extractor_data.get("max_stack"), "extractor.max_stack", minimum=1000
    )
    extractor = ExtractorSpec(
        repository=_required_string(extractor_data, "repository", "extractor"),
        commit=_full_oid(
            _required_string(extractor_data, "commit", "extractor"),
            "extractor.commit",
        ),
        git_path=_relative_path(extractor_data.get("git_path"), "extractor.git_path"),
        max_stack=max_stack,
        preserve_duplicate_occurrences=_boolean(
            extractor_data, "preserve_duplicate_occurrences", "extractor"
        ),
    )
    if extractor.repository not in repositories:
        raise ConfigurationError("extractor.repository is not declared")

    protected_roots_data = data.get("protected_source_roots", {})
    if not isinstance(protected_roots_data, dict):
        raise ConfigurationError("manifest.protected_source_roots must be an object")
    protected_source_roots: dict[str, ProtectedSourceRoot] = {}
    for name, value in protected_roots_data.items():
        label = f"protected_source_roots.{name}"
        if not isinstance(value, dict):
            raise ConfigurationError(f"{label} must be an object")
        repository = _required_string(value, "repository", label)
        if repository not in repositories:
            raise ConfigurationError(f"{label}.repository is not declared")
        access = _required_string(value, "access", label)
        if access != "lua-extractor-only":
            raise ConfigurationError(
                f"{label}.access must be 'lua-extractor-only'"
            )
        protected_source_roots[name] = ProtectedSourceRoot(
            name=name,
            env=_required_string(value, "env", label),
            repository=repository,
            relative_path=_relative_path(
                value.get("relative_path"), f"{label}.relative_path"
            ),
            access=access,
        )

    components_data = data.get("components")
    if not isinstance(components_data, list) or not components_data:
        raise ConfigurationError("manifest.components must be a non-empty array")
    components: list[ComponentSpec] = []
    seen_components: set[str] = set()
    for index, value in enumerate(components_data):
        label = f"components[{index}]"
        if not isinstance(value, dict):
            raise ConfigurationError(f"{label} must be an object")
        component_id = _required_string(value, "id", label)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", component_id):
            raise ConfigurationError(
                f"{label}.id must be a safe token matching [A-Za-z0-9_-]+"
            )
        if component_id in seen_components:
            raise ConfigurationError(f"duplicate component id: {component_id}")
        seen_components.add(component_id)
        source_repository = value.get("source_repository")
        if source_repository is not None and source_repository not in repositories:
            raise ConfigurationError(
                f"{label}.source_repository is not declared: {source_repository!r}"
            )
        sources_data = value.get("sources")
        if not isinstance(sources_data, list):
            raise ConfigurationError(f"{label}.sources must be an array")
        sources: list[SourceMount] = []
        for source_index, source in enumerate(sources_data):
            source_label = f"{label}.sources[{source_index}]"
            if not isinstance(source, dict):
                raise ConfigurationError(f"{source_label} must be an object")
            sources.append(
                SourceMount(
                    git_path=_relative_path(
                        source.get("git_path"), f"{source_label}.git_path"
                    ),
                    mount=_relative_path(source.get("mount"), f"{source_label}.mount"),
                )
            )
        if sources and source_repository is None:
            raise ConfigurationError(f"{label} has sources but no source_repository")
        protected_source_data = value.get("protected_source")
        protected_source: ProtectedSource | None = None
        if protected_source_data is not None:
            if not isinstance(protected_source_data, dict):
                raise ConfigurationError(f"{label}.protected_source must be an object")
            if sources or source_repository is not None:
                raise ConfigurationError(
                    f"{label} cannot combine public and protected source mappings"
                )
            protected_root = _required_string(
                protected_source_data, "root", f"{label}.protected_source"
            )
            if protected_root not in protected_source_roots:
                raise ConfigurationError(
                    f"{label}.protected_source.root is not declared"
                )
            candidates = protected_source_data.get("directory_candidates")
            if not isinstance(candidates, list) or not candidates or not all(
                isinstance(candidate, str) and candidate for candidate in candidates
            ):
                raise ConfigurationError(
                    f"{label}.protected_source.directory_candidates must be a string array"
                )
            normalized_candidates: list[str] = []
            for candidate in candidates:
                candidate_path = PurePosixPath(candidate)
                if (
                    candidate_path.is_absolute()
                    or len(candidate_path.parts) != 1
                    or candidate in (".", "..")
                    or "\\" in candidate
                    or "\x00" in candidate
                ):
                    raise ConfigurationError(
                        f"{label}.protected_source has an unsafe directory candidate"
                    )
                normalized_candidates.append(candidate)
            if len(normalized_candidates) != len(set(normalized_candidates)):
                raise ConfigurationError(
                    f"{label}.protected_source.directory_candidates contains duplicates"
                )
            protected_source = ProtectedSource(
                root=protected_root,
                path_env=_required_string(
                    protected_source_data, "path_env", f"{label}.protected_source"
                ),
                directory_candidates=tuple(normalized_candidates),
                mount=_relative_path(
                    protected_source_data.get("mount"),
                    f"{label}.protected_source.mount",
                ),
            )
        source_baseline_data = value.get("source_baseline")
        source_baseline: SourceBaseline | None = None
        if source_baseline_data is not None:
            if not isinstance(source_baseline_data, dict):
                raise ConfigurationError(f"{label}.source_baseline must be an object")
            if protected_source is None:
                raise ConfigurationError(
                    f"{label}.source_baseline requires a protected_source mapping"
                )
            tdef_count = _integer(
                source_baseline_data.get("tdef_count"),
                f"{label}.source_baseline.tdef_count",
                minimum=1,
            )
            source_baseline = SourceBaseline(
                kind=_required_string(
                    source_baseline_data, "kind", f"{label}.source_baseline"
                ),
                extractor_commit=_full_oid(
                    _required_string(
                        source_baseline_data,
                        "extractor_commit",
                        f"{label}.source_baseline",
                    ),
                    f"{label}.source_baseline.extractor_commit",
                ),
                snapshot_sha256=_sha256(
                    _required_string(
                        source_baseline_data,
                        "snapshot_sha256",
                        f"{label}.source_baseline",
                    ),
                    f"{label}.source_baseline.snapshot_sha256",
                ),
                tdef_count=tdef_count,
            )
            if source_baseline.extractor_commit != extractor.commit:
                raise ConfigurationError(
                    f"{label}.source_baseline.extractor_commit must match extractor.commit"
                )
        copy_fragment = value.get("copy_fragment")
        official_locale = value.get("official_locale")
        full_output = value.get("full_output")
        components.append(
            ComponentSpec(
                id=component_id,
                translation=_relative_path(value.get("translation"), f"{label}.translation"),
                copy_fragment=(
                    _relative_path(copy_fragment, f"{label}.copy_fragment")
                    if copy_fragment is not None
                    else None
                ),
                source_repository=source_repository,
                sources=tuple(sources),
                protected_source=protected_source,
                source_baseline=source_baseline,
                extract_by_default=_boolean(value, "extract_by_default", label),
                official_locale=(
                    _relative_path(official_locale, f"{label}.official_locale")
                    if official_locale is not None
                    else None
                ),
                full_output=(
                    _relative_path(full_output, f"{label}.full_output")
                    if full_output is not None
                    else None
                ),
                addon_eligible=_boolean(value, "addon_eligible", label),
            )
        )

    manual = data.get("manual_definitions", [])
    if not isinstance(manual, list):
        raise ConfigurationError("manual_definitions must be an array")
    manual_definitions = tuple(
        _relative_path(value, "manual_definitions entry") for value in manual
    )

    requirements_data = data.get("addon_external_requirements", [])
    if not isinstance(requirements_data, list):
        raise ConfigurationError("addon_external_requirements must be an array")
    addon_external_requirements: list[ExternalRequirement] = []
    requirement_ids: set[str] = set()
    for index, value in enumerate(requirements_data):
        label = f"addon_external_requirements[{index}]"
        if not isinstance(value, dict):
            raise ConfigurationError(f"{label} must be an object")
        requirement_id = _required_string(value, "id", label)
        if requirement_id in requirement_ids:
            raise ConfigurationError(
                f"duplicate addon external requirement: {requirement_id}"
            )
        requirement_ids.add(requirement_id)
        addon_external_requirements.append(
            ExternalRequirement(
                id=requirement_id,
                reason=_required_string(value, "reason", label),
            )
        )

    component_ids = {component.id for component in components}
    requirement_id_set = {requirement.id for requirement in addon_external_requirements}
    release_layers_data = data.get("release_layers", [])
    if not isinstance(release_layers_data, list):
        raise ConfigurationError("release_layers must be an array")
    release_layers: list[ReleaseLayer] = []
    release_layer_ids: set[str] = set()
    for index, value in enumerate(release_layers_data):
        label = f"release_layers[{index}]"
        if not isinstance(value, dict):
            raise ConfigurationError(f"{label} must be an object")
        layer_id = _required_string(value, "id", label)
        if layer_id in release_layer_ids:
            raise ConfigurationError(f"duplicate release layer: {layer_id}")
        release_layer_ids.add(layer_id)
        artifact_profile = _required_string(value, "artifact_profile", label)
        if artifact_profile not in {"full", "addon"}:
            raise ConfigurationError(
                f"{label}.artifact_profile must be 'full' or 'addon'"
            )
        layer_components = value.get("components", [])
        if not isinstance(layer_components, list) or not all(
            isinstance(component, str) and component for component in layer_components
        ):
            raise ConfigurationError(f"{label}.components must be a string array")
        if len(set(layer_components)) != len(layer_components):
            raise ConfigurationError(f"{label}.components contains duplicates")
        unknown_components = set(layer_components) - component_ids
        if unknown_components:
            raise ConfigurationError(
                f"{label}.components are undeclared: {sorted(unknown_components)}"
            )
        if artifact_profile == "addon":
            non_addon = [
                component
                for component in components
                if component.id in layer_components and not component.addon_eligible
            ]
            if non_addon:
                raise ConfigurationError(
                    f"{label}.components are not addon eligible: "
                    + ", ".join(component.id for component in non_addon)
                )
        layer_requirements = value.get("external_requirements", [])
        if not isinstance(layer_requirements, list) or not all(
            isinstance(requirement, str) and requirement
            for requirement in layer_requirements
        ):
            raise ConfigurationError(
                f"{label}.external_requirements must be a string array"
            )
        if len(set(layer_requirements)) != len(layer_requirements):
            raise ConfigurationError(
                f"{label}.external_requirements contains duplicates"
            )
        unknown_requirements = set(layer_requirements) - requirement_id_set
        if unknown_requirements:
            raise ConfigurationError(
                f"{label}.external_requirements are undeclared: "
                + ", ".join(sorted(unknown_requirements))
            )
        status = _required_string(value, "status", label)
        if status not in {"releaseable", "optional", "baseline-pending"}:
            raise ConfigurationError(
                f"{label}.status must be releaseable, optional, or baseline-pending"
            )
        release_layers.append(
            ReleaseLayer(
                id=layer_id,
                artifact_profile=artifact_profile,
                components=tuple(layer_components),
                external_requirements=tuple(layer_requirements),
                status=status,
                notes=_required_string(value, "notes", label),
            )
        )

    manifest = Manifest(
        path=path,
        raw_bytes=raw_bytes,
        root=root,
        schema_version=schema_version,
        version=_required_string(data, "version", "manifest"),
        locale=_required_string(data, "locale", "manifest"),
        repositories=repositories,
        protected_source_roots=protected_source_roots,
        runtime=runtime,
        extractor=extractor,
        components=tuple(components),
        manual_definitions=manual_definitions,
        addon_external_requirements=tuple(addon_external_requirements),
        release_layers=tuple(release_layers),
        terminology=_relative_path(data.get("terminology"), "terminology"),
        policy=_relative_path(data.get("policy"), "policy"),
    )
    if manifest.version != version:
        raise ConfigurationError(
            f"manifest version mismatch: requested {version}, found {manifest.version}"
        )
    return manifest
