from ui.cTechmanModbusClient import TechmanModbusClient
import time

roboter = TechmanModbusClient('192.168.99.21')
# tstart = time.time()
# roboter.write_dint(9000, [100])
# tend = time.time()
# print(roboter.read_dint(9000, 2))
# print("Error")
# while roboter.read_dint(9500, 2) != [100]:
#     if tend - tstart > 1000000:
#         break  # an dieser Stelle muss ein Fehlerhandling passieren
#     else:
#         print(f'aktuelle Betriebsart im K9000: {roboter.read_dint(9500, 1)}')
#         print("Betriebsart Einlesen")
#         pass

# roboter.write_dint(9002, [0])
# roboter.write_dint(9002, [1])
# roboter.write_dint(9000, [100])
# roboter.write_dint(9000, [0])
# roboter.write_dint(9500, [0])
# roboter.write_dint(9004, [0])
# roboter.write_dint(9004, [1])
# roboter.write_dint(9101, [2, 3]*25)
# roboter.write_dint(9101, [0]*50)
print(f'Kanal 9000: {roboter.read_dint(9000, 1)}')
print(f'Kanal 9500: {roboter.read_dint(9500, 1)}')
# print(f'Kanal 9002: {roboter.read_dint(9002, 1)}')
# print(f'Kanal 9502: {roboter.read_dint(9502, 1)}')
# print(f'Kanal 9101: {roboter.read_dint(9101, 50)}')
# print(f'Kanal 9601: {roboter.read_dint(9601, 50)}')
# print(f'Kanal 9004: {roboter.read_dint(9004, 1)}')
# print(f'Kanal 9504: {roboter.read_dint(9504, 1)}')


