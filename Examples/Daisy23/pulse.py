import daisy
import time

panel = daisy.Daisy23(0,0x5A,'D1','5')
panel.mpr_init()
panel.lcd_init()

panel.lcd_lightOn()
panel.lcd_setCursor(4,0)
panel.lcd_print('Madefree')
panel.lcd_setCursor(3,1)
panel.lcd_print('Electronics')

while True:
	for i in range(0,15):
		panel.lcd_setLight(15-i)
                time.sleep(0.1)

	for i in range(1,15):
		panel.lcd_setLight(i)
		time.sleep(0.1)
