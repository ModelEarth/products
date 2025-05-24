// Displays a label for food nutrition or product impact.
// profileObject is built by createProfileObject() in layout-.js template.

document.addEventListener('hashChangeEvent', hashChangedProfile, false);
function hashChangedProfile() {
    console.log("Profile hash changed");
    loadProfile();
}
loadProfile();

function getUrlHash() {
  return (function (pairs) {
    if (pairs == "") return {};
    var result = {};
    pairs.forEach(function(pair) {
      // Split the pair on "=" to get key and value
      var keyValue = pair.split('=');
      var key = keyValue[0];
      var value = keyValue.slice(1).join('=');

      // Replace "%26" with "&" in the value
      value = value.replace(/%26/g, '&');

      // Set the key-value pair in the result object
      result[key] = value;
    });
    return result;
  })(window.location.hash.substr(1).split('&'));
}

// Recommended daily intake / Average impacts
const dailyValueCalculations = {
    fat: 65, // Total Fat
    satFat: 20, // Saturated Fat
    cholesterol: 300, // Cholesterol
    sodium: 2400, // Sodium
    carb: 300, // Total Carbohydrate
    fiber: 25, // Dietary Fiber
    addedSugars: 50, // Added Sugars
    vitaminD: 20, // Vitamin D (mcg)
    calcium: 1300, // Calcium (mg)
    iron: 18, // Iron (mg)
    potassium: 4700 // Potassium (mg)
};
$(document).ready(function () {
    $("#dailyDiv").text(JSON.stringify(dailyValueCalculations));
});

// Calculate daily values (assuming source data is for a typical 2,000-calorie diet)
// Called from layout-nutrition.js
function calculateDailyValue(value, type) {
    const base = dailyValueCalculations[type];
    return base ? ((value / base) * 100).toFixed(0) : null;
}

function populateNutritionLabel(data) {
    document.getElementById("item-name").innerText = data.itemName;

    const sectionsContainer = document.getElementById("sections");
    sectionsContainer.innerHTML = ''; // Clear existing content

    data.sections.forEach(section => {
        const sectionDiv = document.createElement("div");
        sectionDiv.classList.add("nutrition-section");

        // Add section name and value
        sectionDiv.innerHTML = `
            <div class="section-title">
                <span><strong>${section.name}</strong> <span class="value">${section.value}${section.value ? 'g' : ''}</span></span>
                <span class="daily-value">${section.dailyValue ? section.dailyValue + '%' : ''}</span>
            </div>
        `;

        // Add subsections if they exist
        if (section.subsections) {
            section.subsections.forEach(subsection => {
                const subSectionDiv = document.createElement("div");
                subSectionDiv.classList.add("sub-section");
                if (subsection.extraIndent) subSectionDiv.classList.add("extra-indent");

                subSectionDiv.innerHTML = `
                    <span>${subsection.name}</span>
                    <span class="value">${subsection.value}${subsection.value ? 'g' : ''}</span>
                    <span class="daily-value">${subsection.dailyValue ? subsection.dailyValue + '%' : ''}</span>
                `;

                sectionDiv.appendChild(subSectionDiv);
            });
        }

        sectionsContainer.appendChild(sectionDiv);
        sectionsContainer.appendChild(document.createElement('hr')).classList.add('thin-line');
    });
}

// Function to update the nutrition label based on quantity
function updateNutritionLabel(quantity) {
    const updatedData = JSON.parse(JSON.stringify(profileObject));
    updatedData.sections.forEach(section => {
        if (section.value) section.value = (section.value * quantity).toFixed(2);
        if (section.dailyValue) section.dailyValue = (section.dailyValue * quantity).toFixed(0);
        if (section.subsections) {
            section.subsections.forEach(subsection => {
                if (subsection.value) subsection.value = (subsection.value * quantity).toFixed(2);
                if (subsection.dailyValue) subsection.dailyValue = (subsection.dailyValue * quantity).toFixed(0);
            });
        }
    });
    populateNutritionLabel(updatedData);
}

// Parse the source data into the desired structure
let profileObject = {};

function loadProfile() {
    let hash = getUrlHash();
    let labelType = "food";
    let whichLayout = "js/layout-nutrition.js";
    if (hash.layout == "product") {
        labelType = "product";
        whichLayout = "js/layout-product.js";
    } // Also add removeElement() line below for new layouts.
    whichLayout = "/profile/item/" + whichLayout;

    // Remove prior layout-.js since createProfileObject() repeats.
    // detach() could possibly be used to assign to a holder then restore.
    removeElement('/profile/item/js/layout-nutrition.js'); // Resides in localsite/js/localsite.js
    removeElement('/profile/item/js/layout-product.js');

    loadScript(whichLayout, function(results) {
        let sourceData = {};
        // TO DO: Load these from API or file
        if (labelType == "product") {
            // https://github.com/ModelEarth/io/blob/main/template/product/product-nodashes.yaml
            sourceData = {
                itemName: 'Sample Product',
                id: "ec3yznau",
                ref: "https://openepd.buildingtransparency.org/api/epds/EC3YZNAU",
                doctype: "OpenEPD",
                version: null,
                language: "en",
                valueGlobalWarmingPotential: 445 ,
                ghgunits: "kg CO2 eq"
                /*
                private: false,
                program_operator_doc_id: "9BD4F9CB-3584-4D34-90F8-B6E40B69653D",
                program_operator_version: null,
                third_party_verification_url: null,
                date_of_issue: '2019-01-28T00:00:00Z',
                valid_until: '2024-01-28T00:00:00Z',
                kg_C_per_declared_unit: null,
                product_name: DM0115CA,
                product_sku: null,
                product_description: "DOT MINOR 3/4 15FA 3-5SL AIR",
                product_image_small: null,
                product_image: null,
                product_service_life_years: null,
                applicable_in: null,
                product_usage_description: null,
                product_usage_image: null,
                manufacturing_description: null,
                manufacturing_image: null,
                compliance: []
                */
            };
        }

        if (labelType == "food") {
            // Example source data from the provided object
            sourceData = {
                showServingUnitQuantity: false,
                itemName: 'Bleu Cheese Dressing',
                ingredientList: 'Bleu Cheese Dressing',
                decimalPlacesForQuantityTextbox: 2,
                valueServingUnitQuantity: 1,
                allowFDARounding: true,
                decimalPlacesForNutrition: 2,
                showPolyFat: false,
                showMonoFat: false,
                valueCalories: 450,
                valueFatCalories: 430,
                valueTotalFat: 48,
                valueSatFat: 6,
                valueTransFat: 0,
                valueCholesterol: 30,
                valueSodium: 780,
                valueTotalCarb: 3,
                valueFibers: 0,
                valueSugars: 3,
                valueProteins: 3,
                valueVitaminD: 12.22,
                valuePotassium_2018: 4.22,
                valueCalcium: 7.22,
                valueIron: 11.22,
                valueAddedSugars: 17,
                valueCaffeine: 15.63,
                showLegacyVersion: false
            };
        }

        // TO DO: Since createProfileObject occurs twice, drop one of the layout-.js files.

        profileObject = createProfileObject(sourceData); // Guessing
        console.log("profileObject:")
        console.log(profileObject);

        $(document).ready(function () { // TO DO: Change to just wait for #item-name
            if (hash.layout == "product") {
                $("#nutritionFooter").hide();
            } else {
                $("#nutritionFooter").show();
            }

            // Event listeners for quantity input
            document.getElementById('quantity-input').addEventListener('change', (e) => {
                const quantity = parseFloat(e.target.value) || 1;
                updateNutritionLabel(quantity);
            });

            document.getElementById('decrease-quantity').addEventListener('click', () => {
                const input = document.getElementById('quantity-input');
                let quantity = parseFloat(input.value) || 1;
                if (quantity > 1) {
                    quantity--;
                    input.value = quantity;
                    updateNutritionLabel(quantity);
                }
            });

            document.getElementById('increase-quantity').addEventListener('click', () => {
                const input = document.getElementById('quantity-input');
                let quantity = parseFloat(input.value) || 1;
                quantity++;
                input.value = quantity;
                updateNutritionLabel(quantity);
            });

            // Initial population - HTML
            populateNutritionLabel(profileObject);
            
            $("#sourceDiv").text(JSON.stringify(sourceData));
            $("#jsonDiv").text(JSON.stringify(profileObject));
        });
    });
}