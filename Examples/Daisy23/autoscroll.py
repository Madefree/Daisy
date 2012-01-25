import daisy
import time

panel = daisy.Daisy23(0,0x5A,'D6','6')
panel.mpr_init()
panel.lcd_init()

panel.lcd_lightOn()

while True:
	panel.lcd_setCursor(0,0)
	for i in range (0,10):
		panel.lcd_print(str(i))
		time.sleep(0.5)

	panel.lcd_setCursor(16,1)
	panel.lcd_autoscroll()
        for i in range (0,10):
                panel.lcd_print(str(i))
                time.sleep(0.5)

	panel.lcd_noAutoscroll()
	panel.lcd_clear()
