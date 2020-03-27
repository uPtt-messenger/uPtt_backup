from zipfile import ZipFile, ZIP_DEFLATED


def zip_files(output_path, files):
    with ZipFile(output_path, mode='w', compression=ZIP_DEFLATED) as z:
        for x in files:
            print(f'zip add {x}')
            z.write(x)


def unzip(output_path, zip_file):
    with ZipFile(zip_file, mode='r') as z:
        z.extractall(path=output_path)


files = ['./uPtt.exe']
zip_files('./uPtt.zip', files)

files = ['./uLauncher.exe']
zip_files('./uLauncher.zip', files)
# unzip('./output/', './uPtt.zip')
