import os
import shutil


def copy_static(source_path, destination_path):
	os.mkdir(destination_path)
	for content in os.listdir(source_path):
		from_path = os.path.join(source_path, content)
		to_path = os.path.join(destination_path, content)
		if os.path.isfile(from_path):
			shutil.copy(from_path, to_path)
		elif os.path.isdir(from_path):
			copy_static(from_path, to_path)