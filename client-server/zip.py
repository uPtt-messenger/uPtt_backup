from zipfile import ZipFile, ZIP_DEFLATED
import sys


def zip_files(output_path, files):
    with ZipFile(output_path, mode='w', compression=ZIP_DEFLATED) as z:
        for x in files:
            print(f'zip add {x}')
            z.write(x)


def unzip(output_path, zip_file):
    with ZipFile(zip_file, mode='r') as z:
        z.extractall(path=output_path)


print(sys.argv)
if len(sys.argv) != 2:
    print('python zip.py target_file')
    sys.exit()

target_file = sys.argv[1]

files = [target_file]
file_name = target_file[:target_file.find('.')]
file_name = f'{file_name}.zip'
print(file_name)

zip_files(file_name, files)
#
# files = ['./uLauncher.exe']
# zip_files('./uLauncher.zip', files)

