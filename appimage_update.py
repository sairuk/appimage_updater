#!/usr/bin/env python3

import os,requests,json,re,csv
import argparse

debug = False

def log(s):
    if debug:
        print(s)

def config(conf="appimages.cfg"):
    confdata = {}
    if not os.path.exists(conf):
        try:
            os.copy(f"{conf}.example", conf)
        except:
            return
    with open(conf,'r') as c:
        reader = csv.DictReader(c)
        for row in reader:
            confdata[row['name']] = row
    return confdata

def get(url=None):
    if url is None:
        return
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    return None

def main(args):
    dest = args.path
    conf = config()
    for item in conf.keys():
        appimage = conf[item]
        if appimage['update']:
            data = json.loads(get("https://api.github.com/repos/%s/releases" % appimage['repo']))[0]
            for asset in data['assets']:
                log("Asset: %s" % asset)
                if re.match(appimage['pattern'],asset["name"]):
                    destfile = '%s/%s' % (dest,asset['name'])
                    destlink = '%s/%s.AppImage' % (dest,item)
                    if not os.path.exists(destfile):
                        log("Downloading: %s" % asset["browser_download_url"])
                        response = get(asset["browser_download_url"])
                        with open(destfile,'wb') as f:
                            f.write(response)
                    else:
                        log("File exists: %s" % destfile)


                    # linking
                    if os.path.islink(destlink):
                        os.unlink(destlink)
                    os.chmod(destfile,0o775)
                    if appimage['pinned_version'] == 'latest' or appimage['pinned_version'] == "":
                        os.symlink(destfile,destlink)
                    else:
                        pinned = "%s/%s" % (dest,appimage['pinned_version'])
                        if os.path.exists(pinned):
                            os.symlink(pinned,destlink)
                        else:
                            log("File does not exist: %s" % pinned)
        else:
            log("Skipped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='AppImage Updater',description='Manage AppImages, link to common name')
    parser.add_argument('-p', '--path', type=str, required=True)
    main(parser.parse_args())
