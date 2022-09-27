import zipfile

path = '1dwf0s8.zip'

z = zipfile.ZipFile(path, 'r')

namelist = z.namelist()
for config in namelist:
    print(config)
    print(z.read(config))
