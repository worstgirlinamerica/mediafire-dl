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

### macOS

From this project folder:

```bash
python3 -m pip install --user .
```

Then run:

```bash
mediafire-dl
```

If your terminal says `mediafire-dl` was not found, use the module form instead:

```bash
python3 -m mediafire_dl
```

If the command is installed but your shell cannot find it, add Python's user script folder to your PATH. The version number may be different on your machine:

```bash
echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Windows

From this project folder in PowerShell:

```powershell
py -m pip install --user .
```

Then run:

```powershell
mediafire-dl
```

If PowerShell says `mediafire-dl` was not found, use:

```powershell
py -m mediafire_dl
```

If you want the `mediafire-dl` command to work directly, add Python's user Scripts folder to PATH. It usually looks like this, with the Python version adjusted for your install:

```text
%APPDATA%\Python\Python312\Scripts
```

### Linux

From this project folder:

```bash
python3 -m pip install --user .
```

Then run:

```bash
mediafire-dl
```

If your shell says `mediafire-dl` was not found, use:

```bash
python3 -m mediafire_dl
```

Or add Python's user script folder to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
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

This repo already ignores common private and generated files in `.gitignore`, including `.env`, cookies, logs, caches, virtual environments, `.DS_Store`, partial downloads, and local media/download folders.

## Development

For an editable install while working on the code:

```bash
python3 -m pip install --user -e .
```

Run the CLI from source:

```bash
python3 -m mediafire_dl
```

The package entry point is:

```bash
mediafire-dl
```

## License

MIT License. See [LICENSE](LICENSE).
