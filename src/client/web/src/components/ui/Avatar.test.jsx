import { render, screen } from '@testing-library/react';
import { Avatar } from './Avatar';
import { describe, it, expect } from 'vitest';

describe('Avatar Component', () => {
  it('renders image when src is provided', () => {
    render(<Avatar src="https://example.com/avatar.jpg" alt="User Avatar" />);
    const img = screen.getByRole('img', { name: /user avatar/i });
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', 'https://example.com/avatar.jpg');
  });

  it('renders fallback text when src is missing', () => {
    render(<Avatar fallback="JD" />);
    expect(screen.getByText('JD')).toBeInTheDocument();
  });

  it('renders initial from alt text when src and fallback are missing', () => {
    render(<Avatar alt="John Doe" />);
    expect(screen.getByText('J')).toBeInTheDocument();
  });

  it('applies correct size classes', () => {
    const { container } = render(<Avatar size="lg" fallback="LG" />);
    // The outer div should have the size class
    expect(container.firstChild).toHaveClass('h-24 w-24');
  });
});
