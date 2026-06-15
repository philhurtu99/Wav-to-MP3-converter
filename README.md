# Convertisseur WAV → MP3

Petite app macOS pour glisser-déposer des fichiers `.wav` et créer des `.mp3`.

## Lancer l'app

Le plus simple : double-clique sur l'app créée sur le Bureau :

```text
~/Desktop/Convertisseur WAV vers MP3.app
```

L'app source est ici :

```text
~/wav-to-mp3-app/Convertisseur WAV vers MP3.app
```

Il y a aussi un lanceur Terminal si besoin :

```text
~/wav-to-mp3-app/Convertisseur WAV vers MP3.command
```

## Utilisation

1. Ouvre l'app.
2. Optionnel : clique sur **Choisir dossier de sortie** pour choisir où créer les MP3.
3. Glisse un ou plusieurs fichiers `.wav` dans la zone centrale, ou clique sur **Choisir des fichiers WAV**.
4. Attends le message de confirmation.
5. Les fichiers `.mp3` apparaissent dans le dossier de sortie choisi. Si aucun dossier n'est choisi, ils apparaissent à côté des `.wav` originaux.

## Pré-requis

- Python 3
- ffmpeg installé (`brew install ffmpeg`)

Sur cette machine, `ffmpeg` a déjà été détecté et testé.

## Tests

```bash
cd ~/wav-to-mp3-app
. .venv/bin/activate
pytest -q
```
