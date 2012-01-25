import daisy

panel = daisy.Daisy23(0,0x5A,'D1','6')
panel.mpr_init()
panel.lcd_init()

panel.lcd_lightOn()

while True:
	if panel.mpr_irq():
		n,state = panel.button_state()
		panel.lcd_setCursor(0, 0)
		panel.lcd_print('N=' + str(n))
		panel.lcd_setCursor(7, 0)
		panel.lcd_print('> v o < ^')
		panel.lcd_setCursor(7, 1)
		for i in range(0, 5):
			panel.lcd_print(str(state[i]) + ' ')
