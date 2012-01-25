import daisy
import time

panel = daisy.Daisy23(0,0x5A,'D6','6')
panel.mpr_init()
panel.lcd_init()

panel.lcd_lightOn()
panel.lcd_setCursor(0,0)
panel.lcd_print('  Hello World!  ')
panel.lcd_setCursor(0,1)
panel.lcd_print('<-------------->')
time.sleep(1)

while True:
	for i in range(0,15):
		panel.lcd_scrollDisplayLeft()
		time.sleep(0.3)
        for i in range(0,15):
                panel.lcd_scrollDisplayRight()
                time.sleep(0.3)
	time.sleep(1)
	for i in range(0,15):
		panel.lcd_scrollDisplayRight()
		time.sleep(0.3)
        for i in range(0,15):
                panel.lcd_scrollDisplayLeft()
                time.sleep(0.3)
	time.sleep(1)
