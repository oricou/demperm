import { render, screen, fireEvent } from '@testing-library/react';
import { VoteCard } from './VoteCard';
import { describe, it, expect, vi } from 'vitest';

describe('VoteCard Component', () => {
  it('renders title and subtitle', () => {
    render(<VoteCard title="Election 2025" subtitle="Presidential" />);
    expect(screen.getByText('Election 2025')).toBeInTheDocument();
    expect(screen.getByText('Presidential')).toBeInTheDocument();
  });

  it('renders vote count if provided', () => {
    render(<VoteCard title="Election" votes="100 votes" />);
    expect(screen.getByText('100 votes')).toBeInTheDocument();
  });

  it('renders correct status badge based on accent prop', () => {
    const { rerender } = render(<VoteCard title="Election" accent="warning" />);
    expect(screen.getByText('En attente')).toBeInTheDocument();
    expect(screen.getByText('En attente')).toHaveClass('text-warning');

    rerender(<VoteCard title="Election" accent="danger" />);
    expect(screen.getByText('Non voté')).toBeInTheDocument();
    expect(screen.getByText('Non voté')).toHaveClass('text-danger');
  });

  it('does not render badge for default accent', () => {
    render(<VoteCard title="Election" accent="default" />);
    expect(screen.queryByText('En attente')).not.toBeInTheDocument();
    expect(screen.queryByText('Non voté')).not.toBeInTheDocument();
  });

  it('applies active styles when active prop is true', () => {
    render(<VoteCard title="Election" active={true} />);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('border-primary');
    expect(button).toHaveClass('bg-white');
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<VoteCard title="Election" onClick={handleClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
