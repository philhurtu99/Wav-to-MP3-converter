# Convertisseur WAV → MP3

Petite app pour convertir des fichiers `.wav` en `.mp3`.

- macOS : app graphique drag & drop
- Windows : app graphique classique
- Linux : CLI portable pour toutes les distributions

## macOS / Windows — app graphique

1. Télécharge l'artefact ou la release correspondant à ton OS.
2. Lance l'app.
3. Optionnel : clique sur **Choisir dossier de sortie**.
4. Glisse un ou plusieurs fichiers `.wav` dans la zone centrale, ou clique sur **Choisir des fichiers WAV**.
5. Les fichiers `.mp3` apparaissent dans le dossier de sortie choisi. Si aucun dossier n'est choisi, ils apparaissent à côté des `.wav` originaux.

Voir aussi : [INSTALL.md](INSTALL.md)

## Linux / CLI

Installer depuis le code source :

```bash
python3 -m pip install .
wav-to-mp3 ./mes-wav --output-dir ./mp3
```

Ou utiliser le binaire Linux généré par GitHub Actions :

```bash
tar -xzf wav-to-mp3-linux-x86_64.tar.gz
./wav-to-mp3 ./mes-wav --output-dir ./mp3
```

Exemples CLI :

```bash
# Convertir un fichier
wav-to-mp3 chanson.wav

# Convertir plusieurs fichiers
wav-to-mp3 chanson1.wav chanson2.wav -o ./mp3

# Convertir tous les WAV d'un dossier
wav-to-mp3 ./album --output-dir ./mp3

# Choisir le bitrate
wav-to-mp3 ./album -o ./mp3 --bitrate 192k
```

## Pré-requis

`ffmpeg` doit être installé.

```bash
# macOS
brew install ffmpeg

# Windows avec Chocolatey
choco install ffmpeg

# Debian/Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## Développement

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

## Build local

macOS / Linux :

```bash
./scripts/build-release.sh
```

Windows PowerShell :

```powershell
.\scripts\build-windows.ps1
```

Les artefacts sont produits dans `release/`.
