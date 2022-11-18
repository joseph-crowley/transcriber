# transcriber
transcribe audio using [openai/whisper](https://github.com/openai/whisper.git)

#### dependencies 
[conda](https://docs.conda.io/en/latest/miniconda.html)

[brew](https://brew.sh/)


NOTE: using conda environments, you'll want to do the pip steps _AFTER_ activating the conda environment. see the [local environment setup](https://github.com/joseph-crowley/transcriber/blob/main/README.md#use-the-app-locally)

## use the app locally
### environment [ macOS ]
```
brew install ffmpeg
conda env create -n transcribe
conda activate transcribe
conda install pip 
pip install git+https://github.com/openai/whisper.git 
pip install setuptools-rust
conda install flask
```
### setup and run
```
git clone git@github.com:joseph-crowley/transcriber.git
cd transcriber
conda activate transcribe
flask run
```
then the app will run at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## endpoints

### [/](http://127.0.0.1:5000) 
home page with links for the audio and transcripts of the files in /uploads 

### [upload](http://127.0.0.1:5000/upload)
choose a file for upload. currently only supports mp3 and m4a

### [transcribe/\<name\>](http://127.0.0.1:5000/transcribe/audio.mp3)
if _name_ is an mp3 file, it will transcribe the audio and display on the screen

### [uploads/\<name\>](http://127.0.0.1:5000/uploads/audio.mp3)
play the audio file
