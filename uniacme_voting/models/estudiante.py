# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Estudiante(models.Model):
    _inherit = 'res.partner'
    _description = 'Estudiantes de la universidad UNIACME'
    

    carrera = fields.Char(string='Carrera', required=True)
    es_estudiante = fields.Boolean(string="Es estudiante?", default=False)
    sede_id = fields.Many2one('uniacme_voting.sede', string='Sede')
    votacion_id = fields.Many2one('uniacme_voting.votacion', string='Votación')


    @api.constrains('vat')
    def _check_duplicate_identification(self):
        for estudiante in self:
            duplicate = self.search([('vat', '=', estudiante.vat), ('id', '!=', estudiante.id)])
            if duplicate:
                raise ValidationError('Ya existe un estudiante con el mismo número de identificación.')
    
    @api.model
    def create(self, values):
        values['es_estudiante'] = True
        values['is_company'] = False
        values['company_type'] = 'person'
        return super(Estudiante, self).create(values)

