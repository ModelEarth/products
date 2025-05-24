
// share / download/ copy of menus 
// keto sets diet 

import React, { useState } from 'react';
import './Label.css';
import { USDA_REQUIRED_NUTRIENTS, VITAMIN_NUTRIENTS, compareNutrientsToDiet } from './Diets.js';

const Label = ({ searchResults, servingSizes, selectedDiet }) => {

  console.log(searchResults)


  const getTotalNutrients = () => {
    const totalNutrients = {};
    searchResults.forEach((result, index) => {
      result.foodNutrients.forEach(nutrient => {
        if (!totalNutrients[nutrient.nutrient.name]) {
          totalNutrients[nutrient.nutrient.name] = 0;
        }
        const originalServingSize = result.servingSize || 100;
        const adjustedAmount = (nutrient.amount * servingSizes[index]) / originalServingSize;
        totalNutrients[nutrient.nutrient.name] += adjustedAmount;
      });
    });
    return totalNutrients;
  };

  const totalNutrients = getTotalNutrients();

  const usdaNutrients = USDA_REQUIRED_NUTRIENTS.map(nutrient => ({
    name: nutrient,
    amount: totalNutrients[nutrient] || 0,
  }));

  const vitaminNutrients = VITAMIN_NUTRIENTS.map(nutrient => ({
    name: nutrient,
    amount: totalNutrients[nutrient] || 0,
  }));

  const otherNutrients = Object.keys(totalNutrients)
    .filter(nutrient => !USDA_REQUIRED_NUTRIENTS.includes(nutrient) && !VITAMIN_NUTRIENTS.includes(nutrient))
    .map(nutrient => ({
      name: nutrient,
      amount: totalNutrients[nutrient],
    }));

  return (
    <div className="label-container">
      <TotalNutrientsLabel
        usdaNutrients={usdaNutrients}
        vitaminNutrients={vitaminNutrients}
        otherNutrients={otherNutrients}
      />
      {searchResults.map((result, index) => (
        <NutritionLabel
          key={index}
          result={result}
          servingSize={servingSizes[index]}
          selectedDiet={selectedDiet}
        />
      ))}
    </div>
  );
};

const NutritionLabel = ({ result, servingSize, selectedDiet }) => {
  const [showAll, setShowAll] = useState(false);

  const toggleShowAll = () => {
    setShowAll(!showAll);
  };

  const getNutrientValue = (result, nutrientName) => {
    const nutrient = result.foodNutrients.find(n => n.nutrient.name === nutrientName);
    if (!nutrient) return 'N/A';
    const originalServingSize = result.servingSize || 100;
    const adjustedAmount = (nutrient.amount * servingSize) / originalServingSize;
    return `${adjustedAmount.toFixed(2)} ${nutrient.nutrient.unitName}`;
  };

  const usdaNutrients = result.foodNutrients.filter(nutrient =>
    USDA_REQUIRED_NUTRIENTS.includes(nutrient.nutrient.name)
  );

  const vitaminNutrients = result.foodNutrients.filter(nutrient =>
    VITAMIN_NUTRIENTS.includes(nutrient.nutrient.name)
  );

  const otherNutrients = result.foodNutrients.filter(
    nutrient => !USDA_REQUIRED_NUTRIENTS.includes(nutrient.nutrient.name) && !VITAMIN_NUTRIENTS.includes(nutrient.nutrient.name)
  );

  const gaps = selectedDiet ? compareNutrientsToDiet(result.foodNutrients, selectedDiet) : [];

  return (
    <div className="item-label">
      <h2>{result.description}</h2>
      <p>Brand: {result.brandName || 'N/A'}</p>

      <div className="serving">
        <span>Serving Size</span>
        <span>{servingSize ? `${servingSize} ${result.servingSizeUnit}` : 'N/A'}</span>
      </div>

      <div className="calories">
        <span>Calories</span>
        <span>{getNutrientValue(result, 'Energy')}</span>
      </div>
      <div className="nutrition-facts">
        <h3>Nutrition Facts</h3>

        {usdaNutrients.map((nutrient, index) => (
          <div key={index} className="nutrition-item">
            <span>{nutrient.nutrient.name}</span>
            <span>{getNutrientValue(result, nutrient.nutrient.name)}</span>
          </div>
        ))}

        <h4>Vitamins</h4>
        {vitaminNutrients.map((nutrient, index) => (
          <div key={index} className="nutrition-item">
            <span>{nutrient.nutrient.name}</span>
            <span>{getNutrientValue(result, nutrient.nutrient.name)}</span>
          </div>
        ))}

        {showAll &&
          otherNutrients.map((nutrient, index) => (
            <div key={index} className="nutrition-item">
              <span>{nutrient.nutrient.name}</span>
              <span>{getNutrientValue(result, nutrient.nutrient.name)}</span>
            </div>
          ))}
        <div className="nutrition-item">
          <button onClick={toggleShowAll}>{showAll ? 'Show Less' : '...More'}</button>
        </div>
      </div>

      {selectedDiet && (
        <div className="diet-gaps">
          <h4>{selectedDiet.charAt(0).toUpperCase() + selectedDiet.slice(1)} Diet Gaps</h4>
          {gaps.length > 0 ? (
            gaps.map((gap, index) => (
              <div key={index} className="gap-item">
                <span>{gap.nutrient}</span>
                <span>{`Current: ${gap.amount}, Required: ${gap.required}`}</span>
              </div>
            ))
          ) : (
            <p>No gaps found.</p>
          )}
        </div>
      )}

      <p className="date">Publication Date: {result.publicationDate || 'N/A'}</p>
    </div>
  );
};

const TotalNutrientsLabel = ({ usdaNutrients, vitaminNutrients, otherNutrients }) => {
  const calories = usdaNutrients.find(nutrient => nutrient.name === "Energy")?.amount.toFixed(2) || "N/A";

  return (
    <div className="item-label">
      <h2>Total Nutrients</h2>

      <div className="calories">
        <span>Calories</span>
        <span>{calories}</span>
      </div>
      <div className="nutrition-facts">
        <h3>Nutrition Facts</h3>
        {usdaNutrients.map((nutrient, index) => (
          <div key={index} className="nutrition-item">
            <span>{nutrient.name}</span>
            <span>{nutrient.amount.toFixed(2)}</span>
          </div>
        ))}

        <h4>Vitamins</h4>
        {vitaminNutrients.map((nutrient, index) => (
          <div key={index} className="nutrition-item">
            <span>{nutrient.name}</span>
            <span>{nutrient.amount.toFixed(2)}</span>
          </div>
        ))}

        {otherNutrients.length > 0 && (
          <>
            <h4>Other Nutrients</h4>
            {otherNutrients.map((nutrient, index) => (
              <div key={index} className="nutrition-item">
                <span>{nutrient.name}</span>
                <span>{nutrient.amount.toFixed(2)}</span>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default Label;
