import hid
import time

# !!!DUMB VERSION FOR OLDER HIDAPI VERSIONS ONLY!!!

needle = {
	'vendor_id': 0x258A,
	'product_id': 0x0029
}

cmd_feature_report = [0x05, 0x11, 0x00, 0x00, 0x00, 0x00]
data_feature_report = [0x04] + 519*[0x00]

def deviceFilter(device):
	global needle

	for key in needle:
		if device[key] != needle[key]:
			return False

	return True

def findCommandDevice(devices, command):
	for id, device in devices:
		dev_temp = hid.device()
		dev_temp.open_path(device['path'])

		if dev_temp.send_feature_report(command) >= 0:
			print('Found cmd device: #{}, path: {}'.format(id, device['path']))
			return dev_temp
		else:
			print('Couldn\'t send report 5 to device: #{}, path: {}'.format(id, device['path']))
			dev_temp.close()

	return None

def findDataDevice(devices, report_id, report_len):
	for id, device in devices:
		dev_temp = hid.device()
		dev_temp.open_path(device['path'])

		try:
			data_temp = dev_temp.get_feature_report(report_id, report_len)
			print('Found data device: #{}, path: {}'.format(id, device['path']))
			return dev_temp, data_temp

		except IOError as e:
			print('Couldn\'t request report 4 from device: #{}, path: {}, error: {}'.format(id, device['path'], e))
			dev_temp.close()

	return None

def printProfile(id, data):
	print('Profile {} data: [{}]\n'.format(id, ', '.join(hex(x) for x in data)))

profile_data = []

devices = list(enumerate(filter(deviceFilter, hid.enumerate())))
dev_cmd = findCommandDevice(devices, cmd_feature_report)
# dev_data, profile_data_temp = findDataDevice(devices, 4, 520)
# profile_data.append(profile_data_temp)

print('Cmd device: {}\n'.format(dev_cmd)) # ', Data device: {}' , dev_data

if (dev_cmd is not None): #  and (dev_data is not None)
	print('Requesting profile 1 data')
	cmd_feature_report[1] = 0x11
	dev_cmd.send_feature_report(cmd_feature_report)
	profile_data.append(dev_cmd.get_feature_report(4, 520))
	printProfile(1, profile_data[0])

	time.sleep(0.5)

	print('Requesting profile 2 data')
	cmd_feature_report[1] = 0x21
	dev_cmd.send_feature_report(cmd_feature_report)
	profile_data.append(dev_cmd.get_feature_report(4, 520))
	printProfile(2, profile_data[1])

	time.sleep(0.5)

	print('Requesting profile 3 data')
	cmd_feature_report[1] = 0x31
	dev_cmd.send_feature_report(cmd_feature_report)
	profile_data.append(dev_cmd.get_feature_report(4, 520))
	printProfile(3, profile_data[2])

	print('WARNING! This action is going to OVERRIDE profile data on your mouse.')
	print('By proceeding you accept all possible risks related to this.')
	print('Author is not responsible for any potential damage to your hardware')
	consent = input('Replace profile 2 and 3 data with a copy of profile 1? Y/n:')

	if consent == 'Y':
		print('')
		usb_buf = 520*[0x00]
		for i, byte in enumerate(profile_data[0]):
			usb_buf[i] = byte
		
		usb_buf[3] = 123
		usb_buf[6] = 0x00

		usb_buf[1] = 0x21
		print('Writing profile 2')
		printProfile('W2', usb_buf)
		dev_cmd.send_feature_report(usb_buf)

		time.sleep(0.5)

		usb_buf[1] = 0x31
		print('Writing profile 3')
		printProfile('W3', usb_buf)
		dev_cmd.send_feature_report(usb_buf)

		time.sleep(0.5)

		print('Reading back new profile 2 data')
		cmd_feature_report[1] = 0x21
		dev_cmd.send_feature_report(cmd_feature_report)
		printProfile(2, dev_cmd.get_feature_report(4, 520))

		time.sleep(0.5)

		print('Reading back new profile 3 data')
		cmd_feature_report[1] = 0x31
		dev_cmd.send_feature_report(cmd_feature_report)
		printProfile(3, dev_cmd.get_feature_report(4, 520))

	print('Done.')

	# dev_data.close()
	dev_cmd.close()