<a href="/profile">Profile Panels</a> - <a href="/io/template">IO Template</a>

# Profile YAML and JS

Toggle between [Nutrition Layout](#layout=nutrition) and [Product Layout](#layout=product)

[View Profile Label JavaScript](https://github.com/ModelEarth/profile/blob/main/item/js/label.js)

TO DO: Add emissions details from [BuildingTransparency.org Products](/profile/products/) to the [Product Layout](#layout=product).  

TO DO: Create a list of food linked to the label formatter below using the Food API pull examples in our [Food Data Commons](/data-commons/docs/food/)

Our following label builder is similar to a [Nutritionix Label](/data-commons/docs/food/), but it's easier to reuse since the layout object is built from YAML by a javascript template. Here's an assist from [ChatGPT](https://chatgpt.com/share/68ade5c5-9b05-46a8-a0da-ccd771289693). Combines Food YAML and Daily Recommended YAML to create Profile Object json.

