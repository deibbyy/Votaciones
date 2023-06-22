# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Candidato(models.Model):
    _inherit = 'res.partner'
    _description = 'Candidatos para las votaciones de la universidad UNIACME'
    
    es_candidato = fields.Boolean(string="Es candidato?", default=False)

    sede_id = fields.Many2one('uniacme_voting.sede', string='Sede')
    votacion_ids = fields.Many2one('uniacme_voting.votacion', string='Votaciones como Candidato', readonly=True)

    @api.constrains('vat')
    def _check_duplicate_identification(self):
        for candidato in self:
            duplicate = self.search([('vat', '=', candidato.vat), ('id', '!=', candidato.id)])
            if duplicate:
                raise ValidationError('Ya existe un candidato con el mismo número de identificación.')

    @api.model
    def create(self, values):
        values['es_candidato'] = True
        values['es_estudiante'] = False
        values['is_company'] = False
        values['company_type'] = 'person'
        return super(Candidato, self).create(values)