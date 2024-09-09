from enum import Enum

class Collections(Enum):
    HourIntervalHistoricalData = 'HourIntervalHistoricalData'
    HourIntervalPredictedData = 'HourIntervalPredictedData'
    MinuteIntervalHistoricalData = 'MinuteIntervalHistoricalData'
    MinuteIntervalPredictedData = 'MinuteIntervalPredictedData'
    DayIntervalHistoricalData = 'DayIntervalHistoricalData'
    DayIntervalPredictedData = 'DayIntervalPredictedData'

collections_granularity = {
    Collections.HourIntervalHistoricalData.value: 'hours',
    Collections.HourIntervalPredictedData.value: 'hours',
    Collections.MinuteIntervalHistoricalData.value: 'minutes',
    Collections.MinuteIntervalPredictedData.value: 'minutes',
    Collections.DayIntervalHistoricalData.value: None,
    Collections.DayIntervalPredictedData.value: None
}

interval_historical_collections = {
    '1m': Collections.MinuteIntervalHistoricalData.value,
    '60m': Collections.HourIntervalHistoricalData.value,
    '1d': Collections.DayIntervalHistoricalData.value
}
