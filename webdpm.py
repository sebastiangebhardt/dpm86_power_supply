import json
from typing import Union
from fastapi import FastAPI
from dpm86oo import dpm86

app = FastAPI()
dpm = dpm86(
        port = "/dev/ttyUSB0",
        baudrate = 9600,
        timeout=0.5, 
        inter_byte_timeout=0.1
)

@app.get("/temp") # read the temperature
def read_temp():
    return {"temp": dpm.temperature()}

@app.get("/power") # read the actual delivered power
def read_power():
    return {"power": dpm.power()} 

@app.get("/output") # read the actual output state (on/off)
def read_output():
    return {"Output": dpm.output()} 

@app.patch("/output")
def patch_output(set: str):
    if set in ['1', 'on']:
        return {"action": dpm.output(dpm.P_ON)} # output 1/on -- turn the output on"
    else:
        return {"action": dpm.output(dpm.P_OFF)} # output 0/off/"else" -- turn the output off
    
@app.get("/voltage")
def read_voltage(q: Union[str, None] = None):
    if q == 'max':
        return {"voltage": dpm.setting("v", q)} # read the maximum output voltage
    elif q in ['target', 'setting']:
        return {"voltage": dpm.setting("v")} # read the voltage target
    else:
        return {"voltage": dpm.voltage()} # read the actual delivered voltage

@app.patch("/voltage")
def patch_voltage(value: float): # set the voltage target
    return {"voltage": dpm.setting("v",value)}

@app.get("/current")
def read_current(q: Union[str, None] = None):
    if q == 'max':
        return {"current": dpm.setting("c", q)} # read the maximum output current
    elif q in ['target', 'setting']:
        return {"current": dpm.setting("c")} # read the current target
    else:
        return {"current": dpm.current()} #  read the actual deliviered current
    
@app.patch("/current")
def patch_voltage(value: float): # set the current target
    return {"current": dpm.setting("c",value)}

@app.get("/const")
def read_const():
    return {"const": dpm.const()} #  read the actual const setting (voltage/const)
    
@app.patch("/const_voltage")
def patch_const_voltage(value: float): # set constant voltage delivery
    return {"const_voltage": dpm.const(dpm.P_VOLTAGE)}

@app.patch("/const_current")
def patch_const_current(value: float): # set constant current delivery
    return {"const_current": dpm.const(dpm.P_CURRENT)}
