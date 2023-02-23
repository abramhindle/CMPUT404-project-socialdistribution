import { render, screen } from '@testing-library/react';
import Sidebar from './sidebar';

test('Inbox option present', () => {
  render(<Sidebar />);
  const inboxOption = screen.getByText(/Inbox/i);
  expect(inboxOption).toBeInTheDocument();
});

test('Requests option present', () => {
    render(<Sidebar />);
    const reqOption = screen.getAllByText(/Requests/i);
    expect(reqOption).toHaveLength(2);
});

test('Post option present', () => {
    render(<Sidebar />);
    const postOption = screen.getAllByText(/Post/i);
    expect(postOption).toHaveLength(3);
});

test('Profile shown', () => {
    render(<Sidebar />);
    const profile = screen.getByText(/Profile/i);
    expect(profile).toBeInTheDocument();
});