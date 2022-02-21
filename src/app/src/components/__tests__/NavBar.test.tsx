import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import { screen } from '@testing-library/react';
import renderer from 'react-test-renderer';

import NavBar from '../NavBar';

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

describe('Navbar suite', () => {
  let items = [
    {
      Text: 'Hello?',
      handleClick: () => {
        console.log('Hello');
      },
    },
  ];
  it('Navbar children', () => {
    render(<NavBar items={items} />, container);
    expect(screen.getByText(/Hello/i).textContent).toBe('Hello?');
  });
  it('handleClick function', () => {
    console.log = jest.fn();
    render(<NavBar items={items} />, container);
    const button = screen.getByText(/Hello/i);
    button.click();
    expect(console.log).toHaveBeenCalledWith('Hello');
  });
});
