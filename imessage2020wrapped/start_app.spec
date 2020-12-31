# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['start_app.py'],
             pathex=['/Users/mdanello/Code/.virtualenv/imessage/lib/python3.8/site-packages', '/Users/mdanello/Code/Projects/imessage2020wrapped/imessage2020wrapped'],
             binaries=[],
             datas=[('imessage2020wrapped/templates', 'imessage2020wrapped/templates'), ('imessage2020wrapped/static', 'imessage2020wrapped/static'), ('/Users/mdanello/Code/.virtualenv/imessage/lib/python3.8/site-packages/zipcodes/zips.json.bz2', 'zipcodes/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='start_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='start_app.app',
             icon=None,
             bundle_identifier=None)
