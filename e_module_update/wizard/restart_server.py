from odoo import models , fields , exceptions
import zipfile
import io
import shutil
import os
class ModuleUpdateManualWizard(models.TransientModel):
    _name = "e_module_update.restart_server"
    
    commands = fields.Char("Commnads")

    
    def action_restart_server(self):
        pass
        