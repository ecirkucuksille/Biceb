# BİÇEB distribution guide / Dağıtım kılavuzu

## Package outputs

| Platform | Output | Tool |
| --- | --- | --- |
| Windows x64 | `BICEB-<version>-windows-x64-setup.exe` | PyInstaller + Inno Setup |
| macOS Intel | `BICEB-<version>-macos-x86_64.dmg` | PyInstaller + `hdiutil` |
| macOS Apple Silicon | `BICEB-<version>-macos-arm64.dmg` | PyInstaller + `hdiutil` |
| Debian/Ubuntu x64 | `biceb_<version>_amd64.deb` | PyInstaller + `dpkg-deb` |
| Other Linux x64 | `BICEB-<version>-linux-x86_64.AppImage` | PyInstaller + `appimagetool` |

The outputs include Python and application dependencies. End users do not need a terminal, Python or pip for Windows, macOS or DEB installation. AppImage users must grant executable permission once. The Windows installer runs per user without an administrator password, creates a Start Menu entry and supports English and Turkish wizard text. The DEB registers a desktop launcher and icon.

## Automated builds

Put this project in a GitHub repository and run **Actions → Build BİÇEB installers → Run workflow**. Each job runs the tests, builds on its target operating system and uploads its installer as an artifact. Artifacts are kept for 30 days.

For a downloadable release, update `pyproject.toml`, `biceb/__init__.py` and the fallback version in `packaging/windows/BICEB.iss` to the same version, then push a tag such as `v0.2.0`. The workflow checks that the tag matches the DEB version and prepares a draft release containing all five installers and their SHA-256 checksums. Review signing and platform installation before publishing the draft. A GitHub repository with Actions enabled is required.

## Local build commands

Install Python 3.12 and `python -m pip install -e ".[dev]"` on the target operating system. PyInstaller does not make cross-platform executables from one host.

**Windows** (PowerShell, with Inno Setup 6 installed):

```powershell
python -m PyInstaller --noconfirm --clean --onedir --windowed --name BICEB --icon biceb/resources/biodiversity.ico --collect-data biceb main.pyw
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" packaging\windows\BICEB.iss
```

**macOS**:

```bash
python -m PyInstaller --noconfirm --clean --onedir --windowed --name BICEB --icon biceb/resources/images.png --osx-bundle-identifier org.biceb.desktop --collect-data biceb main.py
bash packaging/macos/build_dmg.sh
```

**Ubuntu/Debian**:

```bash
python -m PyInstaller --noconfirm --clean --onefile --windowed --name BICEB --collect-data biceb main.py
python packaging/linux/build.py deb
```

To build the AppImage, pass the pinned official `appimagetool` binary and runtime to `packaging/linux/build.py appimage` via `--appimagetool` and `--runtime-file`. The workflow downloads them and checks their SHA-256 hashes automatically. Linux packages should be built on the oldest supported distribution: the DEB records the build host's glibc version and the AppImage also uses its system libraries. The workflow uses Ubuntu 22.04 for this reason.

## Public distribution requirements

The macOS DMGs are currently unsigned. An Apple Developer ID Application certificate, hardened runtime signing and Apple notarization are required before an ordinary macOS user can open a downloaded app without Gatekeeper blocking it. The DMG builder preserves the `.app` bundle and adds an Applications shortcut, but it does not sign or notarize. See [Apple's distribution guide](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution).

An unsigned Windows installer may show a SmartScreen warning. A trusted code signing certificate is needed to identify the publisher to Windows. Add signing to the build before public release; never commit certificates or passwords to the repository.

Run a final manual install and uninstall on actual Windows, macOS Intel, macOS Apple Silicon, and Ubuntu computers before sending packages to nontechnical users. The automated tests verify calculations, but cannot confirm each desktop environment's interactive installation experience.
