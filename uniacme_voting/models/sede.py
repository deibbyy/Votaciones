# -*- coding: utf-8 -*-
from odoo import models, fields


class Sede(models.Model):
    _name = 'uniacme_voting.sede'
    _description = 'Sedes de la universidad UNIACME'

    name = fields.Char(string='Nombre', required=True)
    direccion = fields.Char(string='Dirección')
    pais = fields.Char(string='País')
