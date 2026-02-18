# User Story 

## User Story Writing Guidelines
### User Story Format
As a [user-rol], I want to [action] so that [value].

### Acceptance Criteria
Given that [xx],
when [xx]
then [xx]
and [xx]

### How to check that I wrote a correct one
1. Independent: Developed and released on its own
2. Negotioable: Method should be negotiable
3. Valuable: Each story should increase product value
4. Estimatble: can be sized by the team
5. Small: Complete within a sprint
6. Testable: In binary way can be tested. 

## My parameters

### Define the user
The user is a person (male or female) of any age that would like to follow a MIND diet. Lets call this "role" a dieter.

### Define the Value
The value to the user is **saving effort**:
- What would the user need to do without the app:
    - Organize meals to hit the weekly servings per food category in the MIND Diet plan. 
    - Prepare flexible cooking recipe instructions for each meal.
    - Create grosery shopping list for required food items. 
    - Keep track of weekly servings they have consumed from each category.
    - Recalculate plan when offtrack (or no food ingredients available).

- What the app will do for the user: 
    - Create a persoanlized meal plan for the user to hit the weekly servings per food category in the MIND Diet plan. 
        - considers dietary restrictions
        - considers dietary goals
        - considers dietary preferences
    - Prepare flexible cooking recipe instructions for each meal.
    - Create grosery shopping list for required food items. 
    - Keeps track of weekly services the user has conusmed for each category. 
    - Recalcualte plan if offtrack (or no food ingredients available).


## Features and their respective user stories

### Feature 1: Weekly Foods Menu
The App provides a randomized list of weekly foods that the belos items are achieved:
    1. Hit all required weekly serviecs per food category of the Mind Diet.
    2. Provides with the recommended amounts for the user's profile.
    3. Provides with the required nutrients for the user's profile.

User Story: As a dieter I want to receive information of the foods I should eat per week to follow the Mind Diet.

Success criteria: 
Given that is Monday, when I ask Mindy to start plan my week then Mindy provides with me with a list of foods according to my current kitchen inventory, restrictions, goals and preferences, and I decide whether to accept it or not. 

Quality check: 
1. Independent: Yes.
2. Negotioable: Yes.
3. Valuable: Yes.
4. Estimatble: Yes.
5. Small: Yes.
6. Testable: Yes.



### Feature 2: 
The app creates a grocery shoppig list for the next x weeks using parameters on: 
1. Current item inventory 
2. Perichabiity of items. 
3. Leverages feature 1 andonly proceeds to create the shopping list if the foods are approevd by the user. 

User Story: As a dieter I want to receive a list of foods I need to buy to make meals that follow my diet.

Success criteria: 
Given that I'm going to the store, when I ask Mindy to create me a shopping list then Mindy asks me for the number of weeks to plkan for and gives me a list personalized for me, and I accept or reject it.

Quality check: 
1. Independent: Yes.
2. Negotioable: Yes.
3. Valuable: Yes.
4. Estimatble: Yes.
5. Small: Yes.
6. Testable: Yes.


### Feature 3: Flexible Cooking Recipe
The app provides with flexible cooking recepies using current foods inventory that accomodate to user preferences, goals and dietary restrictions.

User Story: As a dieter I want to receive recipe options so that I can cook a meal I like that follows the Mind Diet and my personal parameters.

Success criteria: 
Given that its the start of the week, when I ask Mindy what to coook then Mindy gives me options of recipes using the MIND diet parameters, and I accept them as weekly meal plan. 





