# TC²-BBS Meshtastic Version

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1OZ22Z)

This is the TC²-BBS for APRS. The system allows for basic mail message for specific users and bulletin boards. 
This is an APRS BBS only because it uses the APRS protocol and it's not meant to be used on the nationwide APRS freq 144.390MHz.
Ideally, this is meant to be used within the following frequency ranges (US users):
2M - 144.90-145.10 & 145.50-145.80


## Setup

### Requirements

- Python 3.x
- `requests`
- `aprs3`

### Update and Install Git
   
   ```sh
   sudo apt update
   sudo apt upgrade
   sudo apt install git
   ```

### Installation (Linux)

1. Clone the repository:
   
   ```sh
   cd ~
   git clone https://github.com/TheCommsChannel/TC2-APRS-BBS.git
   cd TC2-APRS-BBS
   ```

2. Set up a Python virtual environment:  
   
   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:  
 
   ```sh
   source venv/bin/activate
   ```

4. Install the required packages:  
   
   ```sh
   pip install -r requirements.txt
   ```

5. Rename `example_config.ini`:

   ```sh
   mv example_config.ini config.ini
   ```

6. Set up the configuration in `config.ini`:  

   You'll need to open up the config.ini file in a text editor and make your changes following the instructions below
   
   **MYCALL**  
   This is where you enter the callsign of your BBS. This can be your FCC callsign or eventually a tactical callsign (like BBS). If using a tactical call the BBS will need to transmit your FCC call every 10 minutes while in operation. This hasn't been implemented yet however, so it's best to use your FCC call until then.
   
   **KISS_HOST & KISS PORT**  
   IP Address and Port of the host running direwolf (127.0.0.1 if the BBS is running on the same system)   
   
   **BULLETIN_EXPIRATION_DAYS**  
   Number of days to have bulletins expire 

   **APRS_PATH**  
   The WIDEN-n path for digipeater hops 
   
   **RAW_PACKET_DISPLAY**  
   IP Address of the host running direwolf (127.0.0.1 if the BBS is running on the same system) 


### Running the Server

Run the server with:

```sh
python main.py
```

Be sure you've followed the Python virtual environment steps above and activated it before running.
You should see (venv) at the beginning of the command prompt


## Automatically run at boot

Instructions coming soon....

## License

GNU General Public License v3.0