"""Build user-installable Linux packages from a PyInstaller executable."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
ICON = ROOT / "biceb" / "resources" / "images.png"
ARCHITECTURES = {"x86_64": ("amd64", "x86_64"), "aarch64": ("arm64", "aarch64")}


def desktop_file(executable: str) -> str:
    return f"""[Desktop Entry]
Type=Application
Name=BİÇEB
GenericName=Biodiversity Analysis
GenericName[tr]=Biyoçeşitlilik Analizi
Comment=Calculate biodiversity indices
Comment[tr]=Biyoçeşitlilik indekslerini hesaplayın
Exec={executable}
Icon=biceb
Terminal=false
Categories=Science;
StartupNotify=true
"""


def prepare_deb(binary: Path, output: Path, architecture: str) -> Path:
    deb_arch, _ = ARCHITECTURES[architecture]
    libc_name, libc_version = platform.libc_ver()
    if libc_name != "glibc" or not libc_version:
        raise RuntimeError("DEB builds require a glibc-based Linux build host")
    package = output / f"biceb_{VERSION}_{deb_arch}.deb"
    with tempfile.TemporaryDirectory(prefix="biceb-deb-") as temporary:
        root = Path(temporary) / "package"
        application = root / "opt" / "biceb"
        application.mkdir(parents=True)
        shutil.copy2(binary, application / "BICEB")
        launcher = root / "usr" / "bin" / "biceb"
        launcher.parent.mkdir(parents=True)
        launcher.symlink_to("/opt/biceb/BICEB")
        desktop = root / "usr" / "share" / "applications" / "biceb.desktop"
        desktop.parent.mkdir(parents=True)
        desktop.write_text(desktop_file("biceb"), encoding="utf-8")
        icon = root / "usr" / "share" / "pixmaps" / "biceb.png"
        icon.parent.mkdir(parents=True)
        shutil.copy2(ICON, icon)
        control = root / "DEBIAN" / "control"
        control.parent.mkdir(parents=True)
        control.write_text(
            f"""Package: biceb
Version: {VERSION}
Section: science
Priority: optional
Architecture: {deb_arch}
Maintainer: BİÇEB Project
Depends: libc6 (>= {libc_version}), libx11-6, libxcb1, libxcb-cursor0, libxkbcommon-x11-0, libgl1
Description: BİÇEB biodiversity analysis desktop application
 Calculates alpha and beta diversity indices from CSV and Excel data.
 Supports Turkish and English interfaces and exports XLSX results.
""",
            encoding="utf-8",
        )
        for directory in root.rglob("*"):
            if directory.is_dir():
                directory.chmod(0o755)
        subprocess.run(["dpkg-deb", "--build", "--root-owner-group", str(root), str(package)], check=True)
    return package


def prepare_appimage(binary: Path, output: Path, architecture: str, appimagetool: Path, runtime_file: Path | None) -> Path:
    _, appimage_arch = ARCHITECTURES[architecture]
    package = output / f"BICEB-{VERSION}-linux-{appimage_arch}.AppImage"
    with tempfile.TemporaryDirectory(prefix="biceb-appdir-") as temporary:
        appdir = Path(temporary) / "BICEB.AppDir"
        executable = appdir / "usr" / "bin" / "BICEB"
        executable.parent.mkdir(parents=True)
        shutil.copy2(binary, executable)
        (appdir / "AppRun").write_text(
            '#!/bin/sh\nHERE="$(dirname "$0")"\nexec "$HERE/usr/bin/BICEB" "$@"\n',
            encoding="utf-8",
        )
        (appdir / "AppRun").chmod(0o755)
        (appdir / "biceb.desktop").write_text(desktop_file("BICEB"), encoding="utf-8")
        shutil.copy2(ICON, appdir / "biceb.png")
        (appdir / ".DirIcon").symlink_to("biceb.png")
        command = [str(appimagetool)]
        if runtime_file is not None:
            command.extend(["--runtime-file", str(runtime_file)])
        command.extend([str(appdir), str(package)])
        package.unlink(missing_ok=True)
        subprocess.run(
            command,
            check=True,
            env={**os.environ, "ARCH": appimage_arch},
        )
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("format", choices=("deb", "appimage"))
    parser.add_argument("--binary", type=Path, default=ROOT / "dist" / "BICEB")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "installers")
    parser.add_argument("--appimagetool", type=Path, help="Path to the official appimagetool binary")
    parser.add_argument("--runtime-file", type=Path, help="Pinned official AppImage runtime")
    args = parser.parse_args()
    binary = args.binary.resolve()
    if not binary.is_file():
        parser.error(f"PyInstaller executable is missing: {binary}")
    architecture = platform.machine().lower()
    if architecture not in ARCHITECTURES:
        parser.error(f"Unsupported architecture: {architecture}")
    args.output.mkdir(parents=True, exist_ok=True)
    if args.format == "deb":
        package = prepare_deb(binary, args.output, architecture)
    else:
        if args.appimagetool is None or not args.appimagetool.is_file():
            parser.error("--appimagetool must point to an executable file")
        if args.runtime_file is not None and not args.runtime_file.is_file():
            parser.error(f"AppImage runtime is missing: {args.runtime_file}")
        package = prepare_appimage(
            binary,
            args.output,
            architecture,
            args.appimagetool.resolve(),
            args.runtime_file.resolve() if args.runtime_file else None,
        )
    print(package)


if __name__ == "__main__":
    main()
