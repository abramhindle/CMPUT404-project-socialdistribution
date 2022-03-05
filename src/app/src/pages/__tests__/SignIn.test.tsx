import React from 'react';
import { unmountComponentAtNode } from 'react-dom';
import renderer from 'react-test-renderer';

import SignIn from '../SignIn';

let container: any = null;
//issues with container type and its methods

beforeEach(() => {
  // setup a DOM element as a render target
  container = document?.createElement('div');
  document?.body?.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container?.remove();
  container = null;
});

describe('SignUp suite', () => {
  it('Renders correctly', () => {
    const tree = renderer.create(<SignIn setCurrentUser={() => {}} />).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
