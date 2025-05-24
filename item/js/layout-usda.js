// We'll have multiple version of this script for custom layouts.
// dailyValue might become goal. Later "average" will convery what the average person eats.
function createProfileObject(sourceData) {
    return {
    "itemName": sourceData.description,
    "sections": [
        { "name": "Calories", "value": sourceData.valueCalories },
        { "name": "Calories from Fat", "value": sourceData.valueFatCalories },
        {
            "name": "Total Fat",
            "value": sourceData.valueTotalFat,
            "dailyValue": calculateDailyValue(sourceData.valueTotalFat, 'fat'),
            "subsections": [
                { "name": "Saturated Fat", "value": sourceData.valueSatFat, "dailyValue": calculateDailyValue(sourceData.valueSatFat, 'satFat') },
                { "name": "Trans Fat", "value": sourceData.valueTransFat }
            ]
        },
        { "name": "Cholesterol", "value": sourceData.valueCholesterol, "dailyValue": calculateDailyValue(sourceData.valueCholesterol, 'cholesterol') },
        { "name": "Sodium", "value": sourceData.valueSodium, "dailyValue": calculateDailyValue(sourceData.valueSodium, 'sodium') },
        {
            "name": "Total Carbohydrate",
            "value": sourceData.valueTotalCarb,
            "dailyValue": calculateDailyValue(sourceData.valueTotalCarb, 'carb'),
            "subsections": [
                { "name": "Dietary Fiber", "value": sourceData.valueFibers, "dailyValue": calculateDailyValue(sourceData.valueFibers, 'fiber') },
                { "name": "Sugars", "value": sourceData.valueSugars }
            ]
        },
        { "name": "Protein", "value": sourceData.valueProteins },
        { "name": "Vitamin D", "value": sourceData.valueVitaminD, "dailyValue": calculateDailyValue(sourceData.valueVitaminD, 'vitaminD') },
        { "name": "Potassium", "value": sourceData.valuePotassium_2018, "dailyValue": calculateDailyValue(sourceData.valuePotassium_2018, 'potassium') },
        { "name": "Calcium", "value": sourceData.valueCalcium, "dailyValue": calculateDailyValue(sourceData.valueCalcium, 'calcium') },
        { "name": "Iron", "value": sourceData.valueIron, "dailyValue": calculateDailyValue(sourceData.valueIron, 'iron') },
        { "name": "Added Sugars", "value": sourceData.valueAddedSugars, "dailyValue": calculateDailyValue(sourceData.valueAddedSugars, 'addedSugars') },
        { "name": "Caffeine", "value": sourceData.valueCaffeine }
    ]
    }
}