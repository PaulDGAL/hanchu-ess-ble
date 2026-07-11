"""Switch platform for Hanchu ESS BLE - Inverter On/Off (P500)."""

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

POWER_KEY = "P500"   # 0 = Off, 1 = On


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([InverterPowerSwitch(coordinator, entry)])


class InverterPowerSwitch(CoordinatorEntity, SwitchEntity):
    """On/Off switch for inverter power state (P500)."""

    _attr_has_entity_name = True
    _attr_name = "Inverter Power"
    _attr_icon = "mdi:power"
    _attr_entity_category = EntityCategory.CONFIG
    _entity_registry_enabled_default = False
    
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{coordinator.address}_inverter_power"

#    @property
#    def device_info(self) -> DeviceInfo:
#        return DeviceInfo(
#            identifiers={(DOMAIN, self.coordinator.address)},
#            name=self.coordinator.configured_name,
#            manufacturer="Hanchu",
#            model="ESS Device (Local BLE)",
#        )
    @property 
    def device_info(self) -> DeviceInfo: 
        return DeviceInfo( 
            identifiers={ 
             (DOMAIN, f"{self.coordinator.address}_controls") 
            }, 
            name=f"{self.coordinator.data.configured_name} Controls", 
            manufacturer="Hanchu", 
            model="ESS Controls", 
            via_device=(DOMAIN, self.coordinator.address), 
        ) 


    @property
    def is_on(self) -> bool | None:
        """Return True if inverter is ON (P500 = 1)."""
        if not self.coordinator.data or not self.coordinator.data.values:
            return None
        value = self.coordinator.data.values.get(POWER_KEY)
        if value is None:
            return None
        try:
            return int(float(value)) == 1
        except (ValueError, TypeError):
            return None

    async def async_turn_on(self, **kwargs):
        """Send P500 = 1 over BLE."""
        await self._async_write_power(1)

    async def async_turn_off(self, **kwargs):
        """Send P500 = 0 over BLE."""
        await self._async_write_power(0)

    async def _async_write_power(self, value: int):
        try:
            reply = await self.coordinator.client.async_write_value(
                POWER_KEY, value, encrypted=True
            )
        except Exception as err:
            _LOGGER.error("Failed to set inverter power: %s", err)
            return

        result = reply.as_dict().get(POWER_KEY)
        if result == 0:
            _LOGGER.info("Inverter power set to %s", value)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error(
                "Inverter power write did not confirm success: %s",
                reply.as_dict(),
            )