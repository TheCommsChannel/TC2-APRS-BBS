# TC²-BBS APRS Version

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1OZ22Z)

This is the TC²-BBS for APRS. The system allows for basic mail messages for specific users and bulletin boards. 
This is an APRS BBS only because it uses the APRS protocol and it's not meant to be used on the nationwide APRS freq 144.390MHz.
Ideally, this is meant to be used within the following frequency ranges (US users):
2M - 144.90-145.10 & 145.50-145.80

The BBS currently allows for the posting and viewing of Bulletins and Messages for end-users by callsign. More features coming soon!

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
   
   **[MYCALL]**  
   This is where you enter the callsign of your BBS. This can be your FCC callsign or eventually a tactical callsign (like BBS). If using a tactical call the BBS will need to transmit your FCC call every 10 minutes while in operation. This hasn't been implemented yet however, so it's best to use your FCC call until then.
   
   **[KISS_HOST & KISS PORT]**  
   IP Address and Port of the host running direwolf (127.0.0.1 if the BBS is running on the same system)   
   
   **[BULLETIN_EXPIRATION_DAYS]**  
   Number of days to have bulletins expire 

   **[APRS_PATH]**  
   The WIDEN-n path for digipeater hops 
   
   **[RAW_PACKET_DISPLAY]**  
   Display RAW packet data on the terminal - "True" to display or "False" to not display 


### Running the Server

Run the server with:

```sh
python main.py
```

Be sure you've followed the Python virtual environment steps above and activated it before running.
You should see (venv) at the beginning of the command prompt

## BBS Usage

To interact with the BBS, send a message to the callsign of the BBS (whatever has been put into the MYCALL part of the config)
If the message that's sent isn't a command, the BBS will respond with a welcome message and list of the below commands:

**(L)IST**  
Sending a message with `L` will respond with a list of current bulletins

**(M)SG**  
Sending a message with `M` will respond with a list of messages that were sent to the callsign of the user requesting the list of messages.

**(P)OST**  
This command posts a bulletin and needs to be sent in the following format:  
```P <text>```  
Example: ```P Checkpoint 3 operational. Volunteers needed.```

**(S)END**  
This command leaves a message for a specific user via their callsign and needs to be sent in the following format:  
```S <callsign> <text>```  
Example: ```S N0CALL-1 Meet at the Trailhead at 15:00```  

The BBS will send a notification to the callsign letting them know they have a message waiting.

## Automatically run at boot

Instructions coming soon....

## License

GNU General Public License v3.0
