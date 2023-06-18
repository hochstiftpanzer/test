def senden_an_roboter(self):
    self.IndexHutschiene = self.get_index_hutschiene()
    send = self.liste_alle_hutschienen[self.IndexHutschiene]
    print(send)
    roboter = TechmanModbusClient('192.168.99.21')
    roboter.write_int(9001, send)
    print(roboter.read_int(9001, 50))
    warte_auf_roboter = roboter.read_int(9000, 1)
    gesendet = [send]
    if send not in gesendet:
        return send
    else:
        pass
    self.ui.label_command.setText("Wurde schon gesendet")

    if warte_auf_roboter:
        self.ui.label_command.setText("Wurde gesendet")
    else:
        self.ui.label_command.setText("Bitte warten")

        def schiene_senden(self, nummer_hutschiene):
            # tstart = time.time()
            self.roboter.write_dint(9002, [nummer_hutschiene])
            time.sleep(1)
            # print("zzeh")
            self.schiene_handshake()

            while self.roboter.read_dint(9502, 2) != [nummer_hutschiene]:
                time.sleep(1)
                break
            '''
                if time.time - tstart > 1000000.0:
                    continue  # an dieser Stelle muss ein Fehlerhandling passieren
                else:
                    self.schiene_handshake()
                    print(f'aktueller Hutschienenindex K9502: {self.roboter.read_dint(9502, 2)}')
                    print("Hutschienenindex wurde an Roboter gesendet")
                    pass
                '''

        def schiene_handshake(self):
            tstart = time.time()
            self.roboter.write_dint(9004, [1])
            # if time.time - tstart > 1000000.0:
            '''while self.roboter.read_dint(9504, 2) != [1]:
                time.sleep(0.1)
                break'''

        def reihenfolge_handshake(self):
            tstart = time.time()
            self.roboter.write_dint(9006, [1])

            while self.roboter.read_dint(9506, 2) != [1]:
                time.sleep(0.1)
                break

        def programm_einlesen(self):
            tstart = time.time()
            self.roboter.write_dint(9000, [0])
            time.sleep(1)
            self.roboter.write_dint(9000, [100])

            while self.roboter.read_dint(9500, 2) != [100]:
                # print("asd")
                # time.sleep(0.01)
                # print("asd")
                break

        def reihenfolge_senden(self, nummer_hutschiene):
            tstart = time.time()
            self.roboter.write_dint(9101, self.liste_alle_hutschienen[nummer_hutschiene])
            # print(self.roboter.read_dint(9101, [100]))
            self.reihenfolge_handshake()
            while self.roboter.read_int(9601, 100) != self.liste_alle_hutschienen[nummer_hutschiene]:
                time.sleep(0.1)
                break

        def reset_100(self):
            tstart = time.time()
            self.roboter.write_dint(9002, [0])
            self.roboter.write_dint(9004, [0])
            self.roboter.write_dint(9101, [0])
            self.roboter.write_dint(9006, [0])
            while self.roboter.read_dint(9502, 2) != [0] and self.roboter.read_dint(9504, 2) != [0] and \
                    self.roboter.read_dint(9601, 2) != [0] * 100 and self.roboter.read_int(9506, 2) != [0]:
                time.sleep(0.1)
                break