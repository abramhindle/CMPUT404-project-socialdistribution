# Using FAST Web Components

First, get familiar with the web component lifecycle here: https://www.fast.design/docs/fast-element/defining-elements.

## Running the front-end:

At the root of the project, navigate to the frontend.

`cd frontend`

Call `npm ci` install all the required node modules.
Then call `npm run build` to build the webpack bundles.
Now the required .js and .css files should be present in frontend/build.

In a separate terminal, run the django server using `python manage.py runserver` from the `/backend` folder.

## Adding a new page:

Here, we are relying on the django routes to load what pages are needed. In `templates/index.html` you can see the `<main-page>` attribute which will render all the styles, js, and templates defined in our `MainPageComponent`. However this is subject to change with feedback from the team.

So adding a page means creating a new django route, say for `/profile?authorId=` and adding a `<profile-page>` element in the body.

## Creating custom components:

Following the example `TemplateComponent` in `/components` you can see how we should define components.

### [name].ts
The main typescript file that contains the `FASTElement` definition contains the logic for the experience. It should also hold the data for a given component, retrieved from the API, for example: `@observable profile?: Profile;`

### [name].styles.ts
Pretty straightforward, contains the styles for a web component. Note the `css` function to define css. There are ways to retrieve constant global colors using the FASTDesignSystem, but I still have to define them.

### [name].template.ts
The template for a web component. Defines what the *shadowRoot* will actually look like in the browser. Use bindings like `${x => x.greeting}` to display data reactively (make sure the greeting is `@observable`!). Be sure to use directives like `repeat()` when displaying a list of components or HTMLElements. You can also use other web components in the template, make sure to import the **component** class, and not the **logic** class.

### [name].connector.ts
Brings the template, styles, and logic together in one web component.
Note, **the web component is exported as a new class with a different name**. Use this name when referring to it as the **component** to differentiate from the **logic** class. So when referencing the template web component in the Main page, I import `MyTemplateComponent` instead of `TemplateComponent`.

### Register the component, page, or library.
In `src/appRegistry` add your component, along with the its definition, to the list of web components. This list is used to define web components for the browser, depending on the page (eventually, working on it).

## Creating data services:

Use the `/lib` folder to store any complicated data logic scripts, like fetching from the api.
