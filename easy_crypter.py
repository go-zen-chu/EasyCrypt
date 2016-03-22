# coding:utf-8
from __future__ import print_function # using Python3 print for lambda, forward compatibility
from easy_crypt import EasyCrypt as ec

def check_paths(parsed_args):
	exists_args = []
	if args.e != None: exists_args.append(args.e)
	if args.d != None: exists_args.append(args.d)
	if args.et != None: exists_args.append(args.et)
	if args.dt != None: exists_args.append(args.dt)
	if args.ed != None: exists_args.append(args.ed)
	if args.dd != None: exists_args.append(args.dd)
	for arg in exists_args:
		ec.path_exists_or_exit(arg)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a python encrypter using AES-256-CBC algorithm of openssl.')
	parser.add_argument('-g', action='store_true', help='Generate random password.')
	parser.add_argument('-e', type=str, help='Encrypt specified file to .enc file. This function does not record your password. Do not forget it.')
	parser.add_argument('-d', type=str, help='Decrypt .enc file with password')
	parser.add_argument('-et', type=str, help='Encrypt specified text file (.txt, .csv ...) to .enc file and record your password inside the text file.')
	parser.add_argument('-dt', type=str, help='Decrypt .enc file to text file.')
	parser.add_argument('-ed', type=str, help='Encrypt directory by zipping and encrypt to .zip.enc file.')
	parser.add_argument('-dd', type=str, help='Decrypt .zip.enc file to a directory.')
	args = parser.parse_args()
	# if using debug mode in python
	if sys.flags.debug: print(args)
	check_paths(args)

	result = False
	if args.g:
		print(ec.gen_rnd_pswd())
		result = True
	# Just en/decrypting files with any extensions
	elif args.e != None:
		raw_file_path = args.e
		master_pswd = confirm_pswd_print() # create master password
		if master_pswd == None: return
		result = ec.encrypt_file(raw_file_path, master_pswd)
	elif args.d != None:
		encrypted_file_path = args.d
		result = ec.decrypt_file(encrypted_file_path, failed_act=lambda: print('Decryption failed. Try again.'))
	# En/decrypt txt base file.
	elif args.et != None:
		raw_text_path = args.et
		master_pswd = ec.read_master_pswd(raw_text_path)
		if master_pswd == None: master_pswd = ec.confirm_pswd_print()
		result = ec.encrypt_file(raw_text_path, master_pswd)
	elif args.dt != None:
		encrypted_text_path = args.dt
		result = ec.decrypt_txt_file(encrypted_text_path)
	# En/decrypt dir using zip
	elif args.ed != None:
		raw_dir_path = args.ed
		result = ec.encrypt_dir(raw_dir_path)
	elif args.dd != None:
		encrypted_dir_path = args.dt
		result = ec.decrypt_dir(encrypted_dir_path)
	else:
		print('No valid arguments! Input -h or --help flag for help.')
		result = True

	if result == False:
		print('Failed to run script. Add -d flag to python command for running program in verbose mode.')
