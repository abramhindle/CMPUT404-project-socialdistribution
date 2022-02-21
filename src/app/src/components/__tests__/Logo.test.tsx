import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import renderer from 'react-test-renderer';

import Logo from '../Logo';

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

describe('Logo suite', () => {
  it('Renders correctly', () => {
    const tree = renderer.create(<Logo />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('Logo text', () => {
    render(<Logo />, container);
    expect(container.textContent).toBe('Website.');
  });
});
