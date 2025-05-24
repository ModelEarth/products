export const USDA_REQUIRED_NUTRIENTS = [
    'Total lipid (fat)',
    'Fatty acids, total saturated',
    'Cholesterol',
    'Sodium, Na',
    'Carbohydrate, by difference',
    'Fiber, total dietary',
    'Total Sugars',
    'Protein',
    'Vitamin D (D2 + D3), International Units',
    'Calcium, Ca',
    'Iron, Fe',
    'Potassium, K',
  ];
  
  export const VITAMIN_NUTRIENTS = [
    'Vitamin A, IU',
    'Vitamin C, total ascorbic acid',
    'Vitamin D (D2 + D3), International Units',
    'Vitamin E (alpha-tocopherol)',
    'Vitamin K (phylloquinone)',
    'Thiamin',
    'Riboflavin',
    'Niacin',
    'Vitamin B-6',
    'Folate, total',
    'Vitamin B-12',
    'Choline, total',
  ];
  
  const DIET_REQUIREMENTS = {
    keto: {
      'Total lipid (fat)': { min: 70, max: 80, unit: 'g' },
      'Carbohydrate, by difference': { max: 20, unit: 'g' },
      'Protein': { min: 25, max: 35, unit: 'g' },
      // Add other nutrient requirements as necessary
    },
    // Add other diets as needed
  };
  
  export const compareNutrientsToDiet = (foodNutrients, diet) => {
    const gaps = [];
    const dietNutrients = DIET_REQUIREMENTS[diet];
  
    Object.keys(dietNutrients).forEach(nutrientName => {
      const foodNutrient = foodNutrients.find(n => n.nutrient.name === nutrientName);
      const requirement = dietNutrients[nutrientName];
  
      if (foodNutrient) {
        const amount = parseFloat(foodNutrient.amount);
        if ((requirement.min && amount < requirement.min) || (requirement.max && amount > requirement.max)) {
          gaps.push({
            nutrient: nutrientName,
            amount,
            required: `${requirement.min || 0}-${requirement.max || '∞'} ${requirement.unit}`,
          });
        }
      } else {
        gaps.push({
          nutrient: nutrientName,
          amount: 'N/A',
          required: `${requirement.min || 0}-${requirement.max || '∞'} ${requirement.unit}`,
        });
      }
    });
  
    return gaps;
  };
  