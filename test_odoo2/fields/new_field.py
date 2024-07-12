from odoo import fields
import logging


class NewField(fields.Float):

    def convert_to_column(self, value, record, values=None, validate=True):
        return super().convert_to_column(value, record, values, validate)

    def __get__(self, record, owner):
        logging.info(record)
        logging.info(owner)
        result = super().__get__(record, owner)

        logging.info(result)
        return result

    # def _get_attrs(self, model, name):
    #     value = 42
    #     modules = set()
    #     attrs = {}
    #     if not (self.args.get("automatic") or self.args.get("manual")):
    #         # magic and custom fields do not inherit from parent classes
    #         for field in reversed(
    #             fields.resolve_mro(model, name, self._can_setup_from)
    #         ):
    #             attrs.update(field.args)
    #             if "_module" in field.args:
    #                 modules.add(field.args["_module"])
    #     attrs.update(self.args)  # necessary in case self is not in class

    #     attrs["args"] = self.args
    #     attrs["model_name"] = model._name
    #     attrs["name"] = name
    #     attrs["_modules"] = modules

    #     if attrs.get("custom_compute"):
    #         # by default, computed fields are not stored, not copied and readonly
    #         attrs["store"] = attrs.get("store", False)
    #         attrs["copy"] = attrs.get("copy", False)
    #         attrs["readonly"] = attrs.get("readonly", not attrs.get("inverse"))
    #         attrs["context_dependent"] = attrs.get("context_dependent", True)
    #     if attrs.get("related"):
    #         # by default, related fields are not stored and not copied
    #         attrs["store"] = attrs.get("store", False)
    #         attrs["copy"] = attrs.get("copy", False)
    #         attrs["readonly"] = attrs.get("readonly", True)
    #     if attrs.get("company_dependent"):
    #         # by default, company-dependent fields are not stored and not copied
    #         attrs["store"] = False
    #         attrs["copy"] = attrs.get("copy", False)
    #         attrs["default"] = self._default_company_dependent
    #         attrs["compute"] = self._compute_company_dependent
    #         if not attrs.get("readonly"):
    #             attrs["inverse"] = self._inverse_company_dependent
    #         attrs["search"] = self._search_company_dependent
    #         attrs["context_dependent"] = attrs.get("context_dependent", True)
    #     if attrs.get("translate"):
    #         # by default, translatable fields are context-dependent
    #         attrs["context_dependent"] = attrs.get("context_dependent", True)
    #     if "depends" in attrs:
    #         attrs["depends"] = tuple(attrs["depends"])

    #     return attrs


# ?        return super()._get_attrs(model, name)
