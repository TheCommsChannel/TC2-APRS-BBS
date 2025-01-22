# TC²-BBS APRS Version

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1OZ22Z)

This is the TC²-BBS for APRS. The system allows for basic mail messages for specific users and bulletin boards. 
This is an APRS BBS only because it uses the APRS protocol and it's not meant to be used on the nationwide APRS freq 144.390MHz.
Ideally, this is meant to be used within the following frequency ranges (US users):
2M - 144.90-145.10 & 145.50-145.80

The BBS currently allows for the posting and viewing of Bulletins and Messages for end-users by callsign. More features 
coming soon. This software is experimental and could have bugs. Bug reports and suggestions are welcomed.

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
   
   **[TACTICAL_CALL]**  
   This is where you enter the callsign of your BBS. This can be your FCC callsign if you don't plan on using a tactical call or a tactical callsign like BBS, CAMP1, or whatever makes the most sense for you.
   
   **[STANDARD_CALL]**  
   If using a Tactical Call in the TACTICAL_CALL field, be sure to enter in your ham radio callsign here to ensure your callsign is in the packets to comply with FCC regulations. If you're using your ham radio callsign in the TACTICAL_CALL field, you can just leave this as TC2BBS.

   **[KISS_HOST & KISS PORT]**  
   IP Address and Port of the host running direwolf (127.0.0.1 if the BBS is running on the same system)   
   
   **[BULLETIN_EXPIRATION_DAYS]**  
   Number of days to have bulletins expire 

   **[APRS_PATH]**  
   The WIDEN-n path for digipeater hops 
   
   **[RAW_PACKET_DISPLAY]**  
   Display RAW packet data on the terminal - "True" to display or "False" to not display 

### [OPTIONAL] Steps for Bluetooth TNC Radio Users 

1.  Run the following command to make the necessary scripts executable.
    ```sh
    chmod +x bt_pair.exp rfcomm_bind.sh
    ```

2. Install "expect"
   ```sh
   sudo apt install expect
   ```

3. Pairing radio: 
   The first time you connect your radio, it will need to be paired and trusted. The bt_pair.exp makes this process easy. It will search for currently known Bluetooth TNC capable radios ("VR-N76" "UV-PRO" "GA-5WB" "TH-D75" "TH-D74" "VR-N7500") If one is found, it will pair, trust, and save the info in a file for the binding script in the next step. This step only needs to be performed once when you're first setting things up, or wanting to use a different radio.  

    Put your radio in pairing mode and run the follwing command to go through the pairing process:
    ```sh
    ./bt_pair.exp
   ```   

4. Binding the radio to a serial port:
   This will need to be run before you start the server (not every time; likely only after a reboot). If you're not sure, you can run the `rfcomm` command and if you see something listed, you probably don't need to run this script. If you get nothing from the `rfcomm` command then you need to run this script to bind your radio to the serial port. After running this command, you can continue on to the "Running the Server" section

    Run the following command to bind your radio to the serial port
    ```sh
   ./rfcomm_bind.sh
   ```

### Running the Server

Run the server with:

```sh
python main.py
```

Be sure you've followed the Python virtual environment steps above and activated it with `source venv/bin/activate` before running.
You should see (venv) at the beginning of the command prompt

## BBS Usage

To interact with the BBS, send a message to the callsign of the BBS (whatever has been put into the MYCALL part of the config)
If the message that's sent isn't a command, the BBS will respond with a welcome message and list of the below commands:

**(L)IST**  
Sending a message with `L` will respond with a list of current bulletins

**(M)SG**  
Sending a message with `M` will respond with a list of messages that were sent to the callsign of the user requesting the list of messages.

**(S)END**  
This command leaves a message for a specific user via their callsign and needs to be sent in the following format:  
```S <callsign> <text>```  
Example: ```S N0CALL-1 Meet at the Trailhead at 15:00```  

The BBS will send a notification to the callsign letting them know they have a message waiting.

**(P)OST**  
This command posts a bulletin and needs to be sent in the following format:  
```P <text>```  
Example: ```P Checkpoint 3 operational. Volunteers needed.```

**(P)OST (U)RGENT**
This command will post an urgent bulletin which will have the BBS send out a bulletin packet which will be seen by all 
supported devices. It needs to be sent in the following format:  
```PU <text>```  
Example: ```PU Highway 12 closed. Use alternate routes.```

## Automatically run at boot

Instructions coming soon....

