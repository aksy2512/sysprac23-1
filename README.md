# TransformX

![TransformX Logo](https://i.gifer.com/origin/c5/c5f36cbf85f0dd53cca234142247416f.gif)

TransformX is a file conversion service that allows users to convert various file types to different formats. This service supports a wide range of file formats, including document files, image files, audio files, and video files.

## Team Details
1. [Yash Sharma](https://github.com/yashcode00)
2. [Vinayak Sachan](https://github.com/metavinayak)
3. [Akshar Singh](https://github.com/aksy2512)
4. [Gautam Dhulipala](https://github.com/gd-codes)
5. [Ashutosh Sharma](https://github.com/ashu3103)
6. [Shashwat Sharma](https://github.com/shashwat-1-11)

## Features

- User-friendly web interface for uploading and converting files
- RESTful API for integrating with other applications and workflows
- Cloud storage integration for accessing files from Dropbox, Google Drive, or Microsoft OneDrive
- Support for multiple file formats, including popular file types such as PDF, DOCX, JPG, MP3, and MP4
- Conversion engine with high accuracy and fast processing speeds
- Secure file transfer and storage with encryption, authentication, and access controls

### To run the source code :
1. Clone the repository or Extract the submitted ZIP file
2. You will need an installation of Python 3.7 or newer
3. From the terminal/command line, `cd` into the root folder of the repo
4. Create a virtual environment, `python3 -m venv ./venv`
5. Activate the venv, `source ./venv/bin/activate` on \*nix or `venv\Scripts\activate.bat` on CMD
6. Install the required libraries, `pip3 install -r requirements.txt`
7. Entrypoint : Run `python3 app.py`
8. This will start a flask webserver on port 5000. You can open the website in your browser at `http://localhost:5000/`

## Addition support for APIs:
1. Install `ffpmeg` for Audio conversion. Use `sudo apt install ffmpeg` to install it on Ubuntu
2. Install `wkhtmltopdf` for HTML conversion. Use `sudo apt-get install wkhtmltopdf` to install it on Ubuntu
3. Install `poppler` for PDF to Image conversion. Use `sudo apt-get install poppler-utils` to install it on Ubuntu

## Docker
1. sudo docker build -t sysprac .
2. sudo docker run -p 5000:5000 sysprac
3. open `http://localhost:5000/`
## docker-compose.yml
1. sudo docker compose up --build
## Usage

To use TransformX, simply visit the web interface and select the file you want to convert. Choose the desired output format and click the convert button. The converted file will be available for download within a few minutes. If you prefer to use the API, you can integrate TransformX with your application using the provided API documentation.

### Supported Conversions

| From/To | Image ^ | PDF | DOCX | MP3 | WAV | CSV | TSV |
|---------|---------|-----|------|-----|-----|-----|-----|
| Image ^ | ✔️       | ✔️   |      |     |     |     |     |
| PDF     | ✔️       |     | ✔️    |     |     |     |     |
| DOCX    |         | ✔️   |      |     |     |     |     |
| MP3     |         | ✔️ * |      |     | ✔️   |     |     |
| WAV     |         | ✔️ * |      | ✔️   |     |     |     |
| XLSX    |         |     |      |     |     | ✔️   | ✔️   |
| HTML    |         | ✔️   |      |     |     |     |     |

> **\*** Using Speech Recognition
> **^** Only Non-Raw Raster Formats

## Contributing

We welcome contributions from the community! If you have any ideas for new features, bug fixes, or improvements, please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
