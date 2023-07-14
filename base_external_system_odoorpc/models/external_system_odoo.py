# Copyright 2023 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from urllib.error import URLError

import odoorpc

from odoo import _, models
from odoo.exceptions import UserError


class ExternalSystemOdoo(models.Model):
    """This is an Interface implementing the RPC module."""

    _name = "external.system.odoo"
    _inherit = "external.system.adapter"
    _description = "External System RPC"

    previous_dir = None

    def external_test_connection(self):
        """Test connection in the UI"""
        self.ensure_one()
        try:
            odoo = self._connect()
            user_model = odoo.env["res.users"]
            ids = user_model.search([("login", "=", "admin")])
            user_model.read([ids[0]], ["name"])[0]
        except Exception as e:
            raise UserError(_("Connection failed.\n\nDETAIL: %s") % e) from e
        return super().external_test_connection()

    def _connect(self):
        """Return connection object"""
        self.ensure_one()
        if not all([self.host, self.port, self.db_name, self.username, self.password]):
            raise UserError(
                _(
                    "Connection failed. Please make sure that all fields"
                    " are filled: Database, Host, Port, Username, Password."
                )
            )
        try:
            odoo = odoorpc.ODOO(
                self.host,
                port=self.port,
                protocol="jsonrpc+ssl" if self.is_ssl else "jsonrpc",
            )
        except URLError as exc:
            raise UserError(
                _("Could not connect the Odoo server at %(host)s:%(port)s")
                % {"host": self.host, "port": self.port}
            ) from exc
        odoo.login(self.db_name, self.username, self.password)
        return odoo
