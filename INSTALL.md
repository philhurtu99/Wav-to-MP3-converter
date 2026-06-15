# Installation

## macOS - desktop app

Download the GitHub Actions artifact or release asset:

```text
WAV-to-MP3-Converter-macOS.zip
```

Then:

1. Unzip the file.
2. Move `WAV to MP3 Converter.app` to `/Applications`.
3. Open the app.
4. If macOS blocks the app because it is not signed: right-click the app -> **Open** -> **Open**.

> Note: the app uses `ffmpeg`. Install it with `brew install ffmpeg` if needed.

## Windows - desktop app

Download the GitHub Actions artifact or release asset:

```text
WAV-to-MP3-Converter-Windows.zip
```

Then:

1. Unzip the file.
2. Run `WAV to MP3 Converter.exe`.
3. If Windows SmartScreen blocks the app because it is not signed: click **More info** -> **Run anyway**.

> Note: install `ffmpeg` and make sure it is available in the Windows PATH, or use Chocolatey: `choco install ffmpeg`.

## Linux - CLI for any distribution

Recommended source install:

```bash
python3 -m pip install .
wav-to-mp3 ~/Music/album --output-dir ~/Music/mp3
```

Or download the binary artifact:

```text
wav-to-mp3-linux-x86_64.tar.gz
```

Then:

```bash
tar -xzf wav-to-mp3-linux-x86_64.tar.gz
chmod +x wav-to-mp3
./wav-to-mp3 ~/Music/album --output-dir ~/Music/mp3
```

Install `ffmpeg` for your distribution:

```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## CLI examples

Convert two files:

```bash
wav-to-mp3 song1.wav song2.wav
```

Convert all WAV files in a folder to an output folder:

```bash
wav-to-mp3 ./wav --output-dir ./mp3
```

Change the bitrate:

```bash
wav-to-mp3 ./wav -o ./mp3 --bitrate 192k
```
