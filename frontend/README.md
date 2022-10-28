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

Here, we are relying on the django routes to load what pages are needed. In `templates/index.html` you can see the `<main-page>` attribute which will render all the styles, js, and templates defined in our `Main` web component. Also note how to it takes attributes from the django template about the user. This is later read in Page.ts and removed, then using this id, we get the user information from the api for each Page.

So adding a page means creating a new django route, say for `/profile/<authorId>/` and adding a `<profile-page>` element in the body, taking the right attributes

## Creating custom components:

Following the example `TemplateComponent` in `/components` you can see how we should define components.

### [name].ts
The main typescript file that contains the `FASTElement` definition contains the logic for the experience. It should also hold the data for a given component, retrieved from the API, for example: `@observable profile?: Profile;`

Properties of this class can be given decorators like `@observable` or `@attr`. `@attr` should be used for primitives like strings and integers, `@observable` for everything else. These decorators signify to the FAST system that changes to these properties should force a change in the template, if it needs to. These properties are then reactive to changes in data.

### [name].styles.ts
Pretty straightforward, contains the styles for a web component. Note the `css` function to define css. There are ways to retrieve constant global colors using the FASTDesignSystem, but I still have to define them.

### [name].template.ts
The template for a web component. Defines what the *shadowRoot* will actually look like in the browser. Use bindings like `${x => x.greeting}` to display data reactively (make sure the greeting is `@observable`!). Here, `x` binds to the data model next the the html tag (ie. `html<Main>` x will refer to the Main class and can use any methods or properties defined there). Be sure to use directives like `repeat()` when displaying a list of components or HTMLElements. You can also use other web components in the template, make sure to import the **component definition** from the appropriate `index.ts`.

### index.ts
Brings the template, styles, and logic together in one web component. For webpack, this is the entry point for the web component. It defines the fastDesignSystem, web component for the browser, and registers any additional fast-components. To use a custom component in another template, import the definition exported from this file.

### Register the component, page, or library.
In index.ts, call defineComponent to define the web component for the browser.

## Creating data services:

Use the `/lib` folder to store any complicated data logic scripts, like fetching from the api.

Store any api fetch calls you use in the SocialApi.ts file.
