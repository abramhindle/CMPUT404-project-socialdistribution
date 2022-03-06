import React from 'react';
import { unmountComponentAtNode } from 'react-dom';
import renderer from 'react-test-renderer';

import Profile from '../Profile';

let container: any = null;
//issues with container type and its methods
const testUser = {"id":"","displayName":"","github":" ","profileImage":" "}

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

describe('Profile suite', () => {
  it('Renders correctly', () => {
    const tree = renderer.create(<Profile currentUser={testUser}/>).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
