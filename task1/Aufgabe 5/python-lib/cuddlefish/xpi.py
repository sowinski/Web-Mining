# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import zipfile
import simplejson as json
from cuddlefish.util import filter_filenames, filter_dirnames

class HarnessOptionAlreadyDefinedError(Exception):
    """You cannot use --harness-option on keys that already exist in
    harness-options.json"""

ZIPSEP = "/" # always use "/" in zipfiles

def make_zipfile_path(localroot, localpath):
    return ZIPSEP.join(localpath[len(localroot)+1:].split(os.sep))

def mkzipdir(zf, path):
    dirinfo = zipfile.ZipInfo(path)
    dirinfo.external_attr = int("040755", 8) << 16L
    zf.writestr(dirinfo, "")

def build_xpi(template_root_dir, manifest, xpi_path,
              harness_options, limit_to=None, extra_harness_options={}):
    zf = zipfile.ZipFile(xpi_path, "w", zipfile.ZIP_DEFLATED)

    open('.install.rdf', 'w').write(str(manifest))
    zf.write('.install.rdf', 'install.rdf')
    os.remove('.install.rdf')

    if 'icon' in harness_options:
        zf.write(str(harness_options['icon']), 'icon.png')
        del harness_options['icon']

    if 'icon64' in harness_options:
        zf.write(str(harness_options['icon64']), 'icon64.png')
        del harness_options['icon64']

    if 'preferences' in harness_options:
        from options_xul import parse_options, validate_prefs

        validate_prefs(harness_options["preferences"])

        open('.options.xul', 'w').write(parse_options(harness_options["preferences"], harness_options["jetpackID"]))
        zf.write('.options.xul', 'options.xul')
        os.remove('.options.xul')

        from options_defaults import parse_options_defaults
        open('.prefs.js', 'w').write(parse_options_defaults(harness_options["preferences"], harness_options["jetpackID"]))

    else:
        open('.prefs.js', 'w').write("")

    zf.write('.prefs.js', 'defaults/preferences/prefs.js')
    os.remove('.prefs.js')


    IGNORED_FILES = [".hgignore", ".DS_Store", "install.rdf",
                     "application.ini", xpi_path]

    files_to_copy = {} # maps zipfile path to local-disk abspath
    dirs_to_create = set() # zipfile paths, no trailing slash

    for dirpath, dirnames, filenames in os.walk(template_root_dir):
        filenames = list(filter_filenames(filenames, IGNORED_FILES))
        dirnames[:] = filter_dirnames(dirnames)
        for dirname in dirnames:
            arcpath = make_zipfile_path(template_root_dir,
                                        os.path.join(dirpath, dirname))
            dirs_to_create.add(arcpath)
        for filename in filenames:
            abspath = os.path.join(dirpath, filename)
            arcpath = make_zipfile_path(template_root_dir, abspath)
            files_to_copy[arcpath] = abspath

    # `packages` attribute contains a dictionnary of dictionnary
    # of all packages sections directories
    for packageName in harness_options['packages']:
      base_arcpath = ZIPSEP.join(['resources', packageName])
      # Always write the top directory, even if it contains no files, since
      # the harness will try to access it.
      dirs_to_create.add(base_arcpath)
      for sectionName in harness_options['packages'][packageName]:
        abs_dirname = harness_options['packages'][packageName][sectionName]
        base_arcpath = ZIPSEP.join(['resources', packageName, sectionName])
        # Always write the top directory, even if it contains no files, since
        # the harness will try to access it.
        dirs_to_create.add(base_arcpath)
        # cp -r stuff from abs_dirname/ into ZIP/resources/RESOURCEBASE/
        for dirpath, dirnames, filenames in os.walk(abs_dirname):
            goodfiles = list(filter_filenames(filenames, IGNORED_FILES))
            dirnames[:] = filter_dirnames(dirnames)
            for filename in goodfiles:
                abspath = os.path.join(dirpath, filename)
                if limit_to is not None and abspath not in limit_to:
                    continue  # strip unused files
                arcpath = ZIPSEP.join(
                    ['resources',
                     packageName,
                     sectionName,
                     make_zipfile_path(abs_dirname,
                                       os.path.join(dirpath, filename)),
                     ])
                files_to_copy[str(arcpath)] = str(abspath)
    del harness_options['packages']

    locales_json_data = {"locales": []}
    mkzipdir(zf, "locale/")
    for language in sorted(harness_options['locale']):
        locales_json_data["locales"].append(language)
        locale = harness_options['locale'][language]
        # Be carefull about strings, we need to always ensure working with UTF-8
        jsonStr = json.dumps(locale, indent=1, sort_keys=True, ensure_ascii=False)
        info = zipfile.ZipInfo('locale/' + language + '.json')
        info.external_attr = 0444 << 16L
        zf.writestr(info, jsonStr.encode( "utf-8" ))
    del harness_options['locale']

    jsonStr = json.dumps(locales_json_data, ensure_ascii=True) +"\n"
    info = zipfile.ZipInfo('locales.json')
    info.external_attr = 0444 << 16L
    zf.writestr(info, jsonStr.encode("utf-8"))

    # now figure out which directories we need: all retained files parents
    for arcpath in files_to_copy:
        bits = arcpath.split("/")
        for i in range(1,len(bits)):
            parentpath = ZIPSEP.join(bits[0:i])
            dirs_to_create.add(parentpath)

    # create zipfile in alphabetical order, with each directory before its
    # files
    for name in sorted(dirs_to_create.union(set(files_to_copy))):
        if name in dirs_to_create:
            mkzipdir(zf, name+"/")
        if name in files_to_copy:
            zf.write(files_to_copy[name], name)

    harness_options = harness_options.copy()
    for key,value in extra_harness_options.items():
        if key in harness_options:
            msg = "Can't use --harness-option for existing key '%s'" % key
            raise HarnessOptionAlreadyDefinedError(msg)
        harness_options[key] = value
    open('.options.json', 'w').write(json.dumps(harness_options, indent=1,
                                                sort_keys=True))
    zf.write('.options.json', 'harness-options.json')
    os.remove('.options.json')

    zf.close()
