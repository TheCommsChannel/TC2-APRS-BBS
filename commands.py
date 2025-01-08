import database
import aprs_comm

def handle_command(callsign, command):
    normalized_callsign = callsign.split('-')[0].upper()
    parts = command.split(' ', 1)
    cmd = parts[0].upper()
    arg = parts[1] if len(parts) > 1 else ''

    if cmd in ['LIST', 'L']:
        bulletins = database.get_bulletins()
        return [
            f"{b[2]} {b[1]}: {b[0]}" for b in bulletins
        ] or ["No bulletins available."]

    elif cmd in ['MSG', 'M']:
        messages = database.get_messages_for_user(normalized_callsign)
        return [
            f"From {m[0]} ({m[2]}): {m[1]}" for m in messages
        ] or ["No messages for you."]

    elif cmd in ['POST', 'P']:
        if arg:
            database.add_bulletin(normalized_callsign, arg)
            return ["Bulletin posted."]
        return ["Usage: POST <text>"]

    elif cmd in ['SEND', 'S']:
        args = arg.split(' ', 1)
        if len(args) == 2:
            recipient, message = args
            database.add_message(normalized_callsign, recipient, message)

            notification = f"You have a new message from {normalized_callsign}."
            aprs_comm.send_direct_message(recipient, notification)

            return [f"Message sent to {recipient}."]
        return ["Usage: SEND <callsign> <text>"]

    elif cmd in ['PU']:
        if arg:
            database.add_bulletin(normalized_callsign, f"URGENT: {arg}")

            urgent_bulletin = f"URGENT: {arg}"
            bulletin_id = "BLN1"
            aprs_comm.send_bulletin(bulletin_id, urgent_bulletin)

            return ["Urgent bulletin posted and transmitted."]
        return ["Usage: PU <text>"]


    else:
        return [
            "Hello and Welcome to the TC2-BBS!",
            "Please send a message with one of the commands below.",
            "Commands: (L)IST, (M)SG, (P)OST <text>, (S)SEND <callsign> <text>"
        ]