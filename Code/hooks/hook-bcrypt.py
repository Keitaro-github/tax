from PyInstaller.utils.hooks import collect_all

# Collect all files related to bcrypt
datas, binaries, hiddenimports = collect_all('bcrypt')