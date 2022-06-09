pc = 0
rom = [8, 9, 10, 11] * 256
rom_addr = 0
rom_data = 0
ip = 0


def mod_pc(address, oe, rw, inc):
    global pc
    if not rw:
        pc = address
    if not inc:
        pc += 1
    if not oe:
        return pc
    else:
        return address


def mod_rom(address, oe, rw):
    global rom, rom_addr, rom_data
    if not rw:
        rom_addr = address
    else:
        rom_data = rom[rom_addr]
    if not oe:
        return rom_data
    else:
        return address


def mod_instr(address, oe, rw):
    global ip
    if ip == 0:
        ip += 1
        return 0, 1, 1, 1, 0, 1, 1
    elif ip == 1:
        ip += 1
        return 1, 1, 0, 0, 1, 1, 0
    else:
        if not rw:
            if address == 8:
                print("instr!")
        ip = 0
        return 1, 1, 1, 1, 1, 1, 1


bus = -1
pc_en = 1
pc_rw = 1
pc_inc = 1
rom_en = 1
rom_rw = 1
instr_en = 1
instr_rw = 1
for i in range(15):
    pc_en, pc_rw, pc_inc, rom_en, rom_rw, instr_en, instr_rw = mod_instr(bus, instr_en, instr_rw)
    bus = mod_pc(bus, pc_en, pc_rw, pc_inc)
    bus = mod_rom(bus, rom_en, rom_rw)
    print(bus)
