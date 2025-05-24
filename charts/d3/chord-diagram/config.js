/// <reference types="../dist/useeio" />
/** @type {import('useeio')} */
var useeio = useeio;

// Dynamically load model from GitHub or local repo
let model = getModel();

function getModelFolderName() {
  let hash = getUrlHash();
  let theModel = "USEEIOv2.0.1-411";
  if (hash.state) {
    let thestate = hash.state.split(",")[0].toUpperCase();
    theModel = thestate + "EEIOv1.0-s-20";
  }
  return theModel;
}

function getModel() {
  let theModel = getModelFolderName();
  const modelName = getModelFolderName();
  const modelUrl = location.hash.split('?')[0];
  const colorScale = getColorScale(30);

  return useeio.modelOf({
    // Use local clone or GitHub raw files (change this based on hosting setup)
    // Only ONE endpoint should be used

    // For GitHub:
    // endpoint: 'https://raw.githubusercontent.com/ModelEarth/useeio-json/main/models/2020',

    // For GitHub with CNAME (recommended if CORS works):
    // endpoint: 'https://model.earth/useeio-json/main/models/2020',

    // For local setup:
    endpoint: '/useeio-json/models/2020',

    model: theModel,
    asJsonFiles: true,
  });
}

function formatCell(input, format) {
  if (format === 'none' || format === '') return input;

  if (format === 'scientific') return input.toExponential(1);

  if (input >= 1e12) return (input / 1e12).toFixed(3) + ' Trillion';
  if (input >= 1e9) return (input / 1e9).toFixed(1) + ' Billion';
  if (input >= 1e6) return (input / 1e6).toFixed(1) + ' Million';
  if (input >= 1000) return (input / 1000).toFixed(1) + ' K';
  if (input >= 0) return input.toFixed(1).replace(/\.0$/, '');
  if (input >= 0.0001) return input.toFixed(4);
  if (input >= -1000) return (input / 1e3).toFixed(1) + ' K';
  if (input >= -1e9) return (input / 1e6).toFixed(1).replace(/\.0$/, '') + ' Million';
  if (input >= -1e12) return (input / 1e9).toFixed(1).replace(/\.0$/, '') + ' Billion';
  return input.toExponential(1);
}

function formatNum(numberString, locale = navigator.language) {
  if (typeof numberString !== 'string') numberString = String(numberString);
  let cleanString = numberString.replace(/[,.]/g, '');
  if (isNaN(cleanString)) return numberString;

  if (!locale || typeof locale !== 'string' || !Intl.NumberFormat.supportedLocalesOf([locale]).length) {
    locale = 'en-US';
  }

  let number = parseFloat(cleanString);
  return number.toLocaleString(locale);
}

function getColorScale(numSectors) {
  const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
  return colorScale;
}

function getUrlHash() {
  return (function (pairs) {
    if (pairs == "") return {};
    let result = {};
    pairs.forEach(function (pair) {
      let keyValue = pair.split('=');
      let key = keyValue[0];
      let value = keyValue.slice(1).join('=').replace(/%26/g, '&');
      result[key] = value;
    });
    return result;
  })(window.location.hash.substr(1).split('&'));
}

// Function to dynamically update the color scale based on number of sectors
function updateColorScale(numSectors) {
  const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
  // Adjust the color scale based on numSectors
  return colorScale;
}

function fetchModelData() {
  // Fetch the data from the model based on dynamic model setup
  const model = getModel();
  model.load().then(() => {
    console.log("Model loaded successfully.");
    // Additional logic after the model is loaded
  }).catch(error => {
    console.error("Error loading model:", error);
  });
}

// Fetch model data when page loads
fetchModelData();
