from odoo import models, fields, api
from odoo.exceptions import UserError
import urllib.request


class ResConfigSettings(models.TransientModel):
    """Configuración

    Args:
        models.TransientModel

    Raises:
        1 err: Si el campo del endpoint está vacío.
        2 err: paciente no encontrado
        3 err: otro error HTTP (code).

    Returns:
        dict: Si la conexión al endpoint es exitosa (Mensaje).
    """

    _inherit = 'res.config.settings'

    hospital_ws_endpoint = fields.Char(
        string="Endpoint Webservice de Hospital",
        config_parameter='vertical_hospital.hospital_ws_endpoint'
    )

    def action_test_hospital_endpoint(self):
        endpoint = self.hospital_ws_endpoint
        if not endpoint:
            raise UserError("Debes configurar un endpoint antes de probarlo.")
        try:
            with urllib.request.urlopen(endpoint, timeout=5) as response:
                status = response.getcode()
                if status == 200:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': "Éxito",
                            'message': f"Conectado exitosamente al endpoint.\nCódigo: {status}",
                            'type': 'success',
                            'sticky': False,
                        }
                    }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise UserError(
                    "El paciente no fue encontrado en el endpoint.")
            else:
                raise UserError(f"Error HTTP {e.code}: {e.reason}")
        except Exception as e:
            raise UserError(f"No se pudo conectar con el endpoint:\n{str(e)}")
