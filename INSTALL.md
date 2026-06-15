# Installation

## macOS — app classique

Télécharge l'artefact GitHub Actions ou la release :

```text
Convertisseur-WAV-vers-MP3-macOS.zip
```

Puis :

1. Dézippe le fichier.
2. Glisse `Convertisseur WAV vers MP3.app` dans `/Applications`.
3. Ouvre l'app.
4. Si macOS bloque l'ouverture car l'app n'est pas signée : clic droit → **Ouvrir** → **Ouvrir**.

> Note : l'app utilise `ffmpeg`. Installe-le avec `brew install ffmpeg` si nécessaire.

## Windows — app classique

Télécharge l'artefact GitHub Actions ou la release :

```text
Convertisseur-WAV-vers-MP3-Windows.zip
```

Puis :

1. Dézippe le fichier.
2. Lance `Convertisseur WAV vers MP3.exe`.
3. Si Windows SmartScreen bloque l'app car elle n'est pas signée : **Informations complémentaires** → **Exécuter quand même**.

> Note : installe `ffmpeg` et assure-toi qu'il est dans le PATH Windows, ou utilise Chocolatey : `choco install ffmpeg`.

## Linux — CLI toutes distributions

Option recommandée avec Python :

```bash
python3 -m pip install .
wav-to-mp3 ~/Musique/album --output-dir ~/Musique/mp3
```

Ou télécharge l'artefact binaire :

```text
wav-to-mp3-linux-x86_64.tar.gz
```

Puis :

```bash
tar -xzf wav-to-mp3-linux-x86_64.tar.gz
chmod +x wav-to-mp3
./wav-to-mp3 ~/Musique/album --output-dir ~/Musique/mp3
```

Installe `ffmpeg` selon ta distribution :

```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## CLI — exemples

Convertir deux fichiers :

```bash
wav-to-mp3 song1.wav song2.wav
```

Convertir tous les WAV d'un dossier vers un dossier de sortie :

```bash
wav-to-mp3 ./wav --output-dir ./mp3
```

Changer le bitrate :

```bash
wav-to-mp3 ./wav -o ./mp3 --bitrate 192k
```
