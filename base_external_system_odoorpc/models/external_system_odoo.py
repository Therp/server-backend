# Copyright 2023 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import os

from odoo import models


class ExternalSystemOdoo(models.Model):
    """This is an Interface implementing the RPC module."""

    _name = "external.system.odoo"
    _inherit = "external.system.adapter"
    _description = "External System RPC"

    previous_dir = None

    def external_get_client(self):
        """Return a usable client representing the remote system."""
        super(ExternalSystemOdoo, self).external_get_client()
        if self.system_id.remote_path:
            ExternalSystemOdoo.previous_dir = os.getcwd()
            os.chdir(self.system_id.remote_path)
        return os

    def external_destroy_client(self, client):
        """Perform any logic necessary to destroy the client connection.

        Args:
            client (mixed): The client that was returned by
             ``external_get_client``.
        """
        result = super(ExternalSystemOdoo, self).external_destroy_client(client)
        if ExternalSystemOdoo.previous_dir:
            os.chdir(ExternalSystemOdoo.previous_dir)
            ExternalSystemOdoo.previous_dir = None
        return result
