# AppImage Updater
basic appimage manager, supports github assets AppImages, links to a common name

## Usage
edit appimages.cfg (see appimages.cfg.example) to point to the appimages you want to update

```
name,repo,pattern,update,pinned_version
cemu,cemu-project/Cemu,Cemu-.*-x86_64.AppImage,True,Cemu-2.0-29-x86_64.AppImage
pcsx2,PCSX2/pcsx2,pcsx2-.*-linux.*.AppImage,True,latest
steam-rom-manager,SteamGridDB/steam-rom-manager,Steam-ROM-Manager-.*.AppImage,True,latest
```

you can pin a version to link too incase later versions have issues or use the keywork latest to link to whatever version is downloaded

run with `python3 ./appimage_update.py --path <path to appimages>`