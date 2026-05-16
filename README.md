# Mediafire-DL

Mediafire-DL is a small command-line downloader for MediaFire links.

It handles single files and folders, keeps nested folder structure intact, and shows a clean progress display while it downloads. Public links work without any login details. Links that require an account can be tried with an optional local cookies file.

## What It Does

- Downloads public MediaFire file links
- Downloads public MediaFire folder links
- Walks nested folders automatically
- Saves folders using the same folder layout MediaFire reports
- Shows a file preview before downloading
- Supports a dry-run mode so you can check what would be saved first
- Defaults to your system `Downloads` folder
- Can read a local `cookies.txt` file for links your own browser account can access

## Install

You need Python 3.9 or newer.

Install:

```bash
pip install mfget
```

Run:

```bash
mediafire-dl
```

### macOS

If Python is not installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

Then install and run:

```bash
pip install mfget
mediafire-dl
```

If `pip` is not found:

```bash
python3 -m pip install mfget
```

If `mediafire-dl` is not found:

```bash
python3 -m mediafire_dl
```

### Windows

If Python is not installed:

```powershell
winget install Python.Python.3.12
```

Then install and run:

```powershell
pip install mfget
mediafire-dl
```

If `pip` is not found:

```powershell
py -m pip install mfget
```

If `mediafire-dl` is not found:

```powershell
py -m mediafire_dl
```

### Linux

If Python or pip is not installed:

```bash
sudo apt install python3 python3-pip
```

On Fedora:

```bash
sudo dnf install python3 python3-pip
```

On Arch:

```bash
sudo pacman -S python python-pip
```

Then install and run:

```bash
pip install mfget
mediafire-dl
```

If `pip` is not found:

```bash
python3 -m pip install mfget
```

If `mediafire-dl` is not found:

```bash
python3 -m mediafire_dl
```

### From GitHub

Install the latest code from GitHub:

```bash
pip install git+https://github.com/worstgirlinamerica/mediafire-dl.git
```

On Windows:

```powershell
pip install git+https://github.com/worstgirlinamerica/mediafire-dl.git
```

### Local Project

Install from a cloned project folder:

```bash
pip install .
```

## Usage

Run the command and paste a MediaFire link when it asks:

```bash
mediafire-dl
```

Or pass the link directly:

```bash
mediafire-dl "https://www.mediafire.com/file/example/file.zip/file"
```

Choose a save folder:

```bash
mediafire-dl "https://www.mediafire.com/folder/example/My+Folder" --output ~/Downloads/MediaFire
```

Preview a folder without downloading anything:

```bash
mediafire-dl --dry-run "https://www.mediafire.com/folder/example/My+Folder"
```

Show more technical error details:

```bash
mediafire-dl --verbose "https://www.mediafire.com/file/example/file.zip/file"
```

Use a local cookies file for a link that your browser account can already access:

```bash
mediafire-dl --cookies ~/Downloads/cookies.txt "https://www.mediafire.com/file/example/file.zip/file"
```

The cookies file must be in Netscape/Mozilla `cookies.txt` format. Mediafire-DL only reads the file from your computer for that run.

## Supported Links

Supported:

- Public MediaFire file links
- Public MediaFire folder links
- Public folders with nested subfolders
- MediaFire file or folder links that work with a user-provided `cookies.txt` file

Not supported:

- Asking for or storing MediaFire usernames and passwords
- Automatically reading cookies from your browser
- Password-protected downloads that require an extra password prompt
- Captcha-gated or blocked downloads

## Privacy And Safety

Mediafire-DL does not ask for MediaFire login details and does not read browser cookies automatically. If you use `--cookies`, the cookie file stays on your machine and is only read by the current command.

## License

MIT License. See [LICENSE](LICENSE).
