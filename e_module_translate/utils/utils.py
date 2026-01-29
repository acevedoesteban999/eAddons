# -*- coding: utf-8 -*-
import io
import os
import polib
from odoo.tools.translate import trans_export



def get_pot_from_export(module_name,cr):
    with io.BytesIO() as buf:
        trans_export(False, [module_name], buf, 'po', cr)
        buf.seek(0)
        content = buf.read().decode('utf-8')
        return polib.pofile(content)

def get_pot_from_file(local_path,module_name):
    pot_path = os.path.join(local_path, 'i18n', f'{module_name}.pot')
    if not os.path.isfile(pot_path):
        return None
    return polib.pofile(pot_path)

def compare_pot_files(local_path,module_name,cr):
    file_pot = get_pot_from_export(module_name,cr)
    if not file_pot:
        return False

    exported_pot = get_pot_from_file(local_path, module_name)
    
    exported_keys = {entry.msgid for entry in exported_pot if entry.msgid}
    file_keys = {entry.msgid for entry in file_pot if entry.msgid}

    missing_in_file = exported_keys - file_keys
    extra_in_file = file_keys - exported_keys
    common_keys = exported_keys & file_keys

    return common_keys, missing_in_file, extra_in_file
    