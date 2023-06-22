import csv
import io
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64

class VotacionImportWizard(models.TransientModel):
    _name = 'votacion.import.wizard'
    _description = 'Votacion Import Wizard'

    import_file = fields.Binary(string='Import File', required=True)

    def process_import(self):
        file_data = io.BytesIO(base64.b64decode(self.import_file))
        
        decoded_file = io.TextIOWrapper(file_data, encoding='latin-1')
        csv_reader = csv.DictReader(decoded_file)
        print("Aqui llego el archivo", file_data)
        for row in csv_reader:
            try:
                
                votacion_data = {
                    'name': row.get('Descripcion'),
                    'fecha_inicio': row.get('Fecha de inicio'),
                    'fecha_fin': row.get('Fecha de fin'),
                }
                
                votacion = self.env['uniacme_voting.votacion'].create(votacion_data)
                
                candidate_ids = []
                for candidate_name in row.get('Candidatos', '').split(','):
                    candidate = self.env['res.partner'].search([('name', '=', candidate_name.strip()), ('es_candidato', '=', True)], limit=1)
                    if candidate:
                        candidate_ids.append(candidate.id)
                if candidate_ids:
                    votacion.candidatos = candidate_ids
                
                votacion.estado = 'borrador'
            except Exception as e:
                raise UserError(_("An error occurred while importing voting data. Error: %s") % str(e))
        
        return {'type': 'ir.actions.act_window_close'}
