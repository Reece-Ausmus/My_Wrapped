# My Wrapped

My Wrapped is a personal project that uses the Spotify API to collect and store all songs and podcasts that you listen to on Spotify. It then analyzes this data to present information similar to Spotify Wrapped.

## Installation

To install My Wrapped, clone the repository and install the dependencies:

```sh
git clone https://github.com/Reece-Ausmus/My_Wrapped.git
cd My_Wrapped
pip install -r requirements.txt
```

It is recommended to use a python virtual environment, but not required. If using a virtual environment, be sure to run `pip install -r requirements.txt` from the virtual environment.

## Usage

To start the server, run the following command:

```sh
python app.py [-wb | --web-browser]
```

### `-wb, --web-browser`

The `-wb` flag allows you to use the current webbrowser you have open instead of opening a new window with selenium.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [reece@ausmusfamily.com](mailto:reece@ausmusfamily.com).
