.. py:module:: pvpltools.module_efficiency

.. currentmodule:: pvpltools

====================
PV module efficiency
====================

This module contains implementations of several PV module efficiency models.

These models have a common purpose, which is to predict the efficiency at
maximum power point as a function of the main operating conditions:
effective irradiance and module temperature.

A function to fit any of these models to measurements is also provided.

.. autosummary::
   :toctree: generated/

   module_efficiency.fit_efficiency_model
   module_efficiency.adr
   module_efficiency.heydenreich
   module_efficiency.motherpv
   module_efficiency.pvgis
   module_efficiency.mpm6
   module_efficiency.mpm5
   module_efficiency.fit_bilinear
   module_efficiency.bilinear
