from netmiko import ConnectHandler
import getpass

'''
By Charles Zuo
04/25/2018

This script applies a standard config in the config.txt file to every device in the devices.txt file.

'''

devices_completed = [] #Devices that had successful configurations applied to them are saved here
devices_error = [] #Devices that failed to have configuration applied to them are saved here

#asks user for Cisco Platform. Do not try to apply the same config to devices across platforms, e.g applying same config to nxos and catalyst devices
def get_device_platform():
	print('What is the device type? \n 1.  cisco_ios  \n 2.  cisco_nxos \n 3.  cisco_xe \n 4.  cisco_asa \n 5.  cisco_xr' )

	get_device_type = input('Select the type ')

	#print (get_device_type)

	if str(get_device_type)=='1':
		device_type = 'cisco_ios'
	elif str(get_device_type) == '2':
		device_type = 'cisco_nxos'
	elif str(get_device_type) == '3':
		device_type = 'cisco_xe'
	elif str(get_device_type) == '4':
		device_type = 'cisco_asa'
	elif str(get_device_type) == '5':	
		device_type = 'cisco_xr'
	else:
		print ('please select the correct device type')
		get_device_platform

	return device_type


def apply_config(current_device):


	try:
		net_connect = ConnectHandler(device_type=device_platform, ip=current_device, username=un, password=password) 
		net_connect.find_prompt()
		print current_device
		net_connect.send_config_from_file('config.txt')
		devices_completed.append(current_device)
	except:
		print 'Could not connect to ' + current_device
		devices_error.append(current_device)




#Gets username and password
un = raw_input('Enter username: ') 
password = getpass.getpass('Enter Password: ')


#appends all the hosts in the devices.txt file to a list.
with open('devices.txt', 'r') as f:
    devices = f.readlines()
#strips the \n
devices = map(lambda s: s.strip(), devices)


device_platform = get_device_platform()

for i in range (0, len(devices)):
	apply_config(devices[i])
	#print(devices[i])


print 'The config was successfully applied to: '
for i in devices_completed:
	print i

print 'The config was not applied to: '
for i in devices_error:
	print i


