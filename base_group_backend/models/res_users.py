import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    # TODO: (franz) make it clear why we test with "." group and why the share = True
    @api.model
    def has_group(self, group_ext_id):
        """While ensuring a user is part of `base.group_user` this code will
        try if user is in the `base_group_backend.group_backend` group to let access
        to the odoo backend.

        This code avoid to overwrite a lot of places in controllers from
        different modules ('portal', 'web', 'base') with hardcoded statement
        that check if user is part of `base.group_user` group.

        As far `base.group_user` have a lot of default permission this
        makes hard to maintain proper access right according your business.
        """
        res = super().has_group(group_ext_id)
        if not res and (group_ext_id == "base.group_user"):
            has_base_group_backend = super().has_group(
                "base_group_backend.group_backend"
            )
            if has_base_group_backend:
                _logger.warning("Forcing has_group to return True for group_backend")
            return has_base_group_backend
        return res

    @api.depends("groups_id")
    def _compute_share(self):
        user_group_id = self.env["ir.model.data"]._xmlid_to_res_id("base.group_user")
        backend_user_group_id = self.env["ir.model.data"]._xmlid_to_res_id(
            "base_group_backend.group_backend"
        )
        internal_users = self.filtered_domain(
            [("groups_id", "in", [user_group_id, backend_user_group_id])]
        )
        internal_users.share = False
        (self - internal_users).share = True
