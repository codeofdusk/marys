# Marys
A Python library to obtain dining hours and menus at Swarthmore College.

Copyright 2021–2022 Bill Dengler

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) (the "Licence");
you may not use this library except in compliance with the Licence.

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and
limitations under the Licence.
If the terms of the licence pose a serious obstacle for your use, please contact the author.

## Getting started
``` python console
>>> import marys
>>> m=marys.Menu()  # Fetch latest menus from The Dash
```

### JSON API
`Menu` objects make the full json API available, so programs that rely on it can start using Marys immediately.

```python console
>>> m["sharples"][0]["title"]
'Breakfast'
>>> m["sharples"][0]["enddate"]
'2022-02-14 09:30:00'
>>> m["sharples"][0]["description"]
"Soup Island: Oatmeal with Raisins, Craisins &amp; Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg &amp; Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels &amp; Spreads Yogurt, Granola &amp; Cereal Dessert: Baker's Choice of Pastry or Donuts"
```

### Conveniences
Marys adds extra features on top of the base API to ease access to the menu.

#### `cleaned_description`
While the original `description` is provided for backwards compatibility with the original JSON API, there is also a `cleaned_description` more suitable for use inside applications, with resolved HTML entities and cleaned-up formatting.

```python console
>>> m["sharples"][0]["cleaned_description"]
"Soup Island: Oatmeal with Raisins, Craisins & Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg & Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels & Spreads Yogurt, Granola & Cereal Dessert: Baker's Choice of Pastry or Donuts"
```

#### Access by meal period
`Menu` objects contain special `breakfast`, `lunch`, `dinner`, and `now` keys for accessing breakfast, lunch, dinner, or currently available meals respectively. Lunch automatically resolves to brunch when necessary.

```python console
>>> m["breakfast"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Breakfast {'title': 'Breakfast', 'startdate': '2022-02-14 07:30:00', 'enddate': '2022-02-14 09:30:00', 'short_time': '7:30am - 9:30am', 'description': "Soup Island: Oatmeal with Raisins, Craisins &amp; Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg &amp; Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels &amp; Spreads Yogurt, Granola &amp; Cereal Dessert: Baker's Choice of Pastry or Donuts", 'html_description': "<strong>Soup Island:</strong>&nbsp;Oatmeal with Raisins, Craisins &amp; Cinnamon Sugar<br /><strong>Main:</strong>&nbsp;Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes<br />Phoenixes - Egg &amp; Cheese Sandwiches<br />Chef's Choice of Waffles, French Toast or Pancakes<br />Fresh Fruit, Selection of Bread, Bagels &amp; Spreads<br />Yogurt, Granola &amp; Cereal<br /><strong>Dessert:</strong>&nbsp;Baker's Choice of Pastry or Donuts", 'cleaned_description': "Soup Island: Oatmeal with Raisins, Craisins & Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg & Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels & Spreads Yogurt, Granola & Cereal Dessert: Baker's Choice of Pastry or Donuts"}, Sharples Dining Hall Continental Breakfast {'title': 'Continental Breakfast', 'startdate': '2022-02-14 09:30:00', 'enddate': '2022-02-14 10:30:00', 'short_time': '9:30am - 10:30am', 'description': 'Served by the Fireplace - Includes Selection of Breads &amp; Bagels, Spreads, Yogurt &amp; Granola, Cereal, Fresh Bakery Special or Donuts, Full Beverage Station with Coffee', 'html_description': 'Served by the Fireplace - Includes Selection of Breads &amp; Bagels, Spreads, Yogurt &amp; Granola, Cereal, Fresh Bakery Special or Donuts,&nbsp;Full Beverage Station with Coffee', 'cleaned_description': 'Served by the Fireplace - Includes Selection of Breads & Bagels, Spreads, Yogurt & Granola, Cereal, Fresh Bakery Special or Donuts, Full Beverage Station with Coffee'}]}
>>> m["lunch"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Lunch {'title': 'Lunch', 'startdate': '2022-02-14 10:30:00', 'enddate': '2022-02-14 13:30:00', 'short_time': '10:30am - 1:30pm', 'description': "Chicken Fingers and Fries Homestyle Tofu with Green Beans ::vegan::, Vegetable Lo Mein Cheesesteak Bar, with Vegan, Beef, and Chicken Options, and Toppings Corn, Peas Soups: Vegetable ::vegan::, Tomato Dessert: Hope's Homestyle Cookies, Homemade Vegan Cookies", 'html_description': "<ul><li>Chicken Fingers and Fries</li><li>Homestyle Tofu with Green Beans ::vegan::, Vegetable Lo Mein</li><li>Cheesesteak Bar, with Vegan, Beef, and Chicken Options, and Toppings</li><li>Corn, Peas</li><li>Soups:&nbsp; Vegetable ::vegan::, Tomato</li><li>Dessert:&nbsp; Hope's Homestyle Cookies, Homemade Vegan Cookies</li></ul>", 'cleaned_description': "Chicken Fingers and Fries Homestyle Tofu with Green Beans ::vegan::, Vegetable Lo Mein Cheesesteak Bar, with Vegan, Beef, and Chicken Options, and Toppings Corn, Peas Soups: Vegetable ::vegan::, Tomato Dessert: Hope's Homestyle Cookies, Homemade Vegan Cookies"}, Sharples Dining Hall Lite Lunch {'title': 'Lite Lunch', 'startdate': '2022-02-14 13:30:00', 'enddate': '2022-02-14 16:00:00', 'short_time': '1:30pm - 4:00pm', 'description': 'Includes Salad Bar and Deli with Selection of Breads &amp; Wraps, Soups of the Day, Cereal &amp; Granola, Ice Cream &amp; Frozen Yogurt, Fresh Fruit, Full Beverage Station with Coffee', 'html_description': 'Includes Salad Bar and Deli with Selection of Breads &amp; Wraps, Soups of the Day, Cereal &amp; Granola, Ice Cream &amp; Frozen Yogurt, Fresh Fruit,&nbsp;Full Beverage Station with Coffee', 'cleaned_description': 'Includes Salad Bar and Deli with Selection of Breads & Wraps, Soups of the Day, Cereal & Granola, Ice Cream & Frozen Yogurt, Fresh Fruit, Full Beverage Station with Coffee'}], 'kohlberg': Kohlberg coffee bar [Kohlberg coffee bar Grab & Go Lunch {'title': 'Grab & Go Lunch', 'startdate': '2022-02-14 11:30:00', 'enddate': '2022-02-14 13:30:00', 'short_time': '11:30am - 1:30pm', 'description': "Grilled Chicken &amp; Pesto Sandwich on Ciabatta ::halal:: Hummus &amp; Olive Sandwich ::vegan:: Chocolate Sesame Butter &amp; Jam on Multigrain ::vegan:: Chicken Caesar Salad ::halal:: Chef's Salad with Ham, Turkey and Cheese", 'html_description': "<html-blob><u></u>Grilled Chicken &amp; Pesto Sandwich on Ciabatta ::halal::&nbsp;&nbsp;<br>Hummus &amp; Olive Sandwich ::vegan::&nbsp;&nbsp;<br>Chocolate Sesame Butter &amp; Jam on Multigrain ::vegan::&nbsp;&nbsp;<br>Chicken Caesar Salad ::halal::&nbsp;&nbsp;<br>Chef's Salad with Ham, Turkey and Cheese&nbsp;&nbsp;<u></u></html-blob>", 'cleaned_description': "Grilled Chicken & Pesto Sandwich on Ciabatta ::halal:: Hummus & Olive Sandwich ::vegan:: Chocolate Sesame Butter & Jam on Multigrain ::vegan:: Chicken Caesar Salad ::halal:: Chef's Salad with Ham, Turkey and Cheese"}]}
>>> m["dinner"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Dinner {'title': 'Dinner', 'startdate': '2022-02-14 16:00:00', 'enddate': '2022-02-14 20:00:00', 'short_time': '4:00pm - 8:00pm', 'description': 'Tilapia with Seafood Sauce, Rice Pilaf Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan:: Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth Pennsylvania Blend, Cauliflower Soups: Vegetable ::vegan::, Tomato Dessert: Cupcakes', 'html_description': '<ul><li>Tilapia with Seafood Sauce, Rice Pilaf</li><li>Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan::</li><li>Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth</li><li>Pennsylvania Blend, Cauliflower</li><li>Soups:&nbsp; Vegetable ::vegan::, Tomato</li><li>Dessert:&nbsp; Cupcakes</li></ul>', 'cleaned_description': 'Tilapia with Seafood Sauce, Rice Pilaf Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan:: Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth Pennsylvania Blend, Cauliflower Soups: Vegetable ::vegan::, Tomato Dessert: Cupcakes'}]}
>>> m["now"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Dinner {'title': 'Dinner', 'startdate': '2022-02-14 16:00:00', 'enddate': '2022-02-14 20:00:00', 'short_time': '4:00pm - 8:00pm', 'description': 'Tilapia with Seafood Sauce, Rice Pilaf Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan:: Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth Pennsylvania Blend, Cauliflower Soups: Vegetable ::vegan::, Tomato Dessert: Cupcakes', 'html_description': '<ul><li>Tilapia with Seafood Sauce, Rice Pilaf</li><li>Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan::</li><li>Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth</li><li>Pennsylvania Blend, Cauliflower</li><li>Soups:&nbsp; Vegetable ::vegan::, Tomato</li><li>Dessert:&nbsp; Cupcakes</li></ul>', 'cleaned_description': 'Tilapia with Seafood Sauce, Rice Pilaf Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan:: Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth Pennsylvania Blend, Cauliflower Soups: Vegetable ::vegan::, Tomato Dessert: Cupcakes'}], 'essies': Essie Mae's [Essie Mae's Essie Mae's Open {'title': "Essie Mae's Open", 'startdate': '2022-02-14 08:00:00', 'enddate': '2022-02-14 22:30:00', 'short_time': '8:00am - 10:30pm', 'description': "Here to serve you Breakfast, lunch and Dinner Today's Lunch Special South of the Border Burger- Beef patty, pepper jack cheese, bacon and pico de gallo with French fries and a choice of drink. Todays Soup Lobster Bisque Late Night Meal Plan is available 4pm till 10pm and tonight's local food vendor is Yangzi from Media. Please be aware that the Grill close's nightly at 9:30pm.", 'html_description': "<html-blob><u></u><u></u>Here to serve you Breakfast, lunch and Dinner&nbsp;<br><b>Today's Lunch Special&nbsp;</b><u></u><br><u></u>South of the Border Burger- Beef patty, pepper jack cheese, bacon and pico de gallo with French fries and a choice of drink.&nbsp;<br><b>Todays Soup&nbsp;</b></html-blob><br><html-blob>Lobster Bisque&nbsp;<br>Late Night Meal Plan is available 4pm till 10pm and tonight's local food vendor is Yangzi from Media.&nbsp;<br>Please be aware that the Grill close's nightly at 9:30pm.<u></u><u></u></html-blob>", 'cleaned_description': "Here to serve you Breakfast, lunch and Dinner Today's Lunch Special South of the Border Burger- Beef patty, pepper jack cheese, bacon and pico de gallo with French fries and a choice of drink. Todays Soup Lobster Bisque Late Night Meal Plan is available 4pm till 10pm and tonight's local food vendor is Yangzi from Media. Please be aware that the Grill close's nightly at 9:30pm."}], 'science_center': Science Center coffee bar [Science Center coffee bar Science Center Open {'title': 'Science Center Open', 'startdate': '2022-02-14 08:00:00', 'enddate': '2022-02-15 00:00:00', 'short_time': '8:00am - 12:00am', 'description': "We are here to serve you coffee and specialty drinks. We also have a variety of pastries and snacks available. Our local food vendor Yangzi will be here daily for lunch serving Chinese and Sushi. Late Night Meal Plan is available 10pm till midnight. Tonight's local food vendor is Shere Punjab from Media.", 'html_description': "<html-blob>We are here to serve you coffee and specialty drinks. We also have a variety of pastries and snacks available. <br>Our local food vendor Yangzi will be here daily for lunch serving Chinese and Sushi.  <br>Late Night Meal Plan is available 10pm till midnight. <br>Tonight's local food vendor is Shere Punjab from Media.&nbsp;</html-blob>", 'cleaned_description': "We are here to serve you coffee and specialty drinks. We also have a variety of pastries and snacks available. Our local food vendor Yangzi will be here daily for lunch serving Chinese and Sushi. Late Night Meal Plan is available 10pm till midnight. Tonight's local food vendor is Shere Punjab from Media."}]}
```

#### Dining availability
Marys objects have an `open` property which states whether this object or descendants is open.

``` python console
>>> m.open  # Is anything open?
True
>>> m["sharples"].open  # Is Sharples open for any meal?
True
>>> m["sharples"][1]["title"]
'Continental Breakfast'
>>> m["sharples"][1].open  # Is continental breakfast available right now?
False
>>> m["dinner"].open  # Is dinner available anywhere right now?
True
```

#### String rendering
Marys objects have a complete string representation.

```python console
>>> str(m["tomorrow"])
"At Sharples Dining Hall\nBreakfast (07:30–09:30)\nSoup Island: Oatmeal with Raisins, Craisins and Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg and Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels and Spreads Yogurt, Granola and Cereal Dessert: Baker's Choice of Pastry or Donuts\nContinental Breakfast (09:30–10:30)\nServed by the Fireplace - Includes Selection of Breads and Bagels, Spreads, Yogurt and Granola, Cereal, Fresh Bakery Special or Donuts, Full Beverage Station with Coffee\nLunch (10:30–13:30)\nCuban Sandwiches and Yucca Fries Empanadas, Black Beans, Rice, and Island Slaw Kale and Edamame Salad (vegan), Lentil Stew (vegan) Broccoli Soups: Thai Vegetable, New England Clam Chowder Dessert: Brownies\nLite Lunch (13:30–16:00)\nIncludes Salad Bar and Deli with Selection of Breads and Wraps, Soups of the Day, Cereal and Granola, Ice Cream and Frozen Yogurt, Fresh Fruit, Full Beverage Station with Coffee\nDinner (16:00–20:00)\nBaked Chicken (halal) with Macaroni and Cheese Spanish Chickpea Stew (vegan), Mushroom Ragout with Buttered Noodles Potato Bar, with Baked Idaho's and Sweets, Onion Rings, Potato Skins, and All of the Toppings Lima Succotash, Greens Soups: Thai Vegetable, New England Clam Chowder Dessert: Pumpkin Cake\n\nAt Essie Mae's\nEssie Mae's Open (08:00–22:30)\nHere to serve you Breakfast, Lunch and Dinner. We also offer a large variety of snacks and grocery items. Today's Lunch Special Pork Carnita wrap- sauteed onions and peppers and cilantro mayonnaise served with French fries and a choice of drink. Todays Soup Broccoli Cheddar Late Night Meal Plan is available 4pm till 10pm and tonight's local food vendor is Dos Gringo's from Media. Please be aware that the Grill close's nightly at 9:30pm.\n\nAt Kohlberg coffee bar\nKohlberg Open (08:00–16:30)\nWe are open and ready to provide you with you Coffee and specialty drink needs. We also have a selection of Sandwiches, Salads and pastries. Hot food will be provided by Shere Punjab available from 11 am. Today's Soup -Classic beef Stew\nGrab & Go Lunch (11:30–13:30)\nRoast Turkey Sandwich on Ciabatta Tempeh Tomato and Lettuce on Multigrain Bread (vegan) Sunbutter and Jam on Multigrain Bread (vegan) Chicken Caesar Salad (halal) Chef's Salad with Ham, Turkey and Cheese\n\nAt Science Center coffee bar\nScience Center Open (08:00–00:00)\nWe are here to serve you coffee and specialty drinks. We also have a variety of pastries and snacks available. Our local food vendor Yangzi will be here daily for lunch serving Chinese and Sushi. Late Night Meal Plan is available 10pm till midnight. Tonight's local food vendor is Dos Gringo's from Media.\n\n"
>>> str(m["essies"][0])
"Essie Mae's Open (08:00–22:30)\nHere to serve you Breakfast, lunch and Dinner Today's Lunch Special South of the Border Burger- Beef patty, pepper jack cheese, bacon and pico de gallo with French fries and a choice of drink. Todays Soup Lobster Bisque Late Night Meal Plan is available 4pm till 10pm and tonight's local food vendor is Yangzi from Media. Please be aware that the Grill close's nightly at 9:30pm."
```

#### Speech rendering
Marys objects can be rendered as [Speech Synthesis Markup Language](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) for voice assistants and speech systems.

```python console
>>> m["dinner"].ssml()
'At Sharples Dining Hall<break strength="weak"/>Dinner (from 4:00pm to 8:00pm) <break strength="weak"/>Tilapia with Seafood Sauce, Rice Pilaf<break strength="weak"/>Butternut and Sage Orzo ::vegan::, Seitan Chimichurri ::vegan::<break strength="weak"/>Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth<break strength="weak"/>Pennsylvania Blend, Cauliflower<break strength="weak"/>Soups:  Vegetable ::vegan::, Tomato<break strength="weak"/>Dessert:  Cupcakes<break strength="weak"/>'
```

If using this library with Amazon Alexa, Alexa emotions are supported.

```python console
>>> marys.Menu(data={})["breakfast"].ssml(dialect=marys.SSMLDialect.AMAZON)
'<amazon:emotion name="disappointed" intensity="medium">Dining is currently unavailable at this time!</amazon:emotion>'
```

#### Card rendering
Similarly to `ssml`, Marys objects can be represented as a card (object with title and content). These are useful for creating dialog boxes in graphical programs or textual responses for voice assistants like Alexa and Google Assistant.

```python console
>>> m["sharples"].card()
Card(title='At Sharples Dining Hall', content="Breakfast (07:30–09:30)\nSoup Island: Oatmeal with Raisins, Craisins and Cinnamon Sugar Main: Eggs to Order, Bacon, Chicken Sausage, Hashbrown Potatoes Phoenixes - Egg and Cheese Sandwiches Chef's Choice of Waffles, French Toast or Pancakes Fresh Fruit, Selection of Bread, Bagels and Spreads Yogurt, Granola and Cereal Dessert: Baker's Choice of Pastry or Donuts\nContinental Breakfast (09:30–10:30)\nServed by the Fireplace - Includes Selection of Breads and Bagels, Spreads, Yogurt and Granola, Cereal, Fresh Bakery Special or Donuts, Full Beverage Station with Coffee\nLunch (10:30–13:30)\nChicken Fingers and Fries Homestyle Tofu with Green Beans (vegan), Vegetable Lo Mein Cheesesteak Bar, with Vegan, Beef, and Chicken Options, and Toppings Corn, Peas Soups: Vegetable (vegan), Tomato Dessert: Hope's Homestyle Cookies, Homemade Vegan Cookies\nLite Lunch (13:30–16:00)\nIncludes Salad Bar and Deli with Selection of Breads and Wraps, Soups of the Day, Cereal and Granola, Ice Cream and Frozen Yogurt, Fresh Fruit, Full Beverage Station with Coffee\nDinner (16:00–20:00)\nTilapia with Seafood Sauce, Rice Pilaf Butternut and Sage Orzo (vegan), Seitan Chimichurri (vegan) Tortilla Soup Bar, with Chips, Chicken, Rice, Black Beans, Corn, Jalapenos, Cheese, and Choice of Chicken or Vegan Broth Pennsylvania Blend, Cauliflower Soups: Vegetable (vegan), Tomato Dessert: Cupcakes\n")
>>> m["sharples"].card().title
'At Sharples Dining Hall'
```

## Asynchronous programs
For programs using Python's coroutine (`async`/`await`) syntax, a coroutine is provided to asynchronously construct a `Menu` object. If your programs do not use the `async` or `await` keywords, you don't need to use this.

```python
m = await marys.Menu.asynchronous()
```

## What's with the name?
This library was named after Mary Kassab, a Sharples manager who often assisted me, a totally blind student, in navigating the dining hall.
