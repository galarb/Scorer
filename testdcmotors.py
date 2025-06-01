from time import sleep
from dcmotdriver import dcmotdriver
kicker = dcmotdriver(16,12)
kicker.motgo(50)
sleep (2)
kicker.stophard()
sleep(2)

