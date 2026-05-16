# Mediafire-DL

Mediafire-DL is a small command-line downloader for public MediaFire links.

It handles single files and folders, keeps nested folder structure intact, and shows a clean progress display while it downloads. It does not use browser cookies, account sessions, saved passwords, or private MediaFire access.

## What It Does

- Downloads public MediaFire file links
- Downloads public MediaFire folder links
- Walks nested folders automatically
- Saves folders using the same folder layout MediaFire reports
- Shows a file preview before downloading
- Supports a dry-run mode so you can check what would be saved first
- Defaults to your system `Downloads` folder

## Install

You need Python 3.9 or newer.

From this project folder, install it with:

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

On Windows, use `py` instead of `python3`:

```powershell
py -m pip install --user .
py -m mediafire_dl
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

## Supported Links

Supported:

- Public MediaFire file links
- Public MediaFire folder links
- Public folders with nested subfolders

Not supported:

- Private links that require a MediaFire login
- Password-protected downloads
- Links that require browser cookies
- Account-only files
- Captcha-gated or blocked downloads

## Privacy And Safety

Mediafire-DL does not ask for MediaFire login details and does not read browser cookies.

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
