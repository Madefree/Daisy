# daisy.py
#
# Python collection of class that allows to easily manage the Daisy 
# building modules made by Acme Systems srl.
# http://foxg20.acmesystems.it
#
# (C) 2011 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os.path
import smbus
import time

# Daisy connectors pin assignments
#
# D1, D2, etc are the connector names on Daisy1 adapter
# http://foxg20.acmesystems.it/doku.php?id=daisy:adapter
#
# 'pin number', 'kernel id'  # pin description

D1_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  70, #PB6
	'3' :  71, #PB7
	'4' :  92, #PB28
	'5' :  93, #PB29
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D2_kernel_ids = {
	'1' :   0, #3V3
	'2' :  63, #PA31
	'3' :  62, #PA30
	'4' :  61, #PA29
	'5' :  60, #PA28
	'6' :  59, #PA27
	'7' :  58, #PA26
	'8' :  57, #PA25
	'9' :  94, #PB30
	'10':   0, #GND
}

D3_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  68, #PB4
	'3' :  69, #PB5
	'4' :  90, #PB26
	'5' :  91, #PB27
	'6' :  86, #PB22
	'7' :  88, #PB24
	'8' :  89, #PB25
	'9' :  87, #PB23
	'10':  0,  #GND
}

D4_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  0, #AVDD
	'3' :  0, #VREF
	'4' :  0, #AGND
	'5' :  96, #PC0
	'6' :  97, #PC1
	'7' :  98, #PC2
	'8' :  99, #PC3
	'9' :  0,  #5V0
	'10':  0,  #GND
}


D5_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  76, #PB12
	'3' :  77, #PB13
	'4' :  80, #PB16
	'5' :  81, #PB17
	'6' :  82, #PB18
	'7' :  83, #PB19
	'8' :  84, #PB20
	'9' :  85, #PB21
	'10':  0,  #GND
}

D6_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  74, #PB10
	'3' :  75, #PB11
	'4' : 104, #PC8
	'5' : 106, #PC10
	'6' :  95, #PB31
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D7_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  65, #PB1
	'3' :  64, #PB0
	'4' :  66, #PB2
	'5' :  67, #PB3
	'6' : 101, #PC5
	'7' : 100, #PC4
	'8' :  99, #PC3
	'9' :   0, #5V0
	'10':   0, #GND
}

D8_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  72, #PB8
	'3' :  73, #PB9
	'4' :   0, #N.C.
	'5' :   0, #N.C.
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

# Kernel ids descriptor for each connector

daisy_connectors = {
	'D1' :  D1_kernel_ids,
	'D2' :  D2_kernel_ids,
	'D3' :  D3_kernel_ids,
	'D4' :  D4_kernel_ids,
	'D5' :  D5_kernel_ids,
	'D6' :  D6_kernel_ids,
	'D7' :  D7_kernel_ids,
	'D8' :  D8_kernel_ids,
}


def get_kernel_id(daisy_connector_name,pin_number):
	return daisy_connectors[daisy_connector_name][pin_number]

def export(kernel_id):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/gpio/export','w')
		f.write(str(kernel_id))
		f.close()

def direction(kernel_id,direction):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/direction','w')
		f.write(direction)
		f.close()

def set_value(kernel_id,value):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def get_value(kernel_id):
	if kernel_id<>-1:
		iopath='/sys/class/gpio/gpio' + str(kernel_id)
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

class Daisy5():

	"""
	DAISY-5 (8 pushbuttons) related class
	http://foxg20.acmesystems.it/doku.php?id=daisy:daisy5_pushbuttons
	"""
	kernel_id=-1

	buttons = {
		'P1' :  '2',
		'P2' :  '3',
		'P3' :  '4',
		'P4' :  '5',
		'P5' :  '6',
		'P6' :  '7',
		'P7' :  '8',
		'P8' :  '9',
	}

	def __init__(self,connector_id,button_id):
		pin=self.buttons[button_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'in')

	def pressed(self):
		if self.kernel_id<>-1:
			iopath='/sys/class/gpio/gpio' + str(self.kernel_id)
			if os.path.exists(iopath): 
				f = open(iopath + '/value','r')
				a=f.read()
				f.close()
				if int(a)==0:
					return False
				else:
					return True
		return False

	def on(self):
		if self.handler_on!=0: 
			self.handler_on()

	def off(self):
		if self.handler_off!=0: 
			self.handler_off()

class Daisy11():

	"""
	DAISY-11 (8 led) related class
	http://foxg20.acmesystems.it/doku.php?id=daisy:daisy11_led	
	"""

	kernel_id=-1

	leds = {
		'L1' :  '2',
		'L2' :  '3',
		'L3' :  '4',
		'L4' :  '5',
		'L5' :  '6',
		'L6' :  '7',
		'L7' :  '8',
		'L8' :  '9',
	}

	def __init__(self,connector_id,led_id):
		pin=self.leds[led_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if get_value(self.kernel_id):
			return True
		else:
			return False


class Daisy23():

	"""
	DAISY-23 (LCD Panel) related class
	2011 - Daniele Sdei, Marco Antonini
	http://wiki.madefree.eu/doku.php/daisy23
	"""

	register_address = {

		'MHD_Rising'      :   0x2B,
		'NHD_Rising'      :   0x2C,
		'NCL_Rising'      :   0x2D,
		'FDL_Rising'      :   0x2E,
		'MHD_Falling'     :   0x2F,
		'NHD_Falling'     :   0x30,
		'NCL_Falling'     :   0x31,
		'FDL_Falling'     :   0x32,
		'ELE0_Touch'      :   0x41, # ELECTRODE_0
		'ELE0_Release'    :   0x42,
		'ELE1_Touch'      :   0x43,  # ELECTRODE_1
		'ELE1_Release'    :   0x44,
		'ELE2_Touch'      :   0x45,  # ELECTRODE_2
		'ELE2_Release'    :   0x46,
		'ELE3_Touch'      :   0x47,  # ELECTRODE_3
		'ELE3_Release'    :   0x48,
		'ELE4_Touch'      :   0x49,  # ELECTRODE_4 & GPIO_0
		'ELE4_Release'    :   0x4A,
		'ELE5_Touch'      :   0x4B,  # ELECTRODE_5 & GPIO_1
		'ELE5_Release'    :   0x4C,
		'ELE6_Touch'      :   0x4D,  # ELECTRODE_6 & GPIO_2
		'ELE6_Release'    :   0x4E,
		'ELE7_Touch'      :   0x4F,  # ELECTRODE_7 & GPIO_3
		'ELE7_Release'    :   0x50,
		'ELE8_Touch'      :   0x51,  # ELECTRODE_8 & GPIO_4
		'ELE8_Release'    :   0x52,
		'ELE9_Touch'      :   0x53,  # ELECTRODE_9 & GPIO_5
		'ELE9_Release'    :   0x54,
		'ELE10_Touch'     :   0x55,  # ELECTRODE_10 & GPIO_6
		'ELE10_Release'   :   0x56,
		'ELE11_Touch'     :   0x57,  # ELECTRODE_11 & GPIO_7
		'ELE11_Release'   :   0x58,
		'FILTER_Config'   :   0x5D,
		'ELE_Config'      :   0x5E,
		'AUTO_Config'     :   0x7B,
		'AUTO_Config_USL' :   0x7D,
		'AUTO_Config_LSL' :   0x7E,
		'AUTO_Config_TL ' :   0x7F,
		'GPIO_Control0'   :   0x73,
		'GPIO_Control1'   :   0x74,
		'GPIO_Data'       :   0x75,
		'GPIO_Direction'  :   0x76,
		'GPIO_Enable'     :   0x77,
		'GPIO_Set'        :   0x78,
		'GPIO_Clear'      :   0x79,
		'GPIO_Toggle'     :   0x7A,
		'PWM0'            :   0x81,
		'PWM1'            :   0x82,
		'PWM2'            :   0x83,
		'PWM3'            :   0x84,

	}

	# bus is the id of i2c bus, addr is address of mpr121
	# connector_id and pin_number identifies where irq is connected
	def __init__(self,bus,addr,connector_id,pin_number):
		self.mpr121_bus = smbus.SMBus(bus)
		self.mpr_i2c_address = addr
		self.mpr_irq_id = get_kernel_id(connector_id,pin_number)
		# 4bit, 2lines, 5x8dots by default
		self.displayfunction = 0x00 | 0x08 | 0x00
		# display on, cursoroff, blinkoff by default
		self.displaycontrol = 0x04 | 0x00 | 0x00
		# entryleft, entryshiftdecrement by default
		self.displaymode = 0x02 | 0x00
					
	def mpr_register(self,name):
		return self.register_address[name]
      
	def mpr_send(self,register,data):
		self.mpr121_bus.write_byte_data(self.mpr_i2c_address,register,data)

	def mpr_read(self,register):
		return self.mpr121_bus.read_byte_data(self.mpr_i2c_address,register)
	
	def mpr_init(self):
		# Control Filtering when data is > baseline
		self.mpr_send(self.mpr_register('MHD_Rising'),0x01)
		self.mpr_send(self.mpr_register('NHD_Rising'),0x01)
		self.mpr_send(self.mpr_register('NCL_Rising'),0x00)
		self.mpr_send(self.mpr_register('FDL_Rising'),0x00)
		# Control Filtering when data is < baseline
		self.mpr_send(self.mpr_register('MHD_Falling'),0x01)
		self.mpr_send(self.mpr_register('NHD_Falling'),0x01)
		self.mpr_send(self.mpr_register('NCL_Falling'),0xFF)
		self.mpr_send(self.mpr_register('FDL_Falling'),0x02)
		# Set Touch & Release Electrode
		self.mpr_send(self.mpr_register('ELE0_Touch'),0x0A)
		self.mpr_send(self.mpr_register('ELE0_Release'),0x0F)
		self.mpr_send(self.mpr_register('ELE1_Touch'),0x0A)
		self.mpr_send(self.mpr_register('ELE1_Release'),0x0F)
		self.mpr_send(self.mpr_register('ELE2_Touch'),0x0A)
		self.mpr_send(self.mpr_register('ELE2_Release'),0x0F)
		self.mpr_send(self.mpr_register('ELE3_Touch'),0x0A)
		self.mpr_send(self.mpr_register('ELE3_Release'),0x0F)
		self.mpr_send(self.mpr_register('ELE4_Touch'),0x0A)
		self.mpr_send(self.mpr_register('ELE4_Release'),0x0F)
		# Set Filter Configuration
		self.mpr_send(self.mpr_register('FILTER_Config'),0x04)
		# Electrode Configuration
		self.mpr_send(self.mpr_register('ELE_Config'),0x05)
		#self.mpr_send(self.mpr_register('ELE_Config'),0xC)
		# Set GPIO
		self.mpr_send(self.mpr_register('GPIO_Enable'),0xFE)
		self.mpr_send(self.mpr_register('GPIO_Direction'),0xFE)
		self.mpr_send(self.mpr_register('GPIO_Control0'),0x00)
		self.mpr_send(self.mpr_register('GPIO_Control1'),0x00)

	# Returns True if electrode status changes, False otherwise.
	def mpr_irq(self):
		if get_value(self.mpr_irq_id):
			return False
		else:
			return True
	
	### Function for GPIO ###

	def gpio_set(self,data):
		self.mpr_send(self.mpr_register('GPIO_Set'),data)

	def gpio_clear(self,data):
		self.mpr_send(self.mpr_register('GPIO_Clear'),data)
	
	def gpio_toggle(self,data):
		self.mpr_send(self.mpr_register('GPIO_Toggle'),data)

	### Functions For Buttons ###

	# This fuction returns the number of buttons pressed and a list of these.
	def button_state(self):
		count = 0
		touch_state = list()
		value = (self.mpr_read(0x01) << 8) | (self.mpr_read(0x00))
		for i in range(0,5):
			if value & (1<<i):
				count = count + 1 # Numbers of electrode is pressed
		if value & (1 << 0):
			touch_state.append(1)
		else:
			touch_state.append(0)
		if value & (1 << 1):
			touch_state.append(1)
		else:
			touch_state.append(0)
		if value & (1 << 2):
			touch_state.append(1)
		else:
			touch_state.append(0)
		if value & (1 << 3):
			touch_state.append(1)
		else:
			touch_state.append(0)
		if value & (1 << 4):
			touch_state.append(1)
		else:
			touch_state.append(0)
		
		return count,touch_state

	# this function returns a string that specifies the button pressed
	def button_read(self):
		count = 0
		value = (self.mpr_read(0x01) << 8) | (self.mpr_read(0x00))
		for i in range(0,5):
			if value & (1<<i):
				count = count + 1 # Numbers of electrode is pressed
		if count == 0 and count > 1:
			return -1
		else:
			
			if value & (1 << 0):
				return 'Right'

			elif value & (1 << 1):
				return 'Down'

			elif value & (1 << 2):
				return 'Center'

			elif value & (1 << 3):
				return 'Left'

			elif value & (1 << 4):
				return 'Up'

	### Functions For LCD ###

	## LCD RS <- GPIO2 ELE6
	## LCD EN <- GPIO3 ELE7
	## LCD D4 <- GPIO4 ELE8
	## LCD D5 <- GPIO5 ELE9
	## LCD D6 <- GPIO6 ELE10
	## LCD D7 <- GPIO7 ELE11


	## REGISTER ADDRESS:
	
	# CLEARDISPLAY 0x01
	# RETURNHOME 0x02
	# ENTRYMODESET 0x04
	# DISPLAYCONTROL 0x08
	# CURSORSHIFT 0x10
	# FUNCTIONSET 0x20
	# SETCGRAMADDR 0x40
	# SETDDRAMADDR 0x80

	# ENTRYRIGHT 0x00
	# ENTRYLEFT 0x02
	# ENTRYSHIFTINCREMENT 0x01
	# ENTRYSHIFTDECREMENT 0x00

	# DISPLAYON 0x04
	# DISPLAYOFF 0x00
	# CURSORON 0x02
	# CURSOROFF 0x00
	# BLINKON 0x01
	# BLINKOFF 0x00

	# DISPLAYMOVE 0x08
	# CURSORMOVE 0x00
	# MOVERIGHT 0x04
	# MOVELEFT 0x00

	# 8BITMODE 0x10
	# 4BITMODE 0x00
	# 2LINE 0x08
	# 1LINE 0x00
	# 5x10DOTS 0x04
	# 5x8DOTS 0x00
				
	def lcd_init(self):
		self.lcd_rsLow()
		self.lcd_enLow()
		self.lcd_write(0x03)
		time.sleep(0.004)
		self.lcd_write(0x03)
		time.sleep(0.004)
		self.lcd_write(0x03)
		time.sleep(0.0001)
		self.lcd_write(0x02)
		time.sleep(0.0001)
		# Set number of lines and font size
		self.lcd_send(0x20 | self.displayfunction, 0)
		# Turn the display on with no cursor or blinking default
		self.lcd_send(0x08 | self.displaycontrol, 0)
		self.lcd_clear()
		# Initialize to default text direction (for romance languages)
		self.lcd_send(0x04 | self.displaymode, 0)

	### high level commands, for the user! ###

	# Turn the LCD backlight on
	def lcd_lightOn(self):
		self.gpio_set(0x02)	# 00000010

	# Turn the LCD backlight off
	def lcd_lightOff(self):
		self.gpio_clear(0x02)	# 00000010

	# Set the LCD backlight intensity (value >=0 and <16)
	def lcd_setLight(self,value):
		self.mpr_send(self.mpr_register('PWM0'), value << 4 )

	def lcd_print(self,s):
		for i in range(0,len(s)):
			self.lcd_send(ord(s[i]), 1)
			i = i + 1	

	# Clear display, set cursor position to zero
	def lcd_clear(self):
		self.lcd_send(0x01, 0)
		time.sleep(0.002)

	# Set cursor position to zero
	def lcd_home(self):
		self.lcd_send(0x02, 0)
		time.sleep(0.002)

	# Set cursor position
	def lcd_setCursor(self,col,row):
		row_offsets = 0x00, 0x40, 0x14, 0x54
		self.lcd_send(0x80 | (col + row_offsets[row]), 0)
	
	# Turn the display on/off (quickly)
	def lcd_display(self):
		self.displaycontrol |= 0x04
		self.lcd_send(0x08 | self.displaycontrol, 0)

	def lcd_noDisplay(self):
		self.displaycontrol &= ~0x04
		self.lcd_send(0x08 | self.displaycontrol, 0)

	# Turns the underline cursor on/off
	def lcd_cursor(self):
		self.displaycontrol |= 0x02
		self.lcd_send(0x08 | self.displaycontrol, 0)

	def lcd_noCursor(self):
		self.displaycontrol &= ~0x02
		self.lcd_send(0x08 | self.displaycontrol, 0)

	# Turn on and off the blinking cursor
	def lcd_blink(self):
		self.displaycontrol |= 0x01
		self.lcd_send(0x08 | self.displaycontrol, 0)

	def lcd_noBlink(self):
		self.displaycontrol &= ~0x01
		self.lcd_send(0x08 | self.displaycontrol, 0)

	# These commands scroll the display without changing the RAM
	def lcd_scrollDisplayLeft(self):
		self.lcd_send(0x10 | 0x08 | 0x00, 0)

	def lcd_scrollDisplayRight(self):
		self.lcd_send(0x10 | 0x08 | 0x04, 0)

	# This is for text that flows Left to Right
	def lcd_leftToRight(self):
		self.displaymode |= 0x02
		self.lcd_send(0x04 | self.displaymode, 0)

	# This is for text that flows Right to Left
	def lcd_rightToLeft(self):
		self.displaymode &= ~0x02
		self.lcd_send(0x04 | self.displaymode, 0)

	# This will 'right justify' text from the cursor
	def lcd_autoscroll(self):
		self.displaymode |= 0x01
		self.lcd_send(0x04 | self.displaymode, 0)

	# This will 'left justify' text from the cursor
	def lcd_noAutoscroll(self):
		self.displaymode &= ~0x01
		self.lcd_send(0x04 | self.displaymode, 0)

	### low level data pushing commands ###

	def lcd_send(self,value,mode):
		if mode == 0:			# 0 for commnd
			self.lcd_rsLow()
		elif mode == 1:			# 1 for data
			self.lcd_rsHigh()
		self.lcd_write(value>>4)
		self.lcd_write(value)

	def lcd_enPulse(self):
		self.lcd_enLow()
		self.lcd_enHigh()
		self.lcd_enLow()
		time.sleep(0.0001)

	def lcd_write(self,data):
		valueLow = 0x00
		valueHigh = 0x00
		if data & 0x01:
			valueHigh |= 0x10	# 00010000
		else:
			valueLow |= 0x10	# 00010000
		if data & 0x02:
			valueHigh |= 0x20	# 00100000
		else:
			valueLow |= 0x20	# 00100000
		if data & 0x04:
			valueHigh |= 0x40	# 01000000
		else:
			valueLow |= 0x40	# 01000000
		if data & 0x08:
			valueHigh |= 0x80	# 10000000
		else:
			valueLow |= 0x80	# 10000000
		
		self.gpio_set(valueHigh)
		self.gpio_clear(valueLow)
		self.lcd_enPulse()

	def lcd_rsHigh(self):
		self.gpio_set(0x04)	# 00000100
	
	def lcd_rsLow(self):
		self.gpio_clear(0x04)	# 00000100 

	def lcd_enHigh(self):
		self.gpio_set(0x08)	# 00001000
	
	def lcd_enLow(self):
		self.gpio_clear(0x08)	# 00001000
