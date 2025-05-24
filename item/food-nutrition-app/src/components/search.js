import React, { useState } from 'react';
import './Search.css';
import Label from './label.js';

const Search = () => {
  const [searchInput, setSearchInput] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [servingSizes, setServingSizes] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = async (e) => {
    const value = e.target.value;
    setSearchInput(value);

    if (value.length > 3) {
      setLoading(true);
      try {
        const data = await loadDataCommons_search('bLecediTVa2sWd8AegmUZ9o7DxYFSYoef9B4i1Ml', value);
        setSuggestions(data.foods);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSelectSuggestion = async (suggestion) => {
    setLoading(true);
    try {
      const data = await fetchFoodDetails('bLecediTVa2sWd8AegmUZ9o7DxYFSYoef9B4i1Ml', suggestion.fdcId);
      const enrichedData = {
        ...data,
        foodCategory: suggestion.foodCategory,
        brandName: suggestion.brandName,
      };
      setSearchResults([...searchResults, enrichedData]);
      setServingSizes([...servingSizes, enrichedData.servingSize || 100]);
      setSearchInput("");
      setSuggestions([]);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadDataCommons_search = async (apiKey, keyword) => {
    const url = `https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${apiKey}&query=${keyword}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return await response.json();
  };

  const fetchFoodDetails = async (apiKey, fdcId) => {
    const url = `https://api.nal.usda.gov/fdc/v1/food/${fdcId}?api_key=${apiKey}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch food details');
    }
    return await response.json();
  };

  const handleRemoveResult = (index) => {
    setSearchResults(searchResults.filter((_, i) => i !== index));
    setServingSizes(servingSizes.filter((_, i) => i !== index));
  };

  const handleServingSizeChange = (index, newSize) => {
    const updatedSizes = [...servingSizes];
    updatedSizes[index] = newSize;
    setServingSizes(updatedSizes);
  };

  const renderFoodItem = (food) => {
    return food.dataType === "Branded" 
      ? `${food.description}, ${food.foodCategory}, ${food.brandName}`
      : food.description;
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Enter your food search"
        onChange={handleInputChange}
        value={searchInput}
      />
      {loading && <p>Loading...</p>}
      {suggestions.length > 0 && (
        <ul className="suggestions-list">
          {suggestions.map((suggestion) => (
            <li key={suggestion.fdcId} onClick={() => handleSelectSuggestion(suggestion)}>
              {renderFoodItem(suggestion)}
            </li>
          ))}
        </ul>
      )}
      {error && <p className="error">{error}</p>}
      <div className="results-container">
        {searchResults.map((result, index) => (
          <div key={result.fdcId} className="result-item">
            <span>{renderFoodItem(result)}</span>
            <input
              type="number"
              value={servingSizes[index]}
              onChange={(e) => handleServingSizeChange(index, parseFloat(e.target.value))}
              min="1"
            />
            <button onClick={() => handleRemoveResult(index)}>x</button>
          </div>
        ))}
      </div>
      <Label searchResults={searchResults} servingSizes={servingSizes} />
    </div>
  );
};

export default Search;
