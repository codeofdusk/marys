# Marys
A Python library to obtain dining hours and menus at Swarthmore College.

Copyright 2021 Bill Dengler

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
'Brunch'
>>> m["sharples"][0]["enddate"]
'2021-02-07 13:30:00'
>>> m["sharples"][0]["description"]
'Scrambled Eggs or Tofu Scramble (v)\r\nBacon and Chicken Sausage\r\nHomefries\r\nButtermilk Biscuits\r\nLentil Stew and Rice (v)\r\nAsparagus\r\nVegan Chili\r\nOatmeal (v)\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette\r\nGrill Item:&nbsp; Phoenix Sandwiches\r\nDessert:&nbsp; Donuts'
```

### Conveniences
Marys adds extra features on top of the base API to ease access to the menu.

#### `cleaned_description`
While the original `description` is provided for backwards compatibility with the original JSON API, there is also a `cleaned_description` more suitable for use inside applications, with resolved HTML entities and cleaned-up formatting.

```python console
>>> m["sharples"][0]["cleaned_description"]
'Scrambled Eggs or Tofu Scramble (v)\nBacon and Chicken Sausage\nHomefries\nButtermilk Biscuits\nLentil Stew and Rice (v)\nAsparagus\nVegan Chili\nOatmeal (v)\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Phoenix Sandwiches\nDessert:  Donuts'
```

#### Access by meal period
`Menu` objects contain special `breakfast`, `lunch`, `dinner`, and `current` keys for accessing breakfast, lunch, dinner, or next available meals respectively. Lunch automatically resolves to brunch when necessary.

```python console
>>> m["breakfast"]
{}
>>> m["lunch"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Brunch {'title': 'Brunch', 'startdate': '2021-02-07 10:30:00', 'enddate': '2021-02-07 13:30:00', 'short_time': '10:30am - 1:30pm', 'description': 'Scrambled Eggs or Tofu Scramble (v)\r\nBacon and Chicken Sausage\r\nHomefries\r\nButtermilk Biscuits\r\nLentil Stew and Rice (v)\r\nAsparagus\r\nVegan Chili\r\nOatmeal (v)\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette\r\nGrill Item:&nbsp; Phoenix Sandwiches\r\nDessert:&nbsp; Donuts', 'html_description': 'Scrambled Eggs or Tofu Scramble (v)<br />\r\nBacon and Chicken Sausage<br />\r\nHomefries<br />\r\nButtermilk Biscuits<br />\r\nLentil Stew and Rice (v)<br />\r\nAsparagus<br />\r\nVegan Chili<br />\r\nOatmeal (v)<br />\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette<br />\r\nGrill Item:&nbsp; Phoenix Sandwiches<br />\r\nDessert:&nbsp; Donuts', 'cleaned_description': 'Scrambled Eggs or Tofu Scramble (v)\nBacon and Chicken Sausage\nHomefries\nButtermilk Biscuits\nLentil Stew and Rice (v)\nAsparagus\nVegan Chili\nOatmeal (v)\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Phoenix Sandwiches\nDessert:  Donuts'}]}
>>> m["dinner"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Dinner {'title': 'Dinner', 'startdate': '2021-02-07 16:30:00', 'enddate': '2021-02-07 18:30:00', 'short_time': '4:30pm - 6:30pm', 'description': 'Chicken Cutlets with Mashed Potatoes and Gravy\r\nLemony Tofu (v)\r\nPasta with Marinara (v) or Pesto Cream Sauce\r\nSpinach\r\nVegan Chili\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette\r\nGrill Item:&nbsp; Hot Dogs\r\nDessert:&nbsp; Oreo Cheesecake\r\n\r\n(v) denotes vegan option', 'html_description': 'Chicken Cutlets with Mashed Potatoes and Gravy<br />\r\nLemony Tofu (v)<br />\r\nPasta with Marinara (v) or Pesto Cream Sauce<br />\r\nSpinach<br />\r\nVegan Chili<br />\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette<br />\r\nGrill Item:&nbsp; Hot Dogs<br />\r\nDessert:&nbsp; Oreo Cheesecake<br />\r\n<br />\r\n<em>(v) denotes vegan option</em>', 'cleaned_description': 'Chicken Cutlets with Mashed Potatoes and Gravy\nLemony Tofu (v)\nPasta with Marinara (v) or Pesto Cream Sauce\nSpinach\nVegan Chili\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Hot Dogs\nDessert:  Oreo Cheesecake\n\n(v) denotes vegan option'}]}
>>> m["current"]
{'sharples': Sharples Dining Hall [Sharples Dining Hall Dinner {'title': 'Dinner', 'startdate': '2021-02-07 16:30:00', 'enddate': '2021-02-07 18:30:00', 'short_time': '4:30pm - 6:30pm', 'description': 'Chicken Cutlets with Mashed Potatoes and Gravy\r\nLemony Tofu (v)\r\nPasta with Marinara (v) or Pesto Cream Sauce\r\nSpinach\r\nVegan Chili\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette\r\nGrill Item:&nbsp; Hot Dogs\r\nDessert:&nbsp; Oreo Cheesecake\r\n\r\n(v) denotes vegan option', 'html_description': 'Chicken Cutlets with Mashed Potatoes and Gravy<br />\r\nLemony Tofu (v)<br />\r\nPasta with Marinara (v) or Pesto Cream Sauce<br />\r\nSpinach<br />\r\nVegan Chili<br />\r\nSpecialty Salad:&nbsp; Spinach and Mandarin Oranges with Raspberry Vinaigrette<br />\r\nGrill Item:&nbsp; Hot Dogs<br />\r\nDessert:&nbsp; Oreo Cheesecake<br />\r\n<br />\r\n<em>(v) denotes vegan option</em>', 'cleaned_description': 'Chicken Cutlets with Mashed Potatoes and Gravy\nLemony Tofu (v)\nPasta with Marinara (v) or Pesto Cream Sauce\nSpinach\nVegan Chili\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Hot Dogs\nDessert:  Oreo Cheesecake\n\n(v) denotes vegan option'}]}
```

#### Dining availability
Marys objects have an `open` property which states whether this object or descendants is open.

``` python console
>>> m.open  # Is anything open?
False
>>> m["sharples"].open  # Is Sharples open for any meal?
False
>>> m["sharples"][1]["title"]
'Dinner'
>>> m["sharples"][1].open  # Is Sharples open for dinner?
False
>>> m["dinner"].open  # Is dinner available anywhere right now?
False
```

#### String rendering
Marys objects have a complete string representation.

```python console
>>> str(m["tomorrow"])
"At Sharples Dining Hall\nBreakfast (07:30–10:00)\n\nLunch (11:30–14:30)\nMain Entrees:  \nChicken Fingers and French Fries\nVegetable Lo Mein\nHomestyle Tofu with Green Beans and Rice\nCorn\nSoups:  Garden Vegetable (v), Chicken Noodle\nSpecialty Salad:  Coleslaw\nGrill Offering:  Black Bean Burger, Cheeseburger\nDessert:  Hope's Homestyle Cookies, and Our Own Vegan Banana Chocolate Chip Cookies\n\n(v) indicates vegan option\nDinner (16:30–20:00)\nMain Entrees: \nTilapia with Seafood Sauce\nRice Pilaf (v)\nButternut Sage Orzo (v)\nSeitan Chimichurri (v)\nAsparagus\nSoups:  Garden Vegetable (v), Chicken Noodle\nSpecialty Salad:  Coleslaw\nGrill Offering:  Turkey Burgers, with or without Cheese\nDessert:  Strawberry Cheesecake\n\n(v) indicates vegan option\n\nAt Essie Mae's\nEssie's Open (08:00–15:00)\nWe are open and serving Breakfast and Lunch. We have a wide variety of snacks and Drinks available for purchase. \nDeli Lunch Special:\nCorned Beef Reuben Sandwich served with French fries and a choice of drink. \nFor the Safety of our Customers and Staff Essie's will remain takeout only until further notice.\n\n"
>>> str(m["tomorrow"]["sharples"])
"At Sharples Dining Hall\nBreakfast (07:30–10:00)\n\nLunch (11:30–14:30)\nMain Entrees:  \nChicken Fingers and French Fries\nVegetable Lo Mein\nHomestyle Tofu with Green Beans and Rice\nCorn\nSoups:  Garden Vegetable (v), Chicken Noodle\nSpecialty Salad:  Coleslaw\nGrill Offering:  Black Bean Burger, Cheeseburger\nDessert:  Hope's Homestyle Cookies, and Our Own Vegan Banana Chocolate Chip Cookies\n\n(v) indicates vegan option\nDinner (16:30–20:00)\nMain Entrees: \nTilapia with Seafood Sauce\nRice Pilaf (v)\nButternut Sage Orzo (v)\nSeitan Chimichurri (v)\nAsparagus\nSoups:  Garden Vegetable (v), Chicken Noodle\nSpecialty Salad:  Coleslaw\nGrill Offering:  Turkey Burgers, with or without Cheese\nDessert:  Strawberry Cheesecake\n\n(v) indicates vegan option\n"
>>> str(m["tomorrow"]["sharples"][1])
"Lunch (11:30–14:30)\nMain Entrees:  \nChicken Fingers and French Fries\nVegetable Lo Mein\nHomestyle Tofu with Green Beans and Rice\nCorn\nSoups:  Garden Vegetable (v), Chicken Noodle\nSpecialty Salad:  Coleslaw\nGrill Offering:  Black Bean Burger, Cheeseburger\nDessert:  Hope's Homestyle Cookies, and Our Own Vegan Banana Chocolate Chip Cookies\n\n(v) indicates vegan option"
```

#### Speech rendering
Marys objects can be rendered as [Speech Synthesis Markup Language](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) for voice assistants and speech systems.

```python console
>>> m["tomorrow"].ssml()
"At Sharples Dining Hall<break/>Breakfast (from 7:30am to 10:00am) <break/><break/>Lunch (from 11:30am to 2:30pm) <break/>Main Entrees:  <break/>Chicken Fingers and French Fries<break/>Vegetable Lo Mein<break/>Homestyle Tofu with Green Beans and Rice<break/>Corn<break/>Soups:  Garden Vegetable (vegan), Chicken Noodle<break/>Specialty Salad:  Coleslaw<break/>Grill Offering:  Black Bean Burger, Cheeseburger<break/>Dessert:  Hope's Homestyle Cookies, and Our Own Vegan Banana Chocolate Chip Cookies<break/>Dinner (from 4:30pm to 8:00pm) <break/>Main Entrees: <break/>Tilapia with Seafood Sauce<break/>Rice Pilaf (vegan)<break/>Butternut Sage Orzo (vegan)<break/>Seitan Chimichurri (vegan)<break/>Asparagus<break/>Soups:  Garden Vegetable (vegan), Chicken Noodle<break/>Specialty Salad:  Coleslaw<break/>Grill Offering:  Turkey Burgers, with or without Cheese<break/>Dessert:  Strawberry Cheesecake<break/>At Essie Mae's<break/>Essie's open (from 8:00am to 3:00pm) <break/>We are open and serving Breakfast and Lunch. We have a wide variety of snacks and Drinks available for purchase. <break/>Deli Lunch Special:<break/>Corned Beef Reuben Sandwich served with French fries and a choice of drink. <break/>For the Safety of our Customers and Staff Essie's will remain takeout only until further notice."
>>> m["sharples"].ssml()
'At Sharples Dining Hall<break/>Brunch (from 10:30am to 1:30pm) <break/>Scrambled Eggs or Tofu Scramble (vegan)<break/>Bacon and Chicken Sausage<break/>Homefries<break/>Buttermilk Biscuits<break/>Lentil Stew and Rice (vegan)<break/>Asparagus<break/>Vegan Chili<break/>Oatmeal (vegan)<break/>Specialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette<break/>Grill Item:  Phoenix Sandwiches<break/>Dessert:  Donuts<break/>Dinner (from 4:30pm to 6:30pm) <break/>Chicken Cutlets with Mashed Potatoes and Gravy<break/>Lemony Tofu (vegan)<break/>Pasta with Marinara (vegan) or Pesto Cream Sauce<break/>Spinach<break/>Vegan Chili<break/>Specialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette<break/>Grill Item:  Hot Dogs<break/>Dessert:  Oreo Cheesecake'
>>> m["sharples"][1].ssml()
'Dinner (from 4:30pm to 6:30pm) <break/>Chicken Cutlets with Mashed Potatoes and Gravy<break/>Lemony Tofu (vegan)<break/>Pasta with Marinara (vegan) or Pesto Cream Sauce<break/>Spinach<break/>Vegan Chili<break/>Specialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette<break/>Grill Item:  Hot Dogs<break/>Dessert:  Oreo Cheesecake'
```

If using this library with Amazon Alexa, Alexa emotions are supported.

```python console
>>> m["breakfast"].ssml(dialect=marys.SSMLDialect.AMAZON)
'<amazon:emotion name="disappointed" intensity="medium">Dining is currently unavailable at this time!</amazon:emotion>'
```

#### Card rendering
Similarly to `ssml`, Marys objects can be represented as a card (object with title and content). These are useful for creating dialog boxes in graphical programs or textual responses for voice assistants like Alexa and Google Assistant.

```python console
>>> m["sharples"].card()
Card(title='At Sharples Dining Hall', content='Brunch (10:30–13:30)\nScrambled Eggs or Tofu Scramble (v)\nBacon and Chicken Sausage\nHomefries\nButtermilk Biscuits\nLentil Stew and Rice (v)\nAsparagus\nVegan Chili\nOatmeal (v)\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Phoenix Sandwiches\nDessert:  Donuts\nDinner (16:30–18:30)\nChicken Cutlets with Mashed Potatoes and Gravy\nLemony Tofu (v)\nPasta with Marinara (v) or Pesto Cream Sauce\nSpinach\nVegan Chili\nSpecialty Salad:  Spinach and Mandarin Oranges with Raspberry Vinaigrette\nGrill Item:  Hot Dogs\nDessert:  Oreo Cheesecake\n\n(v) denotes vegan option\n')
>>> m["tomorrow"]["essies"][0].card()
Card(title="Essie's Open (08:00–15:00)", content="We are open and serving Breakfast and Lunch. We have a wide variety of snacks and Drinks available for purchase. \nDeli Lunch Special:\nCorned Beef Reuben Sandwich served with French fries and a choice of drink. \nFor the Safety of our Customers and Staff Essie's will remain takeout only until further notice.")
```

Cards can also be formatted as HTML.

```python console
>>> m["tomorrow"].card(html=True)
Card(title='Menu', content="<h2>At Sharples Dining Hall</h2><h3>Breakfast (07:30–10:00)</h3><p></p>\n<h3>Lunch (11:30–14:30)</h3><p><strong>Main Entrees:&nbsp;&nbsp;</strong><br />\r\nChicken Fingers and French Fries<br />\r\nVegetable Lo Mein<br />\r\nHomestyle Tofu with Green Beans and Rice<br />\r\nCorn<br />\r\n<strong>Soups:&nbsp;&nbsp;</strong>Garden Vegetable (v), Chicken Noodle<br />\r\n<strong>Specialty Salad:&nbsp;&nbsp;</strong>Coleslaw<br />\r\n<strong>Grill Offering:&nbsp;&nbsp;</strong>Black Bean Burger, Cheeseburger<br />\r\n<strong>Dessert:&nbsp;&nbsp;</strong>Hope's Homestyle Cookies, and Our Own Vegan Banana Chocolate Chip Cookies<br />\r\n<br />\r\n<em>(v) indicates vegan option</em></p>\n<h3>Dinner (16:30–20:00)</h3><p><strong>Main Entrees:</strong>&nbsp;<br />\r\nTilapia with Seafood Sauce<br />\r\nRice Pilaf (v)<br />\r\nButternut Sage Orzo (v)<br />\r\nSeitan Chimichurri (v)<br />\r\nAsparagus<br />\r\n<strong>Soups:&nbsp;&nbsp;</strong>Garden Vegetable (v), Chicken Noodle<br />\r\n<strong>Specialty Salad:&nbsp;&nbsp;</strong>Coleslaw<br />\r\n<strong>Grill Offering:&nbsp;&nbsp;</strong>Turkey Burgers, with or without Cheese<br />\r\n<strong>Dessert:&nbsp;&nbsp;</strong>Strawberry Cheesecake<br />\r\n<br />\r\n<em>(v) indicates vegan option</em></p>\n\n<h2>At Essie Mae's</h2><h3>Essie's Open (08:00–15:00)</h3><p>We are open and serving Breakfast and Lunch. We have a wide variety of snacks and Drinks available for purchase.&nbsp;<br />\r\n<strong>Deli Lunch Special:</strong><br />\r\nCorned Beef Reuben Sandwich served with French fries and a choice of drink.&nbsp;<br />\r\nFor the Safety of our Customers and Staff Essie's will remain takeout only until further notice.&nbsp;<br />\r\n&nbsp;</p>\n\n")
```

## Asynchronous programs
For programs using Python's coroutine (`async`/`await`) syntax, a coroutine is provided to asynchronously construct a `Menu` object. If your programs do not use the `async` or `await` keywords, you don't need to use this.

```python
m = await marys.Menu.asynchronous()
```

## What's with the name?
This library was named after Mary Kassab, a Sharples manager who often assisted me, a totally blind student, in navigating the dining hall.
