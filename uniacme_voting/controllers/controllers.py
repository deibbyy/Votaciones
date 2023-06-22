# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class EstudianteController(http.Controller):
    
    @http.route('/votacion/estudiante', type='http', auth='user', website=True, csrf=False)
    def participar_votacion(self, **kwargs):
        return request.render('uniacme_voting.ingresar_documento_template')

    @http.route('/votacion/estudiante/validar_documento', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def validar_documento(self, **kwargs):
        documento = kwargs.get('documento')
        estudiante = request.env['res.partner'].search([('vat', '=', documento), ('es_estudiante', '=', True)])
        
        print("estudiante", estudiante, documento)

        if estudiante:
            votaciones = request.env['uniacme_voting.votacion'].search([])
            return request.render('uniacme_voting.participar_votacion_template', {'estudiante': estudiante.id, 'votaciones': votaciones})
        else:
            return request.render('uniacme_voting.documento_invalido_template')
        
    @http.route('/votacion/estudiante/votar', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def votar(self, **kwargs):
        votacion_id = kwargs.get('votacion_id')
        estudiante_id = kwargs.get('estudiante')
        votacion = request.env['uniacme_voting.votacion'].search([('id', '=', votacion_id)])
        estudiante = request.env['res.partner'].search([('id', '=', estudiante_id)])


        print("votacion", votacion.id, estudiante)
        
        if votacion_id:
            return request.render('uniacme_voting.votar_template', {'votacion': votacion.id, 'estudiante': estudiante, 'candidatos':votacion.candidatos})
        else:
            return request.render('uniacme_voting.votacion_invalida_template')
    
    @http.route('/votacion/estudiante/submit', type='http', auth='user', csrf=False, methods=['POST'], website=True)
    def submit_votacion(self, **kwargs):
        votacion_id = kwargs.get('votacion')
        candidato_id = kwargs.get('candidato_id')
        estudiante  = kwargs.get('estudiante')
        
        # Obtener el candidato seleccionado
        candidato = request.env['res.partner'].browse(int(candidato_id))

        # Crear o actualizar el registro de voto
        voto = request.env['uniacme_voting.voto'].search([('candidato_id', '=', candidato.id)])
        
        if not voto:
            voto = request.env['uniacme_voting.voto'].create({
                'candidato_id': candidato.id,
                'votacion_id': votacion_id,
            })

        # Incrementar la cantidad de votos
        voto.cantidad_votos += 1

        # Imprimir información de votación
        print("Votación:", votacion_id)
        print("Candidato:", candidato.name)
        print("Cantidad de votos:", voto.cantidad_votos)
        

        return request.render('uniacme_voting.votacion_exitosa_template')

