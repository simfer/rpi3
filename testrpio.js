var rpio = require('rpio');
//rpio.open(22, rpio.OUTPUT);
//console.log('Pin 22 is currently ' + (rpio.read(22) ? 'high' : 'low'));

var options = {
    gpiomem: false,          /* Use /dev/gpiomem */
    mapping: 'physical',    /* Use the P1-P40 numbering scheme */
    mock: undefined,        /* Emulate specific hardware in mock mode */
}

//rpio.init(options);

rpio.i2cBegin();

rpio.i2cSetSlaveAddress(0x23);

var rxbuf = new Buffer(32);

rpio.i2cRead(rxbuf, 16);

console.log(rxbuf);

rpio.i2cEnd();
