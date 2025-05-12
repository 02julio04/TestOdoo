from odoo import http
from odoo.http import request
import json


class PacienteAPI(http.Controller):
    """Controlador REST público para consultar pacientes por secuencia.

    Args:
        http.Controller: Clase base de Odoo para definir rutas HTTP públicas o privadas.

    Returns:
        dict: Un diccionario con los datos del paciente (seq, name, rnc, state) o un error.
    """

    @http.route('/paciente/consulta/<string:secuencia>', auth='public', type='http', methods=['GET'], csrf=False)
    def consultar_paciente(self, secuencia):
        paciente = request.env['hospital.paciente'].sudo().search(
            [('secuencia', '=', secuencia)], limit=1)
        if not paciente:
            return request.make_response(
                json.dumps({'error': 'Paciente no encontrado'}),
                headers=[('Content-Type', 'application/json')],
                status=404
            )

        result = {
            'seq': paciente.secuencia,
            'name': paciente.name,
            'rnc': paciente.rnc,
            'state': paciente.state
        }

        return request.make_response(
            json.dumps(result),
            headers=[('Content-Type', 'application/json')]
        )
