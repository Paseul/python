# import the library
import can

# create a bus instance
# many other interfaces are supported as well (see below)
bus = can.Bus(interface='socketcan',
              channel='vcan0',
              receive_own_messages=True)

# send a message
message = can.Message(arbitration_id=0xc0ffee, is_extended_id=True,
                      data=[0x11, 0x22, 0x33])
bus.send(message, timeout=0.2)

# iterate over received messages
for msg in bus:
    print("{}: {} {} {}".format(msg.arbitration_id, msg.data[0], msg.data[1], msg.data[2] ))

# or use an asynchronous notifier
notifier = can.Notifier(bus, [can.Logger("recorded.log"), can.Printer()])