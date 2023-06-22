# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Votacion(models.Model):
    _name = 'uniacme_voting.votacion'
    _description = 'Procesos de votación en la universidad UNIACME'

    name = fields.Char(string='Descripción', required=True)
    fecha_inicio = fields.Datetime(string='Fecha de inicio', required=True)
    fecha_fin = fields.Datetime(string='Fecha de fin', required=True)
    candidatos = fields.Many2many('res.partner', string='Candidatos', required=True, domain=[('es_candidato', '=', True)])
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En proceso'),
        ('cerrada', 'Cerrada')],
        default='borrador', string='Estado')
    votos_por_candidato = fields.One2many('uniacme_voting.voto', 'votacion_id', string='Votos por Candidato')

    @api.model
    def create(self, values):
        aux = values.get('candidatos', [])
        candidatos = self.env['res.partner'].search([('id', 'in', aux[0][2])])

        votacion = super(Votacion, self).create(values)
        votacion.candidatos = candidatos
        for candidato in candidatos:
            if candidato.votacion_ids:
                raise ValidationError("El candidato {} ya está asignado a una votación.".format(candidato.name))
            else:
                candidato.votacion_ids = votacion
        return votacion

    def iniciar_votaciones(self):
        self.write({'estado': 'en_proceso'})

class Voto(models.Model):
    _name = 'uniacme_voting.voto'
    _description = 'Votos por Candidato'

    candidato_id = fields.Many2one('res.partner', string='Candidato', required=True, domain=[('es_candidato', '=', True)])
    votacion_id = fields.Many2one('uniacme_voting.votacion', string='Votación', required=True)
    cantidad_votos = fields.Integer(string='Cantidad de Votos', default=0)
    # foto_candidato = fields.Binary(string='Foto del Candidato', related='candidato_id.image_1920')

    