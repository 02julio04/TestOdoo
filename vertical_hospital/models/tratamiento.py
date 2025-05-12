from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalTratamiento(models.Model):
    """Modelo Tratamiento
    Permite registrar el código único del tratamiento, su nombre y el médico responsable.

    Args:
         models.Model

    Raises:
        ValidationError: Si el código contiene la secuencia prohibida '026'.

    Returns:
        list: codigo - nombre
    """
    _name = 'hospital.tratamiento'
    _description = 'Tratamiento'

    codigo = fields.Char(string='Código del Tratamiento', required=True)
    name = fields.Char(string='Nombre del Tratamiento', required=True)
    medico = fields.Char(string='Médico Tratante', required=True)

    _sql_constraints = [
        ('unique_codigo', 'unique(codigo)',
         'El código del tratamiento debe ser único.')
    ]

    @api.constrains('codigo')
    def _check_codigo_no_contiene_026(self):
        for record in self:
            if '026' in (record.codigo or ''):
                raise ValidationError(
                    "El código del tratamiento no puede contener la secuencia '026'.")

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.codigo or ''} - {rec.name or ''}"
            result.append((rec.id, name))
        return result
