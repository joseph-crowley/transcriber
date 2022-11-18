# transcriber
transcribe audio using openai/whisper 

#### dependencies 
follow all of the steps in the [readme for whisper](https://github.com/openai/whisper.git)
NOTE: if using conda environments, you'll want to do the pip steps _AFTER_ activating the transcribe environment.
in short (on macOS):
```
brew install ffmpeg
pip install git+https://github.com/openai/whisper.git 
pip install setuptools-rust
```

## use the app locally
```
git clone git@github.com:joseph-crowley/transcriber.git
cd transcriber
conda create -n transcribe -f environment.yml
conda activate transcribe
flask run
```
then the app will run at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## endpoints

### / 
just a hello world page, placeholder for now. 

### upload
choose a file for upload. currently only supports mp3

### transcribe/<name>
if _name_ is an mp3 file, it will transcribe the audio and display on the screen

### uploads/<name>
play the audio file
