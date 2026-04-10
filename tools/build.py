#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import zipfile
import re
import configparser

# GLOBALS
scriptPath  = os.path.realpath(__file__)
projectRoot = os.path.dirname(os.path.dirname(scriptPath))

config = configparser.ConfigParser()
config.read_string("[build]\n" + open(os.path.join(os.path.dirname(scriptPath), "config.conf")).read())
cfg = config["build"]

projectName       = cfg["projectName"]
remoteFileid      = cfg["remoteFileid"]
excludeList       = [x.strip() for x in cfg["excludeList"].split(",")]
includeList       = [x.strip() for x in cfg["includeList"].split(",")]
supportedVersion  = cfg.get("supported_version")

versionName = sys.argv[1] if len(sys.argv) > 1 else "DevBuild"


def read_tags(sourceDescriptor):
    text = open(sourceDescriptor, "r").read()
    m = re.search(r"tags=\{[^}]*\}", text, re.MULTILINE | re.DOTALL)
    return m.group(0) if m else "tags={}"

def write_descriptor(path, variant):
    sv = supportedVersion or "*.*.*"
    tags = read_tags(os.path.join(projectRoot, "descriptor.mod"))

    pathline = f"path=\"mod/{projectName}\""
    remoteline = f"remote_file_id=\"{remoteFileid}\"" if variant == "steam" else ""

    content = (
        f"name=\"{projectName}\"\n"
        f"version=\"{versionName}\"\n"
        f"{tags}\n"
        f"supported_version=\"{sv}\"\n"
        + (f"{remoteline}\n" if remoteline else "")
        + f"{pathline}\n"
    )
    with open(path, "w") as f:
        f.write(content)

def mkDir(path):
    try:
        os.mkdir(path)
    except:
        pass

def remove(path):
    if os.path.isdir(path):
        try:
            shutil.rmtree(path, ignore_errors=False, onerror=None)
            print("Cleaned up old release...")
        except:
            pass
    if os.path.isfile(path):
        try:
            os.remove(path)
            print("Removed previous archive...")
        except:
            pass


def copy_files(destPath):
    dir_excludes = [x for x in excludeList if not x.startswith('.')]
    ext_excludes = [x for x in excludeList if x.startswith('.')]
    files = glob.glob('**', recursive=True)
    for f in files:
        parts = f.replace('\\', '/').split('/')
        if any(x in parts for x in dir_excludes):
            continue
        if any(x in f for x in ext_excludes):
            if not any(x in f for x in includeList):
                continue
        y = os.path.join(destPath, f)
        if os.path.isdir(f):
            print("Creating path:", y)
            mkDir(y)
        else:
            print("Copying:", f, "==>", os.path.join("release", os.path.basename(destPath), f))
            shutil.copy(f, y)


def build_variant(releasePath, variant):
    variantPath = os.path.join(releasePath, variant)
    suffix = "_steam" if variant == "steam" else "_local"
    archiveFileName = "{}_v{}{}.zip".format(projectName.replace(" ", ""), versionName, suffix)
    releaseProjectPath = os.path.join(variantPath, projectName)
    archivePath = os.path.join(variantPath, archiveFileName)

    mkDir(variantPath)
    remove(archivePath)
    remove(releaseProjectPath)
    mkDir(releaseProjectPath)

    copy_files(releaseProjectPath)

    write_descriptor(os.path.join(releaseProjectPath, "descriptor.mod"), variant)

    os.chdir(variantPath)
    print("Making archive ({})...".format(archiveFileName))
    with zipfile.ZipFile(archiveFileName, 'w') as releaseArchive:
        for f in glob.glob(os.path.join(projectName, "**"), recursive=True):
            releaseArchive.write(f)

    os.chdir(projectRoot)


def main():
    os.chdir(projectRoot)
    releasePath = os.path.join(projectRoot, "release")
    mkDir(releasePath)

    print("=== Building local release ===")
    build_variant(releasePath, "local")

    print("=== Building steam release ===")
    build_variant(releasePath, "steam")

if __name__ == "__main__":
    sys.exit(main())
