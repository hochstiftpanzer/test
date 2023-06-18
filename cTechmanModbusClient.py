# -*- coding: utf-8 -*-
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import time


# =============================================================================
# Allgemeines Modbusdevice mit zusätzlichen eigenschaften zum Lesen und Schreiben
# verschiedener Variablenformate
# =============================================================================


class FloatModbusClient(ModbusClient):
    # Umwandeln von holding Registerwert in Float
    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    # Umwandeln von input Registerwert in Float
    def read_inputFloat(self, address, number=1):
        reg_l = self.read_input_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    # Float als Eingabe aus 2 Bit umschreiben und auf Register schreiben
    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)

    # String vom inputRegister lesen, länge des Strings parametrierbar
    def read_inputString(self, address, number=1):
        reg_l = self.read_input_registers(address, number)
        if reg_l:
            return BinaryPayloadDecoder.fromRegisters(reg_l, byteorder=Endian.Big, wordorder=Endian.Big).decode_string(
                number).decode()
        else:
            return None

    # String mit parametrierbarer Länge vom holding register lesen
    def read_string(self, address, number=1):
        reg_l = self.read_holding_registers(address, number)
        if reg_l:
            return BinaryPayloadDecoder.fromRegisters(reg_l, byteorder=Endian.Big, wordorder=Endian.Big).decode_string(
                number).decode()
        else:
            return None

    # =============================================================================
    #     String auf gegebene Adresse schreiben, Länge ergibt sich aus der Länge der
    #     eingegebenen Zeichenkette
    # =============================================================================
    def write_string(self, address, string):
        NULL = '\x00'
        builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                       wordorder=Endian.Little)
        builder.add_string(string)
        builder.add_string(NULL)
        outreg = builder.to_registers()
        return self.write_multiple_registers(address, outreg)

    # Dint lesen → 2 bit zu Int konvertierung
    def read_dint(self, adress, number=1):
        reg_l = self.read_holding_registers(adress, number * 2)
        answer = []
        if reg_l:
            for i in range(int(len(reg_l) / 2)):
                answer.append(reg_l[i * 2] * 2 ** 16 + reg_l[i * 2 + 1])
            return answer
        else:
            return None

    # Dint schreiben → Int32 zu 2 bit konvertierung
    def write_dint(self, adress: object, dint_array: object) -> object:
        """

        :rtype: object
        """
        data = []
        for i in dint_array:
            data.append(i // (2 ** 16))
            data.append(i % (2 ** 16))
        self.write_multiple_registers(adress, data)

    def write_int(self, adress, int_array):
        self.write_multiple_registers(adress, int_array)

    def read_int(self, adress, int_array):
        self.read_holding_registers(adress, int_array)

# =============================================================================
# Zusammenfassung der Wichtigsten eigenschaften des TM Roboters und der allgemeinen
# Modbusfunktionen aus dem FloatModbusClient
# 
# einige Funktionalitäten funktionieren nur, wenn die Dis und Dos des Roboters
# gebrückt werden
# =============================================================================
class TechmanModbusClient(FloatModbusClient):
    def runProgram(self):
        timeout = 2
        zahler = 0
        if not self.read_discrete_inputs(7202, 1)[0]:
            # DO -- Di Schalten
            self.write_single_coil(12, True)
            time.sleep(0.2)
            self.write_single_coil(12, False)
            while not self.read_discrete_inputs(7202, 1)[0]:
                time.sleep(0.1)
                zahler += 0.1
                if zahler >= timeout:
                    self.runProgram()
        else:
            print("Programm already running")

    def pauseProgram(self, pause=True):
        timeout = 2
        zahler = 0
        # DO -- Di Schalten
        # pausing
        if pause and (self.read_discrete_inputs(7202, 1)[0] and not self.read_discrete_inputs(7204, 1)[0]):
            self.write_single_coil(12, True)
            time.sleep(0.2)
            self.write_single_coil(12, False)
            while not self.read_discrete_inputs(7204, 1)[0]:
                time.sleep(0.1)
                zahler += 0.1
                if zahler >= timeout:
                    self.pauseProgram()
        # unpausing
        elif not pause and (self.read_discrete_inputs(7202, 1)[0] and self.read_discrete_inputs(7204, 1)[0]):
            self.write_single_coil(12, True)
            time.sleep(0.2)
            self.write_single_coil(12, False)
            while self.read_discrete_inputs(7204, 1)[0]:
                time.sleep(0.1)
                zahler += 0.1
                if zahler >= timeout:
                    self.pauseProgram()
        else:
            print("Program not running")

    def stopProgram(self):
        self.write_single_coil(13, True)
        time.sleep(0.2)
        self.write_single_coil(13, False)

    def setProgram(self, ProgramName):
        #        self.open()
        return self.write_string(7701, ProgramName)

    #        self.close()

    def readProgram(self):
        #        self.open()
        return self.read_inputString(7701, 99)

    #        self.close

    # emulierte Plus Taste
    def Plus(self):
        self.write_single_coil(9, True)
        time.sleep(0.2)
        self.write_single_coil(9, False)

    # emulierte Minus Taste
    def Minus(self):
        self.write_single_coil(10, True)
        time.sleep(0.2)
        self.write_single_coil(10, False)

    # emulierte Manuell Taste
    def Manuell(self):
        self.write_single_coil(11, True)
        time.sleep(0.2)
        self.write_single_coil(11, False)

    # emulierte automatische Umschaltung in Automodus
    def Auto(self):
        # lange M/A drücken
        self.write_single_coil(11, True)
        time.sleep(2.5)
        self.write_single_coil(11, False)
        time.sleep(0.3)
        self.Plus()
        time.sleep(0.3)
        self.Minus()
        time.sleep(0.3)
        self.Plus()
        time.sleep(0.3)
        self.Plus()
        time.sleep(0.3)
        self.Minus()
