import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders the homepage with the app title', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Arcade Games App');
  });

  it('renders the home page heading', () => {
    render(<App />);
    const homeHeading = screen.getByRole('heading', { level: 2 });
    expect(homeHeading).toBeInTheDocument();
    expect(homeHeading).toHaveTextContent('Home Page');
  });

  it('renders the footer', () => {
    render(<App />);
    const footer = screen.getByText(/2026 Arcade Games/);
    expect(footer).toBeInTheDocument();
  });
});
