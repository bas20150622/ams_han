# Marshmallow schemas for queries and subscriptions data

from marshmallow import Schema, fields, pre_load


class liveMeasurementsDetailedSubscriptionSchema(Schema):
    timestamp = fields.DateTime()
    power = fields.Int()
    currentL1 = fields.Float()
    currentL2 = fields.Float()
    currentL3 = fields.Float()
    voltagePhase1 = fields.Float()
    voltagePhase2 = fields.Float()
    voltagePhase3 = fields.Float()
    powerFactor = fields.Float()
    maxPower = fields.Int()
    minPower = fields.Int()
    averagePower = fields.Float()
    lastMeterConsumption = fields.Float()

    class Meta:
        dateformat = "%Y-%m-%dT%H:%M:%S.%f+01:00"

    @pre_load
    def flatten_data(self, in_data, **kwargs):
        out_data = in_data.get("data", {}).get("liveMeasurement", False)
        if out_data:
            out_data = {key: val for key, val in out_data.items() if val}
            return out_data
        raise ValueError("key data not found")
