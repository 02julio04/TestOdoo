from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Paciente(models.Model):
    """ Modelo para gestionar paciente

    Args:
        models (_type_): _description_
    """
    _name = "hospital.paciente"
    _description = "Paciente"
    _inherit = ["mail.thread"]  # activa chatter seguimiento de cambios

    secuencia = fields.Char(string='sequence', required=True,
                            copy=False, readonly=True, default='Nuevo')
    name = fields.Char(string="Name", required=True)
    rnc = fields.Char(string="RNC", required=True, tracking=True)
    tratamiento_id = fields.Many2one(
        'hospital.tratamiento',
        string='Treatment',
        tracking=True
    )
    tratamiento_info = fields.Char(
        string='treatment (Code - Name)',
        compute='_compute_tratamiento_info'
    )

    @api.depends('tratamiento_id')
    def _compute_tratamiento_info(self):
        for rec in self:
            if rec.tratamiento_id:
                rec.tratamiento_info = f"{rec.tratamiento_id.codigo} - {rec.tratamiento_id.name}"
            else:
                rec.tratamiento_info = ''

    fecha_alta = fields.Datetime(
        string='Fecha de Alta', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(
        string='Última Actualización', compute='_compute_fecha_actualizacion', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('alta', 'Alta'),
        ('baja', 'Baja')
    ], string='State', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        """Creacion de la secuencia en caso de que sea nuevo
        Args:
            vals (diccionario): contiene los valores que se están guardando.
        """
        if vals.get('secuencia', 'Nuevo') == 'Nuevo':
            vals['secuencia'] = self.env['ir.sequence'].next_by_code(
                'hospital.paciente') or 'Nuevo'
        return super().create(vals)

    @api.depends('write_date')
    def _compute_fecha_actualizacion(self):
        """Calcula automáticamente la fecha de últ update del paciente, cada vez que se edita algo.
        """
        for rec in self:
            rec.fecha_actualizacion = rec.write_date

    @api.constrains('rnc')
    def _check_rnc(self):
        """funcion de revisar que solo contenga numeros 

        Raises:
            ValidationError: Lanza un error en caso de que contenga letras 
        """
        for record in self:
            if not record.rnc.isdigit():
                raise ValidationError("El RNC debe contener solo números.")
