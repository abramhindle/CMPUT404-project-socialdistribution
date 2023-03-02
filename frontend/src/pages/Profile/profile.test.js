import { render, screen } from '@testing-library/react';
import Inbox from './inbox';


test('renders learn react link', () => {
  render(<Inbox />);
  const profileElement = screen.getByText(/Profile/i);
  expect(profileElement).toBeInTheDocument();

  const inboxElement = screen.getByText(/This is now the inbox page/i);
  expect(profileElement).toBeInTheDocument();
});